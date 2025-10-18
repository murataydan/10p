from src.vt_isler import veritabani_baglan, veritabani_sifirla
from src.dosya_isler import en_guncel_csv_dosyasini_bul
from src.csv_isler import csv_oku_ve_veritabani_yaz

def main():
    """
    Programın ana fonksiyonu.
    - Veritabanına bağlanır ve şemayı yükler.
    - En güncel CSV dosyasını bulur.
    - CSV dosyasını veritabanına işler.
    """

    # Veritabanına bağlan
    baglanti = veritabani_baglan()

    # Eğer ihtiyaç varsa veritabanını sıfırla (şemayı tekrar yükle)
    print("Veritabanı şeması yükleniyor...")
    veritabani_sifirla(baglanti, sema_adresi="vt/sema/")

    # CSV dosyalarının bulunduğu klasörü belirt
    csv_klasoru = "csv"

    # En güncel CSV dosyasını bul
    csv_dosyasi = en_guncel_csv_dosyasini_bul(csv_klasoru)
    
    if csv_dosyasi is None:
        print("x İşlenecek CSV dosyası bulunamadı.")
    else:
        print(f"İşlenecek dosya: {csv_dosyasi}")

        # CSV dosyasını okuyup veritabanına aktar
        csv_oku_ve_veritabani_yaz(csv_dosyasi, baglanti)

    # Veritabanı bağlantısını kapat
    baglanti.close()

if __name__ == "__main__":
    main()
