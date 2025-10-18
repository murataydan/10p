# On Parmak Öğrenci Çalışmaları Projesi

Python tabanlı bu proje, bir öğrenci performans izleme yardımcısıdır. Süratli on parmak yazma egzersizlerinden elde edilen CSV verilerini okuyarak SQLite veritabanına kaydeder. Proje bu yönüyle Python ile CSV işleme ve SQLite veritabanı işlemlerinin nasıl yapılabildiğine de bir örnek niteliğindedir.

On parmak süratli daktilo/klavye yazma eğitimi için TurkEgitim.net sitesinde yayımlanan [Uzaktan F Klavye Eğitimi Uygulaması](https://turkegitim.net/FKlavye/) esas alınmıştır. Proje, bu uygulamanın F Klavye ile on parmak yazma eğitimi sırasında topladığı öğrenci çalışma verisinin ileri analiz sürecine katkı sağlamayı amaçlar. Bunun için, uygulamanın eğitmenlere sunduğu CSV uzantılı "Öğrenci Çalışmaları" dosyasını işleyerek, "Sürat Çalışmaları" verisi ile bir SQLite veritabanı (vt/10p.db) oluşturur. Temel tablolara ek olarak kullanışlı görünümler hazırlar.

## Özellikler

Bu proje;
- En güncel CSV dosyasını otomatik olarak seçer.
- vt/sema/ klasörüne kaydedilecek dosyaları otomatik olarak tarar ve işler.
- Açıklamalar ile desteklenmiş, modüler yapı sayesinde kolayca yönetilebilir.

## Proje Yapısı

```plaintext
10p/
├── csv/                # İşlenecek CSV dosyaları
├── vt/                 # Veritabanı dosyaları
│   ├── 10p.db          # Oluşturulacak veritabanı dosyası
│   └── sema/           # Veritabanı şemaları
└── src/                # Proje kaynak dosyaları
    ├── csv_isler.py    # CSV okuma ve veritabanı işlemleri
    ├── vt_isler.py     # Veritabanı işlemleri
    └── dosya_isler.py  # Dosya işlemleri
    10p.py              # Ana çalışma dosyası
	...
```

## Kurulum ve Çalıştırma

1. Sisteminizde Python 3.7 veya daha yeni bir sürümün yüklü olması önerilir.  
   Python’u [https://www.python.org/downloads/](https://www.python.org/downloads/) adresinden indirebilirsiniz.

2. Projeyi klonlayın veya indirin.

3. Sitenin eğitici sayfasından indirdiğiniz "OgrenciCalismalari_gg-aa-yyyy-ss-dd.csv" isim formatındaki dosyayı/dosyaları, projenin CSV klasörüne kaydedin.

4. Projeyi şu komut satırı ile çalıştırın:

	```bash
	python -m 10p
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