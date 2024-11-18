-- Trigger
-- Pengecekan no HP yang terdaftar:
-- Ketika ada akun baru yang mendaftar, sistem terlebih dahulu mengecek apakah no HP sudah terdaftar atau belum.
-- Jika no HP sudah terdaftar, keluarkan pesan error.
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

-- Trigger
-- Pengecekan pasangan nama bank dan nomor rekening pekerja:
-- Ketika ada user mendaftarkan akun baru sebagai pekerja, sistem akan memastikan bahwa tidak ada pekerja lain 
-- yang memiliki kombinasi nama bank dan nomor rekening yang sama telah terdaftar.
-- Jika ada, keluarkan pesan error.
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
<<<<<<< HEAD
    FOR EACH ROW EXECUTE FUNCTION VALIDATE_UNIQUE_BANK_EMPLOYEE();

CREATE OR REPLACE FUNCTION batalkan_pesanan() RETURNS TRIGGER 
AS $$
DECLARE
    pelanggan_id UUID;
    total_biaya NUMERIC;
    id_status_dibatalkan INTEGER;
    id_status_mencari_pekerja INTEGER;
BEGIN
    SELECT Id INTO id_status_dibatalkan FROM STATUS_PESANAN WHERE Keterangan = 'Dibatalkan';
    SELECT Id INTO id_status_mencari_pekerja FROM STATUS_PESANAN WHERE Keterangan = 'Mencari Pekerja Terdekat';
    
    IF NEW.IdStatus = id_status_dibatalkan THEN
        IF OLD.IdStatus = id_status_mencari_pekerja THEN
            SELECT IdPelanggan, TotalBiaya INTO pelanggan_id, total_biaya
            FROM TR_PEMESANAN_JASA
            WHERE Id = NEW.IdTrPemesanan;
            
            UPDATE MYPAY
            SET Saldo = Saldo + total_biaya
            WHERE Id = pelanggan_id;
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_batalkan_pesanan
AFTER UPDATE ON TR_PEMESANAN_STATUS
FOR EACH ROW
EXECUTE FUNCTION batalkan_pesanan();
=======
    FOR EACH ROW EXECUTE FUNCTION VALIDATE_UNIQUE_BANK_EMPLOYEE();
>>>>>>> 2fc378bf43f1fc61e57cc7d1209406a9bee0f9e7
