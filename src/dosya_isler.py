import os
import glob
from datetime import datetime

def en_guncel_csv_dosyasini_bul(dizin="csv"):
    """
    Belirtilen dizinde 'OgrenciCalismalari_gg-aa-yyyy-ss-dd.csv' 
    formatına uyan CSV dosyalarını tarar ve en güncel olanı döner.

    Args:
        dizin (str): CSV dosyalarının bulunduğu klasörün yolu (varsayılan: 'csv')

    Returns:
        str or None: En güncel CSV dosyasının tam dosya yolu, bulunamazsa None
    """
    # Belirtilen dizindeki tüm eşleşen CSV dosyalarını bul
    dosyalar = glob.glob(os.path.join(dizin, "OgrenciCalismalari_*.csv"))

    en_guncel = None        # En güncel dosyanın yolu
    en_yeni_zaman = None    # En güncel dosyanın datetime objesi olarak zamanı

    for dosya in dosyalar:
        dosya_adi = os.path.basename(dosya)  # Sadece dosya adını al (klasörsüz)

        try:
            # Dosya adından tarih ve saat bilgisini ayıkla
            parca = dosya_adi.replace("OgrenciCalismalari_", "").replace(".csv", "")
            # 'gg-aa-yyyy-ss-dd' formatını datetime objesine dönüştür
            tarih = datetime.strptime(parca, "%d-%m-%Y-%H-%M")

            # Daha yeni bir dosya bulunursa onu en güncel olarak kaydet
            if (en_yeni_zaman is None) or (tarih > en_yeni_zaman):
                en_yeni_zaman = tarih
                en_guncel = dosya

        except ValueError:
            # Tarih formatı beklenmeyen dosyaları atla
            continue

    return en_guncel
