"""
Lojistik Intelligence Network (LIN) - Parametreli Lojistik Sevkiyat Simülasyonu
Görev 2 (G2-veri, Issue #47)
Backend Geliştirici: Aykut Çakıcı (@Aykuutt)
Şema Kaynağı: docs/veri-sozlugu.md
"""

import argparse
import csv
import os
import random
import re
import sys
from datetime import date, timedelta

# Sabit Şema Tanımları
SEMA_SUTUNLARI = [
    "sevkiyat_id",
    "tarih",
    "cikis_sehri",
    "varis_sehri",
    "tasima_modu",
    "agirlik_kg",
    "mesafe_km",
    "ucret_tl",
    "teslim_suresi_saat",
    "durum"
]

SEHIRLER = [
    "Istanbul",
    "Ankara",
    "Izmir",
    "Bursa",
    "Antalya",
    "Adana",
    "Trabzon",
    "Gaziantep"
]

# 8 Şehir arasındaki yaklaşık karayolu mesafeleri (km)
MESAFE_MATRISI = {
    ("Istanbul", "Ankara"): 450,
    ("Istanbul", "Izmir"): 480,
    ("Istanbul", "Bursa"): 155,
    ("Istanbul", "Antalya"): 700,
    ("Istanbul", "Adana"): 935,
    ("Istanbul", "Trabzon"): 1065,
    ("Istanbul", "Gaziantep"): 1140,
    ("Ankara", "Izmir"): 590,
    ("Ankara", "Bursa"): 385,
    ("Ankara", "Antalya"): 480,
    ("Ankara", "Adana"): 490,
    ("Ankara", "Trabzon"): 735,
    ("Ankara", "Gaziantep"): 675,
    ("Izmir", "Bursa"): 330,
    ("Izmir", "Antalya"): 460,
    ("Izmir", "Adana"): 900,
    ("Izmir", "Trabzon"): 1310,
    ("Izmir", "Gaziantep"): 1110,
    ("Bursa", "Antalya"): 545,
    ("Bursa", "Adana"): 835,
    ("Bursa", "Trabzon"): 1025,
    ("Bursa", "Gaziantep"): 1040,
    ("Antalya", "Adana"): 565,
    ("Antalya", "Trabzon"): 1205,
    ("Antalya", "Gaziantep"): 805,
    ("Adana", "Trabzon"): 875,
    ("Adana", "Gaziantep"): 220,
    ("Trabzon", "Gaziantep"): 755,
}

MODLAR = ["kara", "deniz", "hava", "demiryolu"]
MOD_AGIRLIKLARI = [50, 15, 15, 20]

# Mod katsayıları ve operasyonel hızları
MOD_CARPANI = {
    "kara": 1.00,
    "demiryolu": 0.75,
    "deniz": 0.60,
    "hava": 2.50
}

MOD_HIZ_KMH = {
    "kara": 65,
    "demiryolu": 50,
    "deniz": 30,
    "hava": 550
}


def mesafe_getir(sehir_a, sehir_b):
    """İki şehir arasındaki karayolu mesafesini simetrik olarak döndürür."""
    if sehir_a == sehir_b:
        raise ValueError(f"Çıkış ve varış şehri aynı olamaz: {sehir_a}")
    if (sehir_a, sehir_b) in MESAFE_MATRISI:
        return MESAFE_MATRISI[(sehir_a, sehir_b)]
    if (sehir_b, sehir_a) in MESAFE_MATRISI:
        return MESAFE_MATRISI[(sehir_b, sehir_a)]
    return 600  # Varsayılan emniyet mesafesi


def parametreleri_dogrula(tohum, gun_sayisi, gunluk_sevkiyat, gecikme_olasiligi, iptal_olasiligi):
    """Girdi parametrelerinin geçerlilik aralıklarını kontrol eder."""
    if not isinstance(tohum, int):
        raise ValueError(f"Tohum tam sayı olmalıdır. Girilen: {tohum}")
    if not isinstance(gun_sayisi, int) or gun_sayisi <= 0:
        raise ValueError(f"Gün sayısı pozitif tam sayı olmalıdır. Girilen: {gun_sayisi}")
    if not isinstance(gunluk_sevkiyat, int) or gunluk_sevkiyat <= 0:
        raise ValueError(f"Günlük sevkiyat pozitif tam sayı olmalıdır. Girilen: {gunluk_sevkiyat}")
    if not (0.0 <= gecikme_olasiligi <= 1.0):
        raise ValueError(f"Gecikme olasılığı 0.0 ile 1.0 arasında olmalıdır. Girilen: {gecikme_olasiligi}")
    if not (0.0 <= iptal_olasiligi <= 1.0):
        raise ValueError(f"İptal olasılığı 0.0 ile 1.0 arasında olmalıdır. Girilen: {iptal_olasiligi}")
    if gecikme_olasiligi + iptal_olasiligi >= 1.0:
        raise ValueError(
            f"Gecikme ve iptal olasılıkları toplamı 1.0'dan küçük olmalıdır. "
            f"Toplam: {gecikme_olasiligi + iptal_olasiligi}"
        )


