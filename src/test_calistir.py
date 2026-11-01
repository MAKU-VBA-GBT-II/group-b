#!/usr/bin/env python3
"""
Görev 2: Lojistik Sevkiyat Veri Kalitesi Otomatik Test Koşucu Betiği
Rol: DQ (Data Quality) — Ece Naz Aktürk
Referans: tests/test-cases.md, docs/veri-sozlugu.md v2.0
Dosya: data/lojistik_sevkiyat_g2.csv
"""

import argparse
import csv
import datetime
import os
import re
import subprocess
import sys
from pathlib import Path

# UTF-8 konsol çıktısı desteği
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

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
IZINLI_SEHIRLER = {"Istanbul", "Ankara", "Izmir", "Bursa", "Antalya", "Adana", "Trabzon", "Gaziantep"}
IZINLI_MODLAR = {"kara", "deniz", "hava", "demiryolu"}
IZINLI_DURUMLAR = {"zamaninda", "gecikmeli", "iptal"}


class DQTestRunnerG2:
    def __init__(self, dosya_yolu: Path):
        self.dosya_yolu = dosya_yolu
        self.satirlar = []
        self.baslik = []
        self.sonuclar = {}

    def run_all(self):
        print("=" * 80)
        print("GÖREV 2 VERİ KALİTE TEST KOŞUCUSU (DQ TEST RUNNER — LIN GROUP-B)")
        print("=" * 80)
        print(f"Test Edilen Dosya : {self.dosya_yolu}")
        print(f"Koşum Zamanı      : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

        self.test_01_dosya_varligi()
        if not self.sonuclar.get(1, (False,))[0]:
            print("[KRİTİK HATA] Dosya açılamadığı için sonraki testler iptal edildi.")
            return False

        self.test_02_satir_sayisi()
        self.test_03_sutun_yapisi()
        self.test_04_id_benzersizlik_ve_format()
        self.test_05_tarih_araligi()
        self.test_06_sehirler_ve_rotalar()
        self.test_07_tasima_modlari()
        self.test_08_sayisal_araliklar()
        self.test_09_durum_ve_iptal_bosluk_kurali()
        self.test_10_tekrarlanabilirlik_simulasyon()

        return self.raporla()

    def test_01_dosya_varligi(self):
        no = 1
        ad = "Dosya Varlığı ve UTF-8 Okuma"
        if not self.dosya_yolu.exists():
            self.sonuclar[no] = (False, ad, "Dosya bulunamadı")
            return

        try:
            with open(self.dosya_yolu, mode="r", encoding="utf-8") as f:
                reader = csv.reader(f)
                self.baslik = next(reader)
                self.satirlar = list(reader)
            self.sonuclar[no] = (True, ad, f"UTF-8 okundu; {len(self.satirlar)} veri satırı mevcut")
        except Exception as e:
            self.sonuclar[no] = (False, ad, f"Okuma hatası: {e}")

    def test_02_satir_sayisi(self):
        no = 2
        ad = "Hedef Satır Sayısı (900 Satır)"
        n = len(self.satirlar)
        if n == 900:
            self.sonuclar[no] = (True, ad, f"Tam 900 veri satırı mevcut (hedef %100 sağlandı)")
        else:
            self.sonuclar[no] = (False, ad, f"Satır sayısı 900 değil: {n}")

    def test_03_sutun_yapisi(self):
        no = 3
        ad = "Sütun Sayısı, İsimleri ve Sırası"
        if self.baslik == BEKLENEN_SUTUNLAR:
            self.sonuclar[no] = (True, ad, "10 sütun adı ve sırası veri sözlüğü v2.0 ile birebir uyumlu")
        else:
            self.sonuclar[no] = (False, ad, f"Sütun uyumsuzluğu: {self.baslik}")

    def test_04_id_benzersizlik_ve_format(self):
        no = 4
        ad = "Kimlik Formatı ve Benzersizlik"
        ids = [r[0] for r in self.satirlar]
        if len(ids) != len(set(ids)):
            self.sonuclar[no] = (False, ad, "Tekrarlanan sevkiyat_id tespit edildi")
            return
        format_hatasi = [x for x in ids if not re.fullmatch(r"SVK-G2-\d{4,}", x)]
        if format_hatasi:
            self.sonuclar[no] = (False, ad, f"Geçersiz ID formatı: {format_hatasi[:3]}")
            return
        self.sonuclar[no] = (True, ad, f"900 ID benzersiz ve SVK-G2-XXXX formatında")

    def test_05_tarih_araligi(self):
        no = 5
        ad = "Tarih Formatı ve 60 Günlük Periyot"
        tarihler = [r[1] for r in self.satirlar]
        gecersiz = [t for t in tarihler if not re.fullmatch(r"2026-\d{2}-\d{2}", t)]
        if gecersiz:
            self.sonuclar[no] = (False, ad, f"Geçersiz tarih formatı: {gecersiz[:3]}")
            return
        min_t = min(tarihler)
        max_t = max(tarihler)
        if min_t == "2026-01-01" and max_t == "2026-03-01":
            self.sonuclar[no] = (True, ad, f"Tarihler 2026-01-01 ile 2026-03-01 arasında (60 gün tam)")
        else:
            self.sonuclar[no] = (False, ad, f"Beklenmeyen tarih aralığı: {min_t} - {max_t}")

    def test_06_sehirler_ve_rotalar(self):
        no = 6
        ad = "8 Lojistik Merkez ve Farklı Şehir Kuralı"
        cikislar = {r[2] for r in self.satirlar}
        varislar = {r[3] for r in self.satirlar}
        if not (cikislar.issubset(IZINLI_SEHIRLER) and varislar.issubset(IZINLI_SEHIRLER)):
            self.sonuclar[no] = (False, ad, "İzin verilmeyen şehir tespit edildi")
            return
        ayni_sehir = [r for r in self.satirlar if r[2] == r[3]]
        if ayni_sehir:
            self.sonuclar[no] = (False, ad, f"Çıkış ve varış şehri aynı olan kayıt bulundu: {len(ayni_sehir)}")
            return
        self.sonuclar[no] = (True, ad, "8 merkez doğru kullanıldı, tüm rotalarda çıkış != varış")

    def test_07_tasima_modlari(self):
        no = 7
        ad = "4 Taşıma Modu Temsili"
        modlar = {r[4] for r in self.satirlar}
        if modlar == IZINLI_MODLAR:
            self.sonuclar[no] = (True, ad, "kara, deniz, hava, demiryolu modlarının tamamı temsil ediliyor")
        else:
            self.sonuclar[no] = (False, ad, f"Mod uyumsuzluğu: {modlar}")

    def test_08_sayisal_araliklar(self):
        no = 8
        ad = "Sayısal Aralıklar ve Tipler (Ağırlık, Mesafe, Ücret)"
        hatalar = []
        for i, r in enumerate(self.satirlar, 1):
            agirlik = int(r[5])
            mesafe = int(r[6])
            ucret_str = r[7]
            if not (50 <= agirlik <= 10000):
                hatalar.append(f"Satır {i}: Ağırlık aralık dışı ({agirlik})")
            if not (100 <= mesafe <= 1800):
                hatalar.append(f"Satır {i}: Mesafe aralık dışı ({mesafe})")
            if not re.fullmatch(r"\d+\.\d{2}", ucret_str) or float(ucret_str) <= 0:
                hatalar.append(f"Satır {i}: Geçersiz ücret ({ucret_str})")
        if hatalar:
            self.sonuclar[no] = (False, ad, f"{len(hatalar)} sayıda aralık hatası: {hatalar[:2]}")
        else:
            self.sonuclar[no] = (True, ad, "Ağırlık (50-10000 kg), mesafe (100-1800 km) ve 2 ondalıklı ücret kuralları tam")

    def test_09_durum_ve_iptal_bosluk_kurali(self):
        no = 9
        ad = "Durum Kategorileri ve İptalde Teslim Süresi Boşluk Kuralı"
        hatalar = []
        iptal_sayisi = 0
        for i, r in enumerate(self.satirlar, 1):
            durum = r[9]
            sure = r[8]
            if durum not in IZINLI_DURUMLAR:
                hatalar.append(f"Satır {i}: Geçersiz durum ({durum})")
            if durum == "iptal":
                iptal_sayisi += 1
                if sure != "":
                    hatalar.append(f"Satır {i}: İptal satırında teslim süresi boş değil ('{sure}')")
            else:
                if not re.fullmatch(r"\d+\.\d", sure) or float(sure) <= 0:
                    hatalar.append(f"Satır {i}: Aktif satırda geçersiz teslim süresi ('{sure}')")
        if hatalar:
            self.sonuclar[no] = (False, ad, f"İptal/süre kuralı hatası: {hatalar[:2]}")
        else:
            self.sonuclar[no] = (True, ad, f"{iptal_sayisi} iptal kaydında teslim süresi tam boş; aktif kayıtlar pozitif 1 ondalık")

    def test_10_tekrarlanabilirlik_simulasyon(self):
        no = 10
        ad = "Tohum 42 ile Deterministik Tekrarlanabilirlik"
        kok_dizin = self.dosya_yolu.parent.parent
        sim_script = kok_dizin / "src" / "simulasyon.py"
        temp_csv = kok_dizin / "data" / "temp_test_sevkiyat.csv"
        if not sim_script.exists():
            self.sonuclar[no] = (False, ad, "src/simulasyon.py bulunamadı")
            return

        cmd = [sys.executable, str(sim_script), "--tohum", "42", "--cikti-dosyasi", str(temp_csv)]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if res.returncode != 0:
            self.sonuclar[no] = (False, ad, f"Simülasyon çalıştırma hatası: {res.stderr}")
            return

        with open(self.dosya_yolu, "r", encoding="utf-8") as f1, open(temp_csv, "r", encoding="utf-8") as f2:
            content1 = f1.read()
            content2 = f2.read()

        if temp_csv.exists():
            temp_csv.unlink()

        if content1 == content2:
            self.sonuclar[no] = (True, ad, "Tohum 42 ile üretilen veri mevcut CSV ile %100 birebir eşleşiyor")
        else:
            self.sonuclar[no] = (False, ad, "Tekrarlanan üretim mevcut CSV ile eşleşmedi")

    def raporla(self):
        print("-" * 80)
        print(f"{'No':<4} {'Senaryo Adı':<45} {'Durum':<10} {'Açıklama'}")
        print("-" * 80)
        basarili = 0
        toplam = len(self.sonuclar)
        for no in sorted(self.sonuclar.keys()):
            status, ad, aciklama = self.sonuclar[no]
            st_text = "GEÇTİ" if status else "KALDI"
            if status:
                basarili += 1
            print(f"{no:<4} {ad:<45} {st_text:<10} {aciklama}")
        print("=" * 80)
        print(f"SONUÇ: {basarili}/{toplam} TEST BAŞARIYLA GEÇTİ.")
        print("=" * 80)
        return basarili == toplam


def main():
    kok = Path(__file__).resolve().parent.parent
    varsayilan_csv = kok / "data" / "lojistik_sevkiyat_g2.csv"

    parser = argparse.ArgumentParser(description="Görev 2 DQ Test Koşucusu")
    parser.add_argument("--csv-yolu", type=Path, default=varsayilan_csv, help="Test edilecek CSV yolu")
    args = parser.parse_args()

    runner = DQTestRunnerG2(args.csv_yolu)
    success = runner.run_all()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
