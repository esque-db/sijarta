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
    FOR EACH ROW EXECUTE FUNCTION VALIDATE_UNIQUE_BANK_EMPLOYEE();