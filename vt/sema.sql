-- Eğer Ogrenciler tablosu daha önceden varsa silinir
DROP TABLE IF EXISTS Ogrenciler;

-- Eğer Calismalar tablosu daha önceden varsa silinir
DROP TABLE IF EXISTS Calismalar;

-- Öğrencilerin temel bilgilerini saklayan tablo
CREATE TABLE Ogrenciler (
    kullanici_adi TEXT PRIMARY KEY,  -- Öğrencinin benzersiz kullanıcı adı (örn: (abc123))
    ad TEXT,                          -- Öğrencinin adı
    soyad TEXT                        -- Öğrencinin soyadı
);

-- Öğrencilerin yaptığı çalışmaların kaydedileceği tablo
CREATE TABLE Calismalar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Otomatik artan benzersiz ID
    kullanici_adi TEXT,                    -- Öğrenciyle ilişki kurmak için kullanıcı adı (foreign key)
    sn INTEGER,                            -- Çalışma sıra numarası
    tarih TEXT,                            -- Çalışmanın yapıldığı tarih (metin formatında)
    metin_no INTEGER,                      -- Hangi metinle çalışıldığı (numara)
    sure INTEGER,                          -- Süre (saniye veya dakika)
    toplam_vurus INTEGER,                 -- Toplam tuş vuruşu
    toplam_net_vurus INTEGER,             -- Hatalar çıkarıldığında kalan net vuruş
    dakikalik_net_vurus INTEGER,          -- Dakika başına net vuruş
    hata_sayisi INTEGER,                   -- Yapılan hata sayısı
    hata_orani REAL,                       -- Hatalı yazım oranı (yüzde)
    kelime_sayisi INTEGER,                 -- Doğru yazılmış kelime sayısı
    katiplik_kelime_sayisi INTEGER,        -- Katiplik modunda yazılan kelime sayısı

    -- kullanici_adi, Ogrenciler tablosundaki bir kayda referans verir
    FOREIGN KEY (kullanici_adi) REFERENCES Ogrenciler(kullanici_adi)
);
