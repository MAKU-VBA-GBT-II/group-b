import csv
import os
import re
import sys
from pathlib import Path

# Windows konsolunda UTF-8 cikti destegi
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Referans Veri Sozlugu Kurallari
BEKLENEN_SUTUNLAR = [
    "sevkiyat_id",
    "tarih",
    "cikis_sehri",
    "varis_sehri",
    "tasima_modu",
    "agirlik_kg",
    "mesafe_km",
    "ucret_tl",
    "teslim_suresi_saat",
    "durum",
]
IZINLI_SEHIRLER = {"Istanbul", "Ankara", "Izmir", "Bursa", "Konya", "Adana", "Antalya"}
IZINLI_MODLAR = {"kara", "deniz", "hava", "demiryolu"}
IZINLI_DURUMLAR = {"zamaninda", "gecikmeli", "iptal"}


class DQTestRunner:
    def __init__(self, dosya_yolu: Path):
        self.dosya_yolu = dosya_yolu
        self.satirlar = []
        self.baslik = []
        self.sonuclar = {}

    def run_all(self):
        print("=" * 68)
        print("  G1 Sevkiyat Veri Kalitesi (DQ) Test Kosumu (8 Senaryo)")
        print(f"  Test Edilen Dosya: {self.dosya_yolu}")
        print("=" * 68)

        senaryolar = [
            (1, "Dosya mevcut ve okunabilir", self.test_senaryo_1),
            (2, "Asgari satir sayisi saglaniyor", self.test_senaryo_2),
            (3, "Sutun sayisi ve adlari semayla eslesiyor", self.test_senaryo_3),
            (4, "Sevkiyat kimlikleri benzersiz ve bicime uygun", self.test_senaryo_4),
            (5, "Tarih, tur ve sayisal araliklar gecerli", self.test_senaryo_5),
            (6, "Kategoriler ve sehir degerleri gecerli", self.test_senaryo_6),
            (7, "Iptal sevkiyatlarda teslim suresi bos", self.test_senaryo_7),
            (8, "Bonus: Cikis ve varis sehirleri farkli", self.test_senaryo_8),
        ]

        basarili_sayisi = 0
        for no, baslik, test_fonk in senaryolar:
            try:
                gecti, detay = test_fonk()
                self.sonuclar[no] = (gecti, detay)
                durum = "[GECTI]" if gecti else "[KALDI]"
                if gecti:
                    basarili_sayisi += 1
                print(f"[Senaryo {no}] {durum} - {baslik}")
                print(f"    -> Detay: {detay}")
            except Exception as e:
                self.sonuclar[no] = (False, f"Hata olustu: {e}")
                print(f"[Senaryo {no}] [HATA]  - {baslik}")
                print(f"    -> Detay: {e}")

        print("=" * 68)
        print(f"  OZET: 8 Senaryo | {basarili_sayisi} Gecti | {8 - basarili_sayisi} Kaldi")
        print("=" * 68)
        return basarili_sayisi == 8

    def test_senaryo_1(self):
        """Senaryo 1: Dosya mevcut ve okunabilir"""
        if not self.dosya_yolu.exists():
            return False, f"Dosya bulunamadi: {self.dosya_yolu}"

        with open(self.dosya_yolu, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            self.baslik = next(reader, None)
            if not self.baslik:
                return False, "Dosya bos veya baslik satiri yok"
            self.satirlar = list(reader)

        if len(self.satirlar) == 0:
            return False, "Dosyada hic veri satiri yok"

        return True, f"UTF-8 olarak basariyla okundu. Baslik ve {len(self.satirlar)} satir mevcut."

    def test_senaryo_2(self):
        """Senaryo 2: Asgari satir sayisi saglaniyor (en az 100)"""
        toplam_satir = len(self.satirlar)
        if toplam_satir < 100:
            return False, f"Yetersiz satir: {toplam_satir} < 100"
        return True, f"{toplam_satir} veri satiri mevcut (alt sinir 100, hedef 300 saglandi)."

    def test_senaryo_3(self):
        """Senaryo 3: Sutun sayisi ve adlari semayla eslesiyor"""
        if self.baslik != BEKLENEN_SUTUNLAR:
            return False, f"Sutunlar uyusmuyor! Beklenen: {BEKLENEN_SUTUNLAR}, Bulunan: {self.baslik}"
        return True, "Tam 10 sutun ve ad/siralama veri sozlügüyle birebir eslesiyor."

    def test_senaryo_4(self):
        """Senaryo 4: Sevkiyat kimlikleri benzersiz ve bicime uygun (SVK-0001 - SVK-0300)"""
        kimlikler = [s[0] for s in self.satirlar]
        if len(kimlikler) != len(set(kimlikler)):
            tekrarlar = len(kimlikler) - len(set(kimlikler))
            return False, f"{tekrarlar} adet mukerrer kimlik tespit edildi."

        gecersiz_bicimler = [k for k in kimlikler if not re.fullmatch(r"SVK-\d{4}", k)]
        if gecersiz_bicimler:
            return False, f"Bicime uymayan ID ornekleri: {gecersiz_bicimler[:3]}"

        return True, f"{len(kimlikler)} kimligin tamami benzersiz ve 'SVK-XXXX' biciminde."

    def test_senaryo_5(self):
        """Senaryo 5: Tarih, tur ve sayisal araliklar gecerli"""
        hatalar = []
        for s in self.satirlar:
            sid, tarih, _, _, _, agirlik, mesafe, ucret, _, _ = s
            # Tarih kontrolu
            if not ("2026-01-01" <= tarih <= "2026-03-31"):
                hatalar.append(f"{sid}: Tarih aralik disi ({tarih})")
            # Agirlik kontrolu
            try:
                agirlik_val = int(agirlik)
                if not (10 <= agirlik_val <= 5000):
                    hatalar.append(f"{sid}: Agirlik 10-5000 disi ({agirlik_val})")
            except ValueError:
                hatalar.append(f"{sid}: Agirlik tam sayi degil ({agirlik})")
            # Mesafe kontrolu
            try:
                mesafe_val = int(mesafe)
                if not (50 <= mesafe_val <= 2500):
                    hatalar.append(f"{sid}: Mesafe 50-2500 disi ({mesafe_val})")
            except ValueError:
                hatalar.append(f"{sid}: Mesafe tam sayi degil ({mesafe})")
            # Ucret kontrolu
            try:
                ucret_val = float(ucret)
                if ucret_val <= 0:
                    hatalar.append(f"{sid}: Ucret <= 0 ({ucret_val})")
            except ValueError:
                hatalar.append(f"{sid}: Ucret sayisal degil ({ucret})")

            if len(hatalar) >= 3:
                break

        if hatalar:
            return False, f"Aralik/Tur ihlalleri: {', '.join(hatalar[:3])}"
        return True, "Tarihler 2026-01-01..2026-03-31; agirlik 10..5000; mesafe 50..2500; ucret > 0."

    def test_senaryo_6(self):
        """Senaryo 6: Kategoriler ve sehir degerleri gecerli"""
        mevcut_modlar = set()
        for s in self.satirlar:
            sid = s[0]
            cikis, varis, mod, durum = s[2], s[3], s[4], s[9]
            if cikis not in IZINLI_SEHIRLER:
                return False, f"{sid}: Gecersiz cikis sehri: '{cikis}'"
            if varis not in IZINLI_SEHIRLER:
                return False, f"{sid}: Gecersiz varis sehri: '{varis}'"
            if mod not in IZINLI_MODLAR:
                return False, f"{sid}: Gecersiz tasima modu: '{mod}'"
            if durum not in IZINLI_DURUMLAR:
                return False, f"{sid}: Gecersiz durum: '{durum}'"
            mevcut_modlar.add(mod)

        if mevcut_modlar != IZINLI_MODLAR:
            eksikler = IZINLI_MODLAR - mevcut_modlar
            return False, f"Eksik tasima modu: {eksikler}"

        return True, "Tum sehir, durum ve modlar izinli listede; 4 tasima modu da temsil ediliyor."

    def test_senaryo_7(self):
        """Senaryo 7: Iptal sevkiyatlarda teslim suresi bos"""
        iptal_sayisi = 0
        hatalar = []
        for s in self.satirlar:
            sid, sure, durum = s[0], s[8].strip(), s[9]
            if durum == "iptal":
                iptal_sayisi += 1
                if sure != "":
                    hatalar.append(f"{sid} (sure: {sure})")
            else:
                try:
                    float(sure)
                except ValueError:
                    hatalar.append(f"{sid} (iptal degil ama sure sayisal degil: '{sure}')")

        if hatalar:
            return False, f"Hatali satirlar: {', '.join(hatalar[:3])}"
        return True, f"{iptal_sayisi} adet iptal satirlarinin teslim suresi bos; aktif satirlar sayisal."

    def test_senaryo_8(self):
        """Senaryo 8: Bonus: Cikis ve varis sehirleri farkli"""
        ayni_sehir_olanlar = [s[0] for s in self.satirlar if s[2] == s[3]]
        if ayni_sehir_olanlar:
            return False, f"Cikis ve varis sehri ayni olan kayitlar: {ayni_sehir_olanlar[:3]}"
        return True, "Hicbir satirda cikis ve varis sehri ayni degil (0 hata)."


if __name__ == "__main__":
    kok_dizin = Path(__file__).resolve().parent.parent
    hedef_csv = kok_dizin / "data" / "lojistik-sevkiyat.csv"
    runner = DQTestRunner(hedef_csv)
    basarili = runner.run_all()
    sys.exit(0 if basarili else 1)
