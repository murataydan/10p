import re
from datetime import datetime

def ismi_ayristir(ham_isim):
    """
    Gelen isimden soyadını ayrıştırır.
    - Sondaki 1 veya 2 kelime eğer tamamen BÜYÜK harfse soyad olarak alınır.
    - Geri kalan kelimeler ad olarak alınır.
    - Eğer sondaki kelime BÜYÜK değilse (beklenmedik durum), son kelime soyad kabul edilir.
    - Ad: Her kelimenin ilk harfi büyük, geri kısmı küçük şeklinde döner.
    - Soyad: Tamamen büyük harf olarak döner.
    """
    toks = [t.strip() for t in ham_isim.split() if t.strip()]
    if not toks:
        return "", ""

    # Sondan başlayarak 1 veya 2 kelimeyi soyad olarak al (tamamen büyük harfli olanlar)
    surname_tokens = []
    given_tokens = toks.copy()

    if toks[-1].isupper():
        surname_tokens.insert(0, toks[-1])
        given_tokens = toks[:-1]
        # Eğer sondan bir önceki de tamamen büyükse iki kelimelik soyad al
        if len(toks) >= 2 and toks[-2].isupper():
            surname_tokens.insert(0, toks[-2])
            given_tokens = toks[:-2]
    else:
        # Fallback: son kelimeyi soyad al
        if len(toks) == 1:
            return toks[0].capitalize(), ""
        surname_tokens = [toks[-1]]
        given_tokens = toks[:-1]

    ad = " ".join(t.capitalize() for t in given_tokens).strip()
    soyad = " ".join(t.upper() for t in surname_tokens).strip()
    return ad, soyad

def csv_oku_ve_veritabani_yaz(csv_yolu, baglanti):
    """
    Verilen CSV dosyasını okuyup ayrıştırır ve veritabanına yazar.

    Args:
        csv_yolu (str): İşlenecek CSV dosyasının tam yolu
        baglanti (sqlite3.Connection): Aktif veritabanı bağlantısı
    """
    with open(csv_yolu, "r", encoding="utf-8", errors="replace") as f:
        tum_satirlar = [satir.strip() for satir in f if satir.strip()]  # Boş satırları at

    print(f"Toplam satır sayısı: {len(tum_satirlar)}")

    # 'SÜRAT TESTLERİ' başlığı bulunan satırdan sonra işlem başlayacak
    indis = None
    for idx, satir in enumerate(tum_satirlar):
        # Satırı büyük harfe çevir, boşluk ve noktalı virgülü kaldır
        temiz_satir = satir.upper().replace(" ", "").replace(";", "")
        if "SÜRATTESTLERİ" in temiz_satir:
            indis = idx + 1
            print("SÜRAT TESTLERİ başlığı bulundu, veri ayrıştırma başlıyor.")
            break

    if indis is None:
        print("Hata: 'SÜRAT TESTLERİ' başlığı bulunamadı, işlem durduruldu.")
        return

    # İşlem yapılacak satırlar (başlık satırından sonrası)
    satirlar = tum_satirlar[indis:]
    print(f"{len(satirlar)} satır işlenecek.")

    imlec = baglanti.cursor()
    i = 0
    while i < len(satirlar):
        satir = satirlar[i]

        # Öğrenci bilgisi başlangıcı (örnek: ÖĞRENCİ;Ad Soyad;(kullanici_adi))
        if satir.startswith("ÖĞRENCİ;"):
            try:
                parcalar = satir.split(";")
                ad_soyad = parcalar[1].strip()
                kullanici_adi = re.search(r"\((.*?)\)", parcalar[2]).group(1).strip()

                # Yeni ayrıştırma: sondaki 1 veya 2 tamamı büyük kelime(ler) soyad,
                # kalanlar ad. Ad Title case, soyad UPPER.
                ad, soyad = ismi_ayristir(ad_soyad)

                # Öğrenci bilgilerini veritabanına ekle veya güncelle
                imlec.execute("""
                    INSERT OR REPLACE INTO Ogrenciler (kullanici_adi, ad, soyad)
                    VALUES (?, ?, ?)
                """, (kullanici_adi, ad, soyad))

                i += 2  # Başlık satırını atla

            except Exception as e:
                print(f"Hata: Öğrenci bilgisi ayrıştırılamadı (satır {indis + i + 1}): {e}")
                i += 1
                continue

            # Öğrencinin çalışmalarını okuma döngüsü
            while i < len(satirlar) and not satirlar[i].startswith("ÖĞRENCİ;"):
                satir = satirlar[i]

                # Çalışma başlık satırını atla
                if satir.startswith("SN;"):
                    i += 1
                    continue

                try:
                    alanlar = satir.split(";")

                    # Gerekli alan sayısı kontrolü (en az 12 alan olmalı)
                    if len(alanlar) < 12:
                        print(f"Uyarı: Eksik alanlı satır atlandı: {satir}")
                        i += 1
                        continue

                    # Çalışma verisini veritabanına ekle
                    imlec.execute("""
                        INSERT INTO Calismalar (
                            kullanici_adi, sn, tarih, metin_no, sure, toplam_vurus, 
                            toplam_net_vurus, dakikalik_net_vurus, hata_sayisi, hata_orani, 
                            kelime_sayisi, katiplik_kelime_sayisi
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        kullanici_adi,
                        int(alanlar[0]),
                        tarih_donusumu(alanlar[1]),
                        int(alanlar[2]),
                        float(alanlar[3].replace(",", ".")),
                        int(alanlar[4]),
                        int(alanlar[5]),
                        int(alanlar[6]),
                        int(alanlar[7]),
                        float(alanlar[8].replace(",", ".")),
                        int(alanlar[9]),
                        int(alanlar[10])
                    ))

                except Exception as e:
                    print(f"Hata: Çalışma satırı işlenemedi (satır {indis + i + 1}): {e}")

                i += 1

        else:
            i += 1

    baglanti.commit()
    print("İşlem tamamlandı. Veritabanı hazır.")

def tarih_donusumu(tarih_str):
    """
    Tarih formatını "MM/DD/YYYY HH:MM:SS AM/PM" formatından "YYYY-MM-DD HH:MM:SS" formatına dönüştürür.

    tarih_str (str): Dönüştürülecek tarih stringi
    str: Dönüştürülmüş tarih stringi
    """
    dt = datetime.strptime(tarih_str, "%m/%d/%Y %I:%M:%S %p")
    return dt.strftime("%Y-%m-%d %H:%M:%S")