def simule_et(tohum=42, gun_sayisi=60, gunluk_sevkiyat=15, gecikme_olasiligi=0.15, iptal_olasiligi=0.05):
    """
    Parametrelere ve docs/veri-sozlugu.md şemasına göre sentetik sevkiyat verisi üretir.
    """
    parametreleri_dogrula(tohum, gun_sayisi, gunluk_sevkiyat, gecikme_olasiligi, iptal_olasiligi)

    rng = random.Random(tohum)
    baslangic_tarihi = date(2026, 1, 1)

    zamaninda_olasiligi = 1.0 - gecikme_olasiligi - iptal_olasiligi
    durumlar = ["zamaninda", "gecikmeli", "iptal"]
    durum_olasiliklari = [zamaninda_olasiligi, gecikme_olasiligi, iptal_olasiligi]

    kayitlar = []

    for gun_indeksi in range(gun_sayisi):
        mevcut_tarih = baslangic_tarihi + timedelta(days=gun_indeksi)
        tarih_metni = mevcut_tarih.isoformat()

        for _ in range(gunluk_sevkiyat):
            cikis = rng.choice(SEHIRLER)
            olasi_varislar = [s for s in SEHIRLER if s != cikis]
            varis = rng.choice(olasi_varislar)

            mod = rng.choices(MODLAR, weights=MOD_AGIRLIKLARI)[0]
            mesafe = mesafe_getir(cikis, varis)
            if mod == "hava":
                # Hava taşımacılığında direkt uçuş katsayısı (%85)
                mesafe = round(mesafe * 0.85)

            agirlik = rng.randint(50, 10000)

            # Formül: (agirlik_kg * 0.50) + (mesafe_km * mod_carpani * 1.6)
            ucret = (agirlik * 0.50) + (mesafe * MOD_CARPANI[mod] * 1.6)
            ucret_metin = f"{ucret:.2f}"

            durum = rng.choices(durumlar, weights=durum_olasiliklari)[0]

            if durum == "iptal":
                sure_metin = ""
            else:
                hiz = MOD_HIZ_KMH[mod]
                sure = (mesafe / hiz) + rng.uniform(2.0, 8.0)
                if durum == "gecikmeli":
                    sure += rng.uniform(6.0, 36.0)
                sure_metin = f"{round(sure, 1):.1f}"

            kayitlar.append([
                tarih_metni,
                cikis,
                varis,
                mod,
                agirlik,
                mesafe,
                ucret_metin,
                sure_metin,
                durum
            ])

    # Tarihe göre sırala
    kayitlar.sort(key=lambda x: x[0])

    # SVK-G2-0001 formatında benzersiz ID'leri ekle
    sonuc = []
    for i, satir in enumerate(kayitlar, start=1):
        sid = f"SVK-G2-{i:04d}"
        sonuc.append([sid] + satir)

    return sonuc


