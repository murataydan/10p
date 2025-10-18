-- Son 30 gun icinde yapilan calismalar
DROP VIEW IF EXISTS Sure5_Hata1_Son30gun;
CREATE VIEW Sure5_Hata1_Son30gun AS
SELECT
    c.kullanici_adi,
    o.ad || ' ' || o.soyad AS ad_soyad,
    COUNT(*) AS calisma,
    COUNT(DISTINCT c.metin_no) AS FM_sayisi,
    ROUND(COUNT(DISTINCT c.metin_no)* 1.0 / COUNT(*), 1) AS FM_orani,
    ROUND(AVG(c.dakikalik_net_vurus), 0) AS DNV_ortalama,
    MIN(c.dakikalik_net_vurus) AS DNV_dusuk,
    MAX(c.dakalik_net_vurus) AS DNV_yuksek,
    MAX(c.dakalik_net_vurus) - MIN(c.dakalik_net_vurus) AS DNV_araligi,
    ROUND(AVG(c.hata_orani), 1) AS Hata_ortalama
FROM Calismalar c
JOIN Ogrenciler o ON c.kullanici_adi = o.kullanici_adi
WHERE
    c.sure >= 5 AND c.hata_orani < 1 AND dakikalik_net_vurus >= 100 AND hata_orani <= 3
    AND DATE(c.tarih) >= DATE((SELECT MAX(DATE(tarih)) FROM Calismalar), '-30 days')
GROUP BY c.kullanici_adi
ORDER BY DNV_ortalama DESC, Hata_ortalama ASC, FM_orani DESC;