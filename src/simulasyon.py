"""
Lojistik Intelligence Network (LIN) - Parametreli Lojistik Sevkiyat Simülasyonu
Görev 3 (G3 - Çok Ajanlı Şirket Programı Sentetik Veri Motoru)
Backend Sorumlusu: Aykut Çakıcı (@Aykuutt)
Duyuru 10 Uyumlu: Dışarıdan dinamik şehir listesi, tarih aralığı, yakıt/fiyat katsayısı ve ağırlık aralığı desteği.
Şema Kaynağı: docs/veri-sozlugu.md (v3.0)
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

VARSAYILAN_SEHIRLER = [
    "Istanbul",
    "Ankara",
    "Izmir",
    "Bursa",
    "Antalya",
    "Adana",
    "Trabzon",
    "Gaziantep"
]

# 8 Temel Şehir arasındaki yaklaşık karayolu mesafeleri (km)
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
    # Matriste doğrudan olmayan ikililer için emniyetli ortalama mesafe
    return 650


def parametreleri_dogrula(
    tohum,
    gun_sayisi,
    gunluk_sevkiyat,
    gecikme_olasiligi,
    iptal_olasiligi,
    sehirler=None,
    baslangic_tarihi_str="2026-11-20",
    fiyat_carpani=1.0,
    min_agirlik=50,
    max_agirlik=10000,
):
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
    if fiyat_carpani <= 0:
        raise ValueError(f"Fiyat çarpanı pozitif olmalıdır. Girilen: {fiyat_carpani}")
    if not isinstance(min_agirlik, int) or not isinstance(max_agirlik, int):
        raise ValueError("Ağırlık sınırları tam sayı olmalıdır.")
    if min_agirlik <= 0 or max_agirlik < min_agirlik:
        raise ValueError(
            f"Geçersiz ağırlık aralığı: min={min_agirlik}, max={max_agirlik}"
        )
    try:
        date.fromisoformat(baslangic_tarihi_str)
    except ValueError as exc:
        raise ValueError(
            f"Başlangıç tarihi ISO YYYY-MM-DD formatında olmalıdır. Girilen: {baslangic_tarihi_str}"
        ) from exc
    if sehirler is not None:
        temiz_sehirler = [s for s in sehirler if s]
        if len(set(temiz_sehirler)) < 2:
            raise ValueError("Simülasyon için en az 2 farklı şehir tanımlanmalıdır.")


def simule_et(
    tohum=42,
    gun_sayisi=60,
    gunluk_sevkiyat=15,
    gecikme_olasiligi=0.15,
    iptal_olasiligi=0.05,
    sehirler=None,
    baslangic_tarihi_str="2026-01-01",
    fiyat_carpani=1.0,
    min_agirlik=50,
    max_agirlik=10000,
    id_oneki="SVK-G3"
):
    """
    Duyuru 10 şartlarına uygun olarak dinamik parametreler ve web kaynaklarıyla eşleşebilen
    sentetik sevkiyat veri seti üretir.
    """
    aktif_sehirler = [s.strip() for s in sehirler if s and s.strip()] if sehirler else VARSAYILAN_SEHIRLER
    parametreleri_dogrula(
        tohum,
        gun_sayisi,
        gunluk_sevkiyat,
        gecikme_olasiligi,
        iptal_olasiligi,
        aktif_sehirler,
        baslangic_tarihi_str=baslangic_tarihi_str,
        fiyat_carpani=fiyat_carpani,
        min_agirlik=min_agirlik,
        max_agirlik=max_agirlik,
    )

    rng = random.Random(tohum)
    baslangic_tarihi = date.fromisoformat(baslangic_tarihi_str)

    zamaninda_olasiligi = 1.0 - gecikme_olasiligi - iptal_olasiligi
    durumlar = ["zamaninda", "gecikmeli", "iptal"]
    durum_olasiliklari = [zamaninda_olasiligi, gecikme_olasiligi, iptal_olasiligi]

    kayitlar = []
    toplam_sayac = 1

    for gun_indeksi in range(gun_sayisi):
        mevcut_tarih = baslangic_tarihi + timedelta(days=gun_indeksi)
        tarih_metni = mevcut_tarih.isoformat()

        for _ in range(gunluk_sevkiyat):
            cikis = rng.choice(aktif_sehirler)
            olasi_varislar = [s for s in aktif_sehirler if s != cikis]
            varis = rng.choice(olasi_varislar)

            mod = rng.choices(MODLAR, weights=MOD_AGIRLIKLARI)[0]
            mesafe = mesafe_getir(cikis, varis)
            if mod == "hava":
                mesafe = round(mesafe * 0.82)

            agirlik = rng.randint(min_agirlik, max_agirlik)

            # Ücret hesabı: baz navlun + mesafe katsayısı * dinamik fiyat/yakıt çarpanı
            temel_ucret = (agirlik * 0.50) + (mesafe * MOD_CARPANI[mod] * 1.60)
            ucret = round(temel_ucret * fiyat_carpani, 2)

            durum = rng.choices(durumlar, weights=durum_olasiliklari)[0]

            if durum == "iptal":
                teslim_suresi = ""
            else:
                hiz = MOD_HIZ_KMH[mod]
                saf_sure = mesafe / hiz
                if durum == "zamaninda":
                    # Operasyonel bekleme ve teslim süresi: saf süre + [2, 6] saat
                    sure_degeri = saf_sure + rng.uniform(2.0, 6.0)
                else:
                    # Gecikmeli sevkiyat: [8, 28] saat ek gecikme
                    sure_degeri = saf_sure + rng.uniform(8.0, 28.0)
                teslim_suresi = f"{round(sure_degeri, 1):.1f}"

            sevkiyat_id = f"{id_oneki}-{toplam_sayac:04d}"
            toplam_sayac += 1

            kayitlar.append([
                sevkiyat_id,
                tarih_metni,
                cikis,
                varis,
                mod,
                agirlik,
                mesafe,
                f"{ucret:.2f}",
                teslim_suresi,
                durum
            ])

    return kayitlar


def dogrula(veri):
    """Üretilen veri setinin docs/veri-sozlugu.md şemasına ve kurallarına uygunluğunu doğrular."""
    if not veri or len(veri) == 0:
        raise ValueError("Doğrulanacak veri kümesi boş olamaz.")

    gorulen_id_kumesi = set()

    for i, satir in enumerate(veri, start=1):
        if len(satir) != len(SEMA_SUTUNLARI):
            raise ValueError(
                f"Satır {i}: Sütun sayısı hatalı. Beklenen {len(SEMA_SUTUNLARI)}, bulunan {len(satir)}: {satir}"
            )

        sid, tarih, cikis, varis, mod, agirlik, mesafe, ucret, sure, durum = satir

        # 1. sevkiyat_id kontrolü
        if not re.fullmatch(r"SVK-[A-Z0-9]+-\d{4,}", sid):
            raise ValueError(f"Satır {i}: Geçersiz sevkiyat_id formatı: {sid}")
        if sid in gorulen_id_kumesi:
            raise ValueError(f"Satır {i}: Tekrarlanan sevkiyat_id: {sid}")
        gorulen_id_kumesi.add(sid)

        # 2. tarih kontrolü
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", tarih):
            raise ValueError(f"Satır {i}: Tarih formatı ISO YYYY-MM-DD olmalıdır: {tarih}")
        try:
            date.fromisoformat(tarih)
        except ValueError as exc:
            raise ValueError(f"Satır {i}: Geçersiz takvim tarihi: {tarih}") from exc

        # 3. şehir kontrolleri
        if cikis == varis:
            raise ValueError(f"Satır {i}: Çıkış ve varış şehri aynı olamaz: {cikis}")

        # 4. taşıma modu kontrolü
        if mod not in MODLAR:
            raise ValueError(f"Satır {i}: Geçersiz taşıma modu: {mod}")

        # 5. ağırlık kontrolü
        if not isinstance(agirlik, int) or agirlik <= 0:
            raise ValueError(f"Satır {i}: Ağırlık pozitif tam sayı olmalıdır: {agirlik}")

        # 6. mesafe kontrolü
        if not isinstance(mesafe, int) or mesafe <= 0:
            raise ValueError(f"Satır {i}: Mesafe pozitif tam sayı olmalıdır: {mesafe}")

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
        description="Görev 3 - Dinamik Parametreli Lojistik Sevkiyat Simülasyonu (LIN Group-B)"
    )
    parser.add_argument("--tohum", "--seed", type=int, default=42, help="Rastgelelik tohumu (varsayılan: 42)")
    parser.add_argument("--gun-sayisi", "--days", type=int, default=7, help="Simüle edilecek toplam gün sayısı (varsayılan: 7)")
    parser.add_argument("--gunluk-sevkiyat", "--daily-shipments", type=int, default=20, help="Günlük ortalama sevkiyat sayısı (varsayılan: 20)")
    parser.add_argument("--gecikme-olasiligi", "--delay-prob", type=float, default=0.15, help="Gecikme olasılığı (varsayılan: 0.15)")
    parser.add_argument("--iptal-olasiligi", "--cancel-prob", type=float, default=0.05, help="İptal olasılığı (varsayılan: 0.05)")
    parser.add_argument("--sehirler", type=str, default=None, help="Virgülle ayrılmış şehir listesi (örn: 'Istanbul,Ankara,Izmir,Trabzon')")
    parser.add_argument("--baslangic-tarihi", type=str, default="2026-11-20", help="Simülasyon başlangıç tarihi YYYY-MM-DD (varsayılan: 2026-11-20)")
    parser.add_argument("--fiyat-carpani", type=float, default=1.0, help="Akaryakıt/fiyat katsayısı (varsayılan: 1.0)")
    parser.add_argument("--min-agirlik", type=int, default=50, help="Minimum yük ağırlığı kg (varsayılan: 50)")
    parser.add_argument("--max-agirlik", type=int, default=10000, help="Maksimum yük ağırlığı kg (varsayılan: 10000)")
    parser.add_argument("--id-oneki", type=str, default="SVK-G3", help="Sevkiyat ID öneki (varsayılan: SVK-G3)")
    parser.add_argument("--cikti-dosyasi", "--output", type=str, default=None, help="Çıktı CSV dosya yolu")

    args = parser.parse_args()

    sehir_listesi = [s.strip() for s in args.sehirler.split(",") if s.strip()] if args.sehirler else None

    # Veriyi üret
    veri = simule_et(
        tohum=args.tohum,
        gun_sayisi=args.gun_sayisi,
        gunluk_sevkiyat=args.gunluk_sevkiyat,
        gecikme_olasiligi=args.gecikme_olasiligi,
        iptal_olasiligi=args.iptal_olasiligi,
        sehirler=sehir_listesi,
        baslangic_tarihi_str=args.baslangic_tarihi,
        fiyat_carpani=args.fiyat_carpani,
        min_agirlik=args.min_agirlik,
        max_agirlik=args.max_agirlik,
        id_oneki=args.id_oneki,
    )

    # Veriyi doğrula
    dogrula(veri)

    # Hedef dosya yolunu belirle
    if args.cikti_dosyasi:
        hedef_yol = os.path.abspath(args.cikti_dosyasi)
    else:
        kok_dizin = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        hedef_yol = os.path.join(kok_dizin, "data", "lojistik_sevkiyat_g3_ornek.csv")

    os.makedirs(os.path.dirname(hedef_yol), exist_ok=True)

    with open(hedef_yol, "w", newline="", encoding="utf-8") as f:
        yazici = csv.writer(f)
        yazici.writerow(SEMA_SUTUNLARI)
        yazici.writerows(veri)

    print(f"[OK] G3 Simulasyon tamamlandi: {len(veri)} satir basariyla yazildi -> {hedef_yol}")


if __name__ == "__main__":
    main()
