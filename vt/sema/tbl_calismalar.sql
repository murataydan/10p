-- Calismalar tablosu
DROP TABLE IF EXISTS Calismalar;
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