-- Store Procedure
CREATE OR REPLACE FUNCTION UPDATE_MYPAY_PEKERJA() RETURN TRIGGER AS
$$
    -- Deklarasi variable tersebut untuk transfer saldo MyPay
    DECLARE
        IdPekerja UUID;
        IdKategori UUID;
        BiayaJasa DECIMAL;

    BEGIN
        -- Jalankan jika status pekerjaan selesai
        IF NEW.Status = 'Pekerjaan Selesai' THEN

            -- Cari dan simpan biaya jasa dan ID pekerja
            SELECT PJ.TotalBiaya, PJ.IdPekerja
                INTO BiayaJasa, IdPekerja
            FROM STATUS_PESANAN S
                LEFT JOIN TR_PEMESANAN_STATUS PS ON S.Id = PS.IdStatus
                LEFT JOIN TR_PEMESANAN_JASA PJ ON PS.IdTrPemesanan = PJ.Id
            WHERE S.Id = NEW.Id;

            -- Simpan kategori transfer MyPay untuk pembayaran jasa
            SELECT Id
                INTO IdKategori
            FROM KATEGORI_TR_MYPAY
            WHERE Nama = 'Pembayaran Jasa';

            -- Masukkan histori transaksi MyPay
            INSERT INTO TR_MYPAY (Id, UserId, Tgl, Nominal, KategoriId) VALUES
            (gen_random_uuid(), IdPekerja, CURRENT_DATE, BiayaJasa, IdKategori);

            -- Tambah saldo pekerja dengan biaya jasa
            UPDATE USER
            SET SaldoMyPay = SaldoMyPay + BiayaJasa
            WHERE Id = IdPekerja;
        END IF;

        RETURN NEW;
    END;
$$
LANGUAGE plpgsql

-- Trigger
CREATE OR REPLACE TRIGGER TGR_STATUS_DONE
AFTER UPDATE ON STATUS_PESANAN
FOR EACH ROW
EXECUTE FUNCTION UPDATE_MYPAY();