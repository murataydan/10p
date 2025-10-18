import os
import glob
import sqlite3

def veritabani_baglan(vt_adresi="vt/10p.db"):
    """
    Belirtilen dosya yolundaki SQLite veritabanına bağlanır.
    Dosya mevcut değilse oluşturur.

    vt_adresi (str): Veritabanı dosyasının adresi (varsayılan: '10p.db')
    sqlite3.Connection: Veritabanı bağlantı nesnesi
    """
    try:
        return sqlite3.connect(vt_adresi)
    except sqlite3.Error as e:
        raise RuntimeError(f"Veritabanına bağlanılamadı: {e}") from e


def veritabani_sifirla(baglanti, sema_adresi="vt/sema"):
    """
    *.sql dosyaları alfabetik sırada çalıştırılır.
    - Her dosya kendi transaction'ında çalıştırılır; hata olursa o dosya rollback edilir ve hata fırlatılır.

    baglanti (sqlite3.Connection): Veritabanı bağlantısı
    sema_adresi (str): SQL şema dosyası ya da dizin yolu
    """
    if baglanti is None:
        raise ValueError("Geçerli veritabanı bağlantısı bulunamadı.")

    # Dosya listesi oluştur
    files = []
    if os.path.isdir(sema_adresi):
        # dizindeki .sql dosyalarını sırala
        files = sorted(glob.glob(os.path.join(sema_adresi, "*.sql")))
        if not files:
            raise RuntimeError(f"x Şema dizini boş: {sema_adresi}")
    elif os.path.isfile(sema_adresi):
        files = [sema_adresi]
    else:
        raise RuntimeError(f"x Şema yolu bulunamadı: {sema_adresi}")

    cur = baglanti.cursor()
    for fpath in files:
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                sql = f.read()
        except OSError as e:
            raise RuntimeError(f"Şema dosyası okunamadı: {fpath}: {e}") from e

        print(f"- {os.path.basename(fpath)} çalıştırılıyor.")
        try:
            baglanti.execute("BEGIN")
            # executescript tüm dosyayı tek seferde çalıştırır (DOSYA İÇİNDE birden fazla ifade olabilir)
            cur.executescript(sql)
            baglanti.commit()
            print(f"+ {os.path.basename(fpath)} başarıyla uygulandı.")
        except sqlite3.Error as e:
            try:
                baglanti.rollback()
            except Exception:
                pass
            print(f"x {os.path.basename(fpath)} sırasında hata: {e}")
            raise RuntimeError(f"Şema uygulama hatası ({os.path.basename(fpath)}): {e}") from e
