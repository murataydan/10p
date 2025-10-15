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
    return sqlite3.connect(vt_adresi)


def veritabani_sifirla(baglanti, sema_adresi="vt/sema.sql"):
    """
    Belirtilen SQL şema dosyasını çalıştırarak veritabanını sıfırlar.
    Yani: Var olan tabloları siler ve şemaya göre yeniden oluşturur.

    Args:
        baglanti (sqlite3.Connection): Aktif veritabanı bağlantısı
        sema_adresi (str): SQL şema dosyasının yolu (varsayılan: 'vt/sema.sql')
    """
    with open(sema_adresi, "r", encoding="utf-8") as f:
        sema = f.read()  # SQL komutlarını dosyadan oku

    baglanti.executescript(sema)  # Tüm betiği bir kerede çalıştır
    baglanti.commit()  # Değişiklikleri kalıcı hale getir
