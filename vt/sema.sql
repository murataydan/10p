-- Mevcut tablo ve görünümler siliniyor
DROP TABLE IF EXISTS Ogrenciler;
DROP TABLE IF EXISTS Calismalar;
DROP VIEW IF EXISTS Sure5_Hata1_EnAz5;
DROP VIEW IF EXISTS Sure5_Hata1_Son30gun;
DROP VIEW IF EXISTS GunlukSure30Ustu;

-- Öğrenciler tablosu
CREATE TABLE Ogrenciler (
    kullanici_adi TEXT PRIMARY KEY,  -- Öğrencinin benzersiz kullanıcı adı (örnek: abc123)
    ad TEXT,                          -- Öğrencinin adı
    soyad TEXT                        -- Öğrencinin soyadı
);

-- Çalışmalar tablosu
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

-- GunlukSure30Ustu: Günlük toplam çalışma süresi 30 dk. ve üstü olanların özeti
CREATE VIEW GunlukSure30Ustu AS
SELECT
    kullanici_adi,
    COUNT(*) AS calismalar,
    MIN(tarih) AS tarih1,
    MAX(tarih) AS tarih2,
    MIN(gunluk_sure) AS sure_en_az,
    MAX(gunluk_sure) AS sure_en_fazla,
    ROUND(AVG(gunluk_sure), 0) AS sure_ortalama,
    (MAX(gunluk_sure) - MIN(gunluk_sure)) AS sure_aciklik,
    FM_sayisi,
    FM_orani,
    DNV_ortalama,
    DNV_dusuk,
    DNV_yuksek,
    DNV_araligi,
    Hata_ortalama
FROM (
    SELECT 
        o.kullanici_adi,
        o.ad,
        o.soyad,
        DATE(c.tarih) AS tarih,
        SUM(c.sure) AS gunluk_sure,
        COUNT(DISTINCT c.metin_no) AS FM_sayisi,
        ROUND(COUNT(DISTINCT c.metin_no)* 1.0 / COUNT(*), 1) AS FM_orani,
        ROUND(AVG(c.dakikalik_net_vurus), 0) AS DNV_ortalama,
        MIN(c.dakikalik_net_vurus) AS DNV_dusuk,
        MAX(c.dakikalik_net_vurus) AS DNV_yuksek,
        MAX(c.dakikalik_net_vurus) - MIN(c.dakikalik_net_vurus) AS DNV_araligi,
        ROUND(AVG(c.hata_orani), 1) AS Hata_ortalama
    FROM 
        Calismalar c
    JOIN 
        Ogrenciler o ON c.kullanici_adi = o.kullanici_adi
    GROUP BY 
        c.kullanici_adi, DATE(c.tarih)
    HAVING 
        SUM(c.sure) >= 30
) AS g
GROUP BY
    g.kullanici_adi;

-- Sure5_Hata1_EnAz5: 5 dk. ve üstü sürede %1'den az hata ile en az 5 çalışma
CREATE VIEW Sure5_Hata1_EnAz5 AS
SELECT
    c.kullanici_adi,
    o.ad || ' ' || o.soyad AS ad_soyad,
    COUNT(*) AS calisma,
    COUNT(DISTINCT c.metin_no) AS FM_sayisi,
    ROUND(COUNT(DISTINCT c.metin_no)* 1.0 / COUNT(*), 1) AS FM_orani,
    ROUND(AVG(c.dakikalik_net_vurus), 0) AS DNV_ortalama,
    MIN(c.dakikalik_net_vurus) AS DNV_dusuk,
    MAX(c.dakikalik_net_vurus) AS DNV_yuksek,
    MAX(c.dakikalik_net_vurus) - MIN(c.dakikalik_net_vurus) AS DNV_araligi,
    ROUND(AVG(c.hata_orani), 1) AS Hata_ortalama
FROM Calismalar c
JOIN Ogrenciler o ON c.kullanici_adi = o.kullanici_adi
WHERE c.sure >= 5 AND c.hata_orani < 1 AND dakikalik_net_vurus >= 100 AND hata_orani <= 3
GROUP BY c.kullanici_adi
HAVING calisma >= 5
ORDER BY DNV_ortalama DESC, Hata_ortalama ASC, FM_orani DESC;

-- Sure5_Hata1_Son1Ay: 5 dk. ve üstü sürede %1'den az hata ile son 30 gündeki çalışmalar
CREATE VIEW Sure5_Hata1_Son30gun AS
SELECT
    c.kullanici_adi,
    o.ad || ' ' || o.soyad AS ad_soyad,
    COUNT(*) AS calisma,
    COUNT(DISTINCT c.metin_no) AS FM_sayisi,
    ROUND(COUNT(DISTINCT c.metin_no)* 1.0 / COUNT(*), 1) AS FM_orani,
    ROUND(AVG(c.dakikalik_net_vurus), 0) AS DNV_ortalama,
    MIN(c.dakikalik_net_vurus) AS DNV_dusuk,
    MAX(c.dakikalik_net_vurus) AS DNV_yuksek,
    MAX(c.dakikalik_net_vurus) - MIN(c.dakikalik_net_vurus) AS DNV_araligi,
    ROUND(AVG(c.hata_orani), 1) AS Hata_ortalama
FROM Calismalar c
JOIN Ogrenciler o ON c.kullanici_adi = o.kullanici_adi
WHERE
    c.sure >= 5 AND c.hata_orani < 1 AND dakikalik_net_vurus >= 100 AND hata_orani <= 3
    AND DATE(c.tarih) >= DATE(
        (SELECT MAX(DATE(tarih)) FROM Calismalar), '-30 days'
    )
GROUP BY c.kullanici_adi
ORDER BY DNV_ortalama DESC, Hata_ortalama ASC, FM_orani DESC;
