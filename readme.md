# On Parmak Öğrenci Çalışmaları Projesi

Python tabanlı bu proje, bir öğrenci performans izleme yardımcısıdır. Süratli on parmak yazma egzersizlerinden elde edilen CSV verilerini okuyarak SQLite veritabanına kaydeder. Proje bu yönüyle Python ile CSV işleme ve SQLite veritabanı işlemlerinin nasıl yapılabildiğine de bir örnek niteliğindedir.

On parmak daktilo eğitimi için TürkEgitim.net sitesinde yayımlanan [Uzaktan F Klavye Eğitimi Uygulaması](https://turkegitim.net/FKlavye/) esas alınmıştır. Proje, bu uygulamanın F Klavye ile on parmak yazma eğitimi sırasında topladığı öğrenci çalışma verisinin ileri analiz sürecine katkı sağlamayı amaçlar. Bunun için, uygulamanın eğitmenlere sunduğu CSV uzantılı "Öğrenci Çalışmaları" dosyasını işleyerek, "Sürat Çalışmaları" verisi ile bir SQLite veritabanı (vt/10p.db) oluşturur. Veritabanında öğrenci listesinin ve çalışma dökümlerinin yer aldığı iki ayrı tablo kurgulanmıştır.

## Özellikler

Bu proje;
- En güncel CSV dosyasını otomatik olarak seçer.
- Öğrenci listesi ve çalışma verisini tablolar halinde derler.
- Okunan veri, ileri çözümleme ve değerlendirme için SQLite veritabanına (vt/10p.db) kaydedilir.
- Modüler ve anlaşılır kod yapısına sahiptir. Hemen her bölüm açıklamalar ile desteklenmiştir.
- Geliştirmeye açıktır.

## Proje Yapısı

```plaintext
10p/
├── csv/               # İşlenecek CSV dosyaları
├── vt/                # Veritabanı dosyaları
│   ├── 10p.db         # Oluşturulacak veritabanı dosyası
│   └── sema.sql       # Veritabanı şeması
└── src/               # Proje kaynak dosyaları
    ├── csv_isler.py   # CSV okuma ve veritabanı işlemleri
    ├── vt_isler.py    # Veritabanı işlemleri
    ├── dosya_isler.py # Dosya işlemleri
    └── proje.py       # Ana çalışma dosyası
```

## Kurulum ve Çalıştırma

1. Sisteminizde Python 3.7 veya daha yeni bir sürümün yüklü olması önerilir.  
   Python’u [https://www.python.org/downloads/](https://www.python.org/downloads/) adresinden indirebilirsiniz.

2. Projeyi klonlayın veya indirin.

3. Sitenin eğitici sayfasından indirdiğiniz "OgrenciCalismalari_gg-aa-yyyy-ss-dd.csv" isim formatındaki dosyayı/dosyaları, projenin CSV klasörüne kaydedin.

4. Projeyi şu komut satırı ile çalıştırın:

	```bash
	python -m src.proje
	```

## Lisans

Bu proje MIT Lisansı ile lisanslanmıştır.

## İletişim

Herhangi bir soru veya katkı için bana ulaşabilirsiniz.

## Notlar

- Geliştirme sürecinde Dr. Murat AYDAN'ın kendi öğrencilerine ilişkin kayıtları referans alınmış, tüm kodlama ve testler bu veri üzerinden yine kendisi tarafından yapılmış, veri hiçbir şekilde üçüncü taraflar ile paylaşılmamıştır.
- Python ile kodlama sürecinde OpenAI ChatGPT yapay zeka asistanından kod ve fikir desteği alınmıştır.

---

**Anahtar Kelimeler:** Python, on parmak, F klavye, CSV, SQLite, öğrenci takibi, veri analizi, uzaktan eğitim, Python veritabanı uygulaması