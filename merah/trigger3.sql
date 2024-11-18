-- Function: validate_voucher_usage
CREATE OR REPLACE FUNCTION validate_voucher_usage()
RETURNS TRIGGER AS $$
DECLARE
    kuota_penggunaan INT;
    jml_digunakan INT;
    tgl_berlaku DATE;
BEGIN
    -- Ambil informasi kuota dan tanggal berlaku dari tabel VOUCHER
    SELECT KuotaPenggunaan, JmlHariBerlaku
    INTO kuota_penggunaan, tgl_berlaku
    FROM VOUCHER
    WHERE Kode = NEW.IdVoucher;

    -- Hitung jumlah penggunaan voucher
    SELECT COUNT(*)
    INTO jml_digunakan
    FROM TR_PEMBELIAN_VOUCHER
    WHERE IdVoucher = NEW.IdVoucher;

    -- Validasi kuota penggunaan
    IF jml_digunakan >= kuota_penggunaan THEN
        RAISE EXCEPTION 'Voucher sudah mencapai batas kuota penggunaan.';
    END IF;

    -- Validasi tanggal berlaku
    IF CURRENT_DATE > (NEW.TglAwal + tgl_berlaku) THEN
        RAISE EXCEPTION 'Voucher sudah melewati batas hari berlaku.';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: trg_validate_voucher_usage
CREATE OR REPLACE TRIGGER trg_validate_voucher_usage
BEFORE INSERT ON TR_PEMBELIAN_VOUCHER
FOR EACH ROW
EXECUTE FUNCTION validate_voucher_usage();

-- Procedure: validate_voucher
CREATE OR REPLACE PROCEDURE validate_voucher(
    IN voucher_kode VARCHAR,
    OUT hasil_validasi VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    kuota_penggunaan INT;
    jml_digunakan INT;
    tgl_berlaku DATE;
BEGIN
    -- Ambil informasi kuota dan tanggal berlaku dari tabel VOUCHER
    SELECT KuotaPenggunaan, JmlHariBerlaku
    INTO kuota_penggunaan, tgl_berlaku
    FROM VOUCHER
    WHERE Kode = voucher_kode;

    -- Hitung jumlah penggunaan voucher
    SELECT COUNT(*)
    INTO jml_digunakan
    FROM TR_PEMBELIAN_VOUCHER
    WHERE IdVoucher = voucher_kode;

    -- Validasi kuota penggunaan
    IF jml_digunakan >= kuota_penggunaan THEN
        hasil_validasi := 'Voucher sudah mencapai batas kuota penggunaan.';
        RETURN;
    END IF;

    -- Validasi tanggal berlaku
    IF CURRENT_DATE > (SELECT TglAwal + tgl_berlaku FROM TR_PEMBELIAN_VOUCHER WHERE IdVoucher = voucher_kode LIMIT 1) THEN
        hasil_validasi := 'Voucher sudah melewati batas hari berlaku.';
        RETURN;
    END IF;

    hasil_validasi := 'VALID';
END;
$$;