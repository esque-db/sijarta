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