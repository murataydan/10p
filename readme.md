# TurkEgitim.net F-Klavye Öğrenci Çalışmaları Veri İşleme Projesi

Bu proje, TürkEgitim.net sitesinde yayımlanan F Klavye Eğitimi Uygulaması'nın (https://turkegitim.net/FKlavye/) eğiticilere sunduğu CSV uzantılı Öğrenci Çalışmaları dosyasını otomatik olarak işler ve dosyadaki veriyi SQLite veritabanına dönüştürür. Sitenin eğitici sayfasından indirilecek "OgrenciCalismalari_gg-aa-yyyy-ss-dd.csv" isim formatındaki dosyalar, projenin CSV klasörüne kaydedilmelidir. SQLite veritabanı vt alt dizininde oluşturulacaktır.

---

## Özellikler

Bu proje;
- İlgili klasördeki en güncel CSV dosyasını otomatik olarak seçer.
- CSV içerisindeki öğrenci ve çalışma verisi ayrıştırılır.
- Okunan veri, ileri analiz ve değerlendirme için SQLite veritabanına (vt/10p.db) kaydedilir.
- Modüler ve anlaşılır kod yapısına sahiptir. Hemen her bölüm açıklamalar ile desteklenmiştir.
- Geliştirmeye açıktır.

---

## Proje Yapısı

proje-dizini/
│
├── csv/ 				# İşlenecek CSV dosyaları
├── vt/					# Veritabanı dosyaları
│ └── sema.sql 			# Veritabanı şeması
└── src/				# Proje kaynak dosyaları
│ └── csv_isler.py 		# CSV okuma ve veritabanı işlemleri
│ └── vt_isler.py 		# Veritabanı işlemleri
│ └── dosya_isler.py 	# Dosya işlemleri
│ └── proje.py 			# Projenin ana çalışma dosyası


---

## Kurulum ve Çalıştırma

1. Python 3.7 veya daha yeni bir sürümün yüklü olması önerilir.  
   Python’u [https://www.python.org/downloads/](https://www.python.org/downloads/) adresinden indirebilirsiniz.

2. Projeyi klonlayın veya indirin.

3. CSV dosyalarını csv/ klasörüne yerleştirin.

4. Projeyi şu kod satırı ile çalıştırın:

	python -m src.proje

---

## Lisans

Bu proje MIT Lisansı ile lisanslanmıştır.

## İletişim

Herhangi bir soru veya katkı için bana ulaşabilirsiniz.

## Not

Geliştirme sürecinde Dr. Murat AYDAN'ın kendi öğrencilerine ilişkin kayıtları referans alınmış, tüm kodlama ve testler bu veri üzerinden yine kendisi tarafından yapılmış, veri hiçbir şekilde üçüncü taraflar ile paylaşılmamıştır. Python ile kodlama sürecinde OpenAI ChatGPT yapay zeka asistanından kod ve fikir desteği alınmıştır.