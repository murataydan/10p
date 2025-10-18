-- Gunde en az 30 dk ve ustu calismalar
DROP VIEW IF EXISTS GunlukSure30Ustu;
CREATE VIEW GunlukSure30Ustu AS
SELECT
    kullanici_adi,
    ad_soyad,
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
        o.ad || ' ' || o.soyad AS ad_soyad,
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
    WHERE
        c.dakikalik_net_vurus >= 100 AND c.hata_orani <= 3
    GROUP BY 
        c.kullanici_adi, DATE(c.tarih)
    HAVING 
        SUM(c.sure) >= 30
) AS g
GROUP BY
    g.kullanici_adi
ORDER BY
    calismalar DESC, sure_ortalama DESC, FM_orani DESC;