def dogrula(veri):
    """
    Üretilen verinin docs/veri-sozlugu.md kurallarına tam uyumunu denetler.
    Herhangi bir ihlalde ValueError fırlatır.
    """
    if not veri:
        raise ValueError("Üretilen veri kümesi boş olamaz.")

    if len(veri) < 100:
        raise ValueError(f"G2 için en az 100 satır veri gereklidir. Mevcut: {len(veri)}")

    gorulen_id_kumesi = set()
    sehir_seti = set(SEHIRLER)

    for i, satir in enumerate(veri, start=1):
        if len(satir) != len(SEMA_SUTUNLARI):
            raise ValueError(
                f"Satır {i}: Sütun sayısı hatalı. Beklenen {len(SEMA_SUTUNLARI)}, bulunan {len(satir)}: {satir}"
            )

        sid, tarih, cikis, varis, mod, agirlik, mesafe, ucret, sure, durum = satir

        # 1. sevkiyat_id kontrolü
        if not re.fullmatch(r"SVK-G2-\d{4,}", sid):
            raise ValueError(f"Satır {i}: Geçersiz sevkiyat_id formatı: {sid}")
        if sid in gorulen_id_kumesi:
            raise ValueError(f"Satır {i}: Tekrarlanan sevkiyat_id: {sid}")
        gorulen_id_kumesi.add(sid)

        # 2. tarih kontrolü
        if not re.fullmatch(r"2026-\d{2}-\d{2}", tarih):
            raise ValueError(f"Satır {i}: Tarih formatı ISO YYYY-MM-DD olmalıdır: {tarih}")

        # 3. şehir kontrolleri
        if cikis not in sehir_seti:
            raise ValueError(f"Satır {i}: Geçersiz çıkış şehri: {cikis}")
        if varis not in sehir_seti:
            raise ValueError(f"Satır {i}: Geçersiz varış şehri: {varis}")
        if cikis == varis:
            raise ValueError(f"Satır {i}: Çıkış ve varış şehri aynı olamaz: {cikis}")

        # 4. taşıma modu kontrolü
        if mod not in MODLAR:
            raise ValueError(f"Satır {i}: Geçersiz taşıma modu: {mod}")

        # 5. ağırlık kontrolü
        if not isinstance(agirlik, int) or not (50 <= agirlik <= 10000):
            raise ValueError(f"Satır {i}: Ağırlık 50 ile 10000 arasında tam sayı olmalıdır: {agirlik}")

        # 6. mesafe kontrolü
        if not isinstance(mesafe, int) or not (100 <= mesafe <= 1800):
            raise ValueError(f"Satır {i}: Mesafe 100 ile 1800 arasında pozitif tam sayı olmalıdır: {mesafe}")

        # 7. ücret kontrolü
        if not re.fullmatch(r"\d+\.\d{2}", ucret):
            raise ValueError(f"Satır {i}: Ücret tam 2 ondalık basamaklı olmalıdır: {ucret}")
        if float(ucret) <= 0:
            raise ValueError(f"Satır {i}: Ücret pozitif olmalıdır: {ucret}")

        # 8. durum ve süre kontrolü
        if durum not in ["zamaninda", "gecikmeli", "iptal"]:
            raise ValueError(f"Satır {i}: Geçersiz durum değeri: {durum}")

        if durum == "iptal":
            if sure != "":
                raise ValueError(f"Satır {i}: İptal durumundaki sevkiyatın teslim süresi boş olmalıdır: '{sure}'")
        else:
            if not re.fullmatch(r"\d+\.\d", sure):
                raise ValueError(f"Satır {i}: Teslim süresi tam 1 ondalık basamaklı olmalıdır: '{sure}'")
            if float(sure) <= 0:
                raise ValueError(f"Satır {i}: Teslim süresi pozitif olmalıdır: {sure}")

    print(f"[OK] Dogrulama basarili: {len(veri)} satir kural kontrolunden gecti.")


def main():
    parser = argparse.ArgumentParser(
        description="Görev 2 - Parametreli Lojistik Sevkiyat Simülasyonu (LIN Group-B)"
    )
    parser.add_argument(
        "--tohum", "--seed",
        type=int,
        default=42,
        help="Rastgelelik tohumu (varsayılan: 42)"
    )
    parser.add_argument(
        "--gun-sayisi", "--days",
        type=int,
        default=60,
        help="Simüle edilecek toplam gün sayısı (varsayılan: 60)"
    )
    parser.add_argument(
        "--gunluk-sevkiyat", "--daily-shipments",
        type=int,
        default=15,
        help="Günlük ortalama sevkiyat sayısı (varsayılan: 15)"
    )
    parser.add_argument(
        "--gecikme-olasiligi", "--delay-prob",
        type=float,
        default=0.15,
        help="Gecikme olasılığı (varsayılan: 0.15)"
    )
    parser.add_argument(
        "--iptal-olasiligi", "--cancel-prob",
        type=float,
        default=0.05,
        help="İptal olasılığı (varsayılan: 0.05)"
    )
    parser.add_argument(
        "--cikti-dosyasi", "--output",
        type=str,
        default=None,
        help="Çıktı CSV dosya yolu (varsayılan: data/lojistik_sevkiyat_g2.csv)"
    )

    args = parser.parse_args()

    # Veriyi üret
    veri = simule_et(
        tohum=args.tohum,
        gun_sayisi=args.gun_sayisi,
        gunluk_sevkiyat=args.gunluk_sevkiyat,
        gecikme_olasiligi=args.gecikme_olasiligi,
        iptal_olasiligi=args.iptal_olasiligi
    )

    # Veriyi doğrula
    dogrula(veri)

    # Hedef dosya yolunu belirle
    if args.cikti_dosyasi:
        hedef_yol = os.path.abspath(args.cikti_dosyasi)
    else:
        kok_dizin = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        hedef_yol = os.path.join(kok_dizin, "data", "lojistik_sevkiyat_g2.csv")

    os.makedirs(os.path.dirname(hedef_yol), exist_ok=True)

    with open(hedef_yol, "w", newline="", encoding="utf-8") as f:
        yazici = csv.writer(f)
        yazici.writerow(SEMA_SUTUNLARI)
        yazici.writerows(veri)

    print(f"[OK] Simulasyon tamamlandi: {len(veri)} satir basariyla yazildi -> {hedef_yol}")


if __name__ == "__main__":
    main()
