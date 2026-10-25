import csv
import os
import random
import re
from datetime import date, timedelta

TOHUM = 42
SATIR_SAYISI = 300

# Sehir ciftleri ve yaklasik karayolu mesafeleri (km)
ROTALAR = [
    ("Istanbul", "Ankara", 450),
    ("Istanbul", "Izmir", 480),
    ("Istanbul", "Bursa", 150),
    ("Ankara", "Izmir", 590),
    ("Ankara", "Konya", 260),
    ("Ankara", "Adana", 490),
    ("Izmir", "Antalya", 460),
    ("Bursa", "Izmir", 330),
]

MODLAR = ["kara", "deniz", "hava", "demiryolu"]
MOD_AGIRLIK = [50, 15, 15, 20]
HIZ_KMH = {"kara": 60, "deniz": 25, "hava": 600, "demiryolu": 50}
KATSAYI = {"kara": 0.004, "deniz": 0.002, "hava": 0.02, "demiryolu": 0.003}
DURUMLAR = ["zamaninda", "gecikmeli", "iptal"]
DURUM_AGIRLIK = [75, 20, 5]

BASLIK = ["sevkiyat_id", "tarih", "cikis_sehri", "varis_sehri", "tasima_modu",
          "agirlik_kg", "mesafe_km", "ucret_tl", "teslim_suresi_saat", "durum"]


def uret(satir_sayisi=SATIR_SAYISI, tohum=TOHUM):
    rng = random.Random(tohum)
    baslangic = date(2026, 1, 1)
    satirlar = []
    for _ in range(satir_sayisi):
        a, b, mesafe = rng.choice(ROTALAR)
        if rng.random() < 0.5:
            a, b = b, a
        mod = rng.choices(MODLAR, weights=MOD_AGIRLIK)[0]
        if mod == "hava":
            mesafe = round(mesafe * 0.85)
        agirlik = rng.randint(10, 5000)
        ucret = round(agirlik * mesafe * KATSAYI[mod], 2)
        sure = mesafe / HIZ_KMH[mod] + rng.uniform(2, 12)
        durum = rng.choices(DURUMLAR, weights=DURUM_AGIRLIK)[0]
        if durum == "gecikmeli":
            sure += rng.uniform(6, 48)
        # Iptal edilen sevkiyatta teslim suresi bos birakilir
        sure_metin = "" if durum == "iptal" else f"{round(sure, 1):.1f}"
        ucret_metin = f"{ucret:.2f}"
        tarih = baslangic + timedelta(days=rng.randint(0, 89))
        satirlar.append([tarih.isoformat(), a, b, mod, agirlik, mesafe,
                         ucret_metin, sure_metin, durum])
    satirlar.sort(key=lambda s: s[0])
    return [[f"SVK-{i + 1:04d}"] + s for i, s in enumerate(satirlar)]


def dogrula(veri):
    """Sozluk kurallarini dosya yazilmadan once kontrol eder; hata varsa durur."""
    if len(veri) < 100:
        raise ValueError("En az 100 satir gerekli")
    if len({s[4] for s in veri}) < 4:
        raise ValueError("tasima_modu'nda en az 4 farkli deger gerekli")
    kimlikler = set()
    for s in veri:
        sid, tarih, cikis, varis, mod, agirlik, mesafe, ucret, sure, durum = s
        if sid in kimlikler:
            raise ValueError(f"Tekrarlanan sevkiyat_id: {sid}")
        kimlikler.add(sid)
        if not "2026-01-01" <= tarih <= "2026-03-31":
            raise ValueError(f"Tarih aralik disi: {sid}")
        if cikis == varis:
            raise ValueError(f"Cikis ve varis sehri ayni: {sid}")
        if not 10 <= agirlik <= 5000:
            raise ValueError(f"agirlik_kg aralik disi: {sid}")
        if not re.fullmatch(r"\d+\.\d{2}", ucret):
            raise ValueError(f"ucret_tl 2 ondalikli degil: {sid}")
        if durum == "iptal" and sure != "":
            raise ValueError(f"Iptalde teslim suresi bos olmali: {sid}")
        if durum != "iptal" and not re.fullmatch(r"\d+\.\d", sure):
            raise ValueError(f"teslim_suresi_saat 1 ondalikli degil: {sid}")


def main():
    veri = uret()
    dogrula(veri)
    klasor = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
    os.makedirs(klasor, exist_ok=True)
    yol = os.path.join(klasor, "lojistik-sevkiyat.csv")
    with open(yol, "w", newline="", encoding="utf-8") as f:
        yazici = csv.writer(f)
        yazici.writerow(BASLIK)
        yazici.writerows(veri)
    print(f"{len(veri)} satir yazildi: {yol}")


if __name__ == "__main__":
    main()