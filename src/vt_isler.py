import sqlite3

def veritabani_baglan(vt_adresi="vt/10p.db"):
    """
    Belirtilen dosya yolundaki SQLite veritabanına bağlanır.
    Dosya mevcut değilse oluşturur.

    Args:
        vt_adresi (str): Veritabanı dosyasının adresi (varsayılan: '10p.db')

    Returns:
        sqlite3.Connection: Veritabanı bağlantı nesnesi
    """
    try:
        return sqlite3.connect(vt_adresi)
    except sqlite3.Error as e:
        raise RuntimeError(f"Veritabanına bağlanılamadı: {e}") from e


def veritabani_sifirla(baglanti, sema_adresi="vt/sema.sql"):
    """
    Belirtilen SQL şema dosyasını çalıştırarak veritabanını sıfırlar.
    Yani: Var olan tabloları siler ve şemaya göre yeniden oluşturur.

    Args:
        baglanti (sqlite3.Connection): Aktif veritabanı bağlantısı
        sema_adresi (str): SQL şema dosyasının yolu (varsayılan: 'vt/sema.sql')
    """
    if baglanti is None:
        raise ValueError("Geçerli veritabanı bağlantısı bulunamadı.")

    try:
        with open(sema_adresi, "r", encoding="utf-8") as f:
            sema = f.read()  # SQL komutlarını dosyadan oku
    except OSError as e:
        raise RuntimeError(f"Şema dosyası okunamadı: {e}") from e

    try:
        baglanti.executescript(sema)  # Tüm betiği bir kerede çalıştır
        baglanti.commit()  # Değişiklikleri kalıcı hale getir
    except sqlite3.Error as e:
        try:
            baglanti.rollback()
        except Exception:
            pass
        raise RuntimeError(f"Veritabanı oluşturulurken hata: {e}") from e
