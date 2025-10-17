-- Mevcut tablo ve görünümleri sil
DROP TABLE IF EXISTS Ogrenciler;
DROP TABLE IF EXISTS Calismalar;
DROP VIEW IF EXISTS Sure5_Hata1_EnAz5;

-- Öğrencilerin temel bilgilerini saklayan tablo
CREATE TABLE Ogrenciler (
    kullanici_adi TEXT PRIMARY KEY,  -- Öğrencinin benzersiz kullanıcı adı (örnek: abc123)
    ad TEXT,                          -- Öğrencinin adı
    soyad TEXT                        -- Öğrencinin soyadı
);

-- Öğrencilerin yaptığı çalışmaların kaydedileceği tablo
CREATE TABLE Calismalar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kullanici_adi TEXT,
    sn INTEGER,
    tarih TEXT,
    metin_no INTEGER,
    sure INTEGER,
    toplam_vurus INTEGER,
    toplam_net_vurus INTEGER,
    dakikalik_net_vurus INTEGER,
    hata_sayisi INTEGER,
    hata_orani REAL,
    kelime_sayisi INTEGER,
    katiplik_kelime_sayisi INTEGER,
    FOREIGN KEY (kullanici_adi) REFERENCES Ogrenciler(kullanici_adi)
);

-- 5 dk. ve üstü sürede %1'den az hata ile en az 5 çalışması bulunan öğrenciler
CREATE VIEW Sure5_Hata1_EnAz5 AS
SELECT
    c.kullanici_adi,
    o.ad || ' ' || o.soyad AS ad_soyad,
    COUNT(*) AS calisma_sayisi,
    ROUND(AVG(c.dakikalik_net_vurus), 2) AS ortalama_dakikalik_net_vurus,
    MIN(c.dakikalik_net_vurus) AS en_dusuk_dakikalik_net_vurus,
    MAX(c.dakikalik_net_vurus) AS en_yuksek_dakikalik_net_vurus,
    ROUND(AVG(c.hata_orani), 2) AS ortalama_hata_orani
FROM Calismalar c
JOIN Ogrenciler o ON c.kullanici_adi = o.kullanici_adi
WHERE c.sure >= 5 AND c.hata_orani < 1
GROUP BY c.kullanici_adi
HAVING COUNT(*) >= 5
ORDER BY ortalama_dakikalik_net_vurus DESC, ortalama_hata_orani ASC, calisma_sayisi DESC;