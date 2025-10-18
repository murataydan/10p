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
    Her SQL ifadesi tek tek çalıştırılır, bilgiler ve hatalar konsola yazdırılır.
    Eğer herhangi bir ifade hata verirse tüm işlem rollback yapılır.
    """
    if baglanti is None:
        raise ValueError("Geçerli veritabanı bağlantısı bulunamadı.")

    try:
        with open(sema_adresi, "r", encoding="utf-8") as f:
            sema = f.read()  # SQL komutlarını dosyadan oku
    except OSError as e:
        raise RuntimeError(f"Şema dosyası okunamadı: {e}") from e

    cur = baglanti.cursor()
    errors = []

    try:
        # Transaction başlat
        baglanti.execute("BEGIN")
        # Basit ayırma: noktalı virgüle göre ayır ve boş parçaları atla
        for raw_stmt in sema.split(";"):
            stmt = raw_stmt.strip()
            if not stmt:
                continue
            try:
                cur.execute(stmt)
                print(f"[TAMAM] {stmt.splitlines()[0][:120]}")
            except sqlite3.Error as e:
                print(f"[HATA] {e}\n  Komut (kısaltılmış): {stmt[:200]}")
                errors.append((stmt, e))
                # Hata anında devam etmek yerine rollback ve çıkmak isterseniz hemen raise edin.
                # continue ile tüm komutları denemek mümkün; şu an hata varsa transaction rollback yapılacak.
        if errors:
            baglanti.rollback()
            first_err = errors[0][1]
            raise RuntimeError(f"Şema uygulanırken {len(errors)} hata oluştu. İlk hata: {first_err}") from first_err
        else:
            baglanti.commit()
            print("[TAMAM] Veritabanı kayda hazır.")
    except Exception:
        try:
            baglanti.rollback()
        except Exception:
            pass
        raise
