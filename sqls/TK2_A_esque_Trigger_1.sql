CREATE OR REPLACE FUNCTION VALIDATE_PHONE_NUMBER()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS(
        SELECT 1
        FROM "USER"
        WHERE NoHP = NEW.NoHP
    ) THEN 
        RAISE EXCEPTION 'Nomor telepon yang sama sudah terdaftar';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER TRG_VALIDATE_PHONE_NUMBER
BEFORE INSERT ON "USER"
    FOR EACH ROW EXECUTE FUNCTION VALIDATE_PHONE_NUMBER();

CREATE OR REPLACE FUNCTION VALIDATE_UNIQUE_BANK_EMPLOYEE()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS(
        SELECT 1
        FROM PEKERJA
        WHERE NamaBank = NEW.NamaBank
            AND NomorRekening = NEW.NomorRekening
    ) THEN 
        RAISE EXCEPTION 'Kombinasi nama bank dan nomor rekening yang sama sudah terdaftar';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER TRG_VALIDATE_UNIQUE_BANK_EMPLOYEE
BEFORE INSERT ON PEKERJA
    FOR EACH ROW EXECUTE FUNCTION VALIDATE_UNIQUE_BANK_EMPLOYEE();

DELIMITER $$

CREATE PROCEDURE RefundSaldoMyPay(IN orderId UUID)
BEGIN
    DECLARE orderTotal DECIMAL(10,2);
    DECLARE userId UUID;

    SELECT TotalBiaya, IdPelanggan
    INTO orderTotal, userId
    FROM TR_PEMESANAN_JASA
    WHERE Id = orderId;

    DECLARE statusId UUID;
    SELECT Id INTO statusId
    FROM STATUS_PESANAN
    WHERE Status = 'Mencari Pekerja Terdekat';

    IF EXISTS (SELECT 1 FROM TR_PEMESANAN_STATUS WHERE IdTrPemesanan = orderId AND IdStatus = statusId) THEN
        UPDATE "USER"
        SET SaldoMyPay = SaldoMyPay + orderTotal
        WHERE Id = userId;

        INSERT INTO TR_MYPAY (Id, UserId, Tgl, Nominal, KategoriId)
        VALUES (UUID(), userId, CURDATE(), orderTotal, (SELECT Id FROM KATEGORI_TR_MYPAY WHERE Nama = 'Pengembalian Saldo'));
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Pesanan tidak dapat dibatalkan karena status tidak sesuai';
    END IF;
END $$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER AfterCancelOrder
AFTER UPDATE ON TR_PEMESANAN_STATUS
FOR EACH ROW
BEGIN
    -- Periksa apakah status pesanan berubah menjadi 'Dibatalkan'
    IF NEW.IdStatus = (SELECT Id FROM STATUS_PESANAN WHERE Status = 'Dibatalkan') THEN
        -- Panggil stored procedure untuk mengembalikan saldo
        CALL RefundSaldoMyPay(NEW.IdTrPemesanan);
    END IF;
END $$

DELIMITER ;