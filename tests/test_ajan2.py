"""
Görev 3: src/simulasyon.py ve src/ajan2_risk.py Birim ve Entegrasyon Testleri
Sorumlu: Aykut Çakıcı (@Aykuutt)
"""

import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import date

KOK_DIZIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK_DIZIN, "src"))

import ajan2_risk
import simulasyon


def _ornek_ajan1_paketi(uretim_zamani="2026-11-26T09:00:00Z", mgm=None, kgm=None, birim="TL/LT"):
    return {
        "mesaj_id": "MSG-G3-TEST-001",
        "uretim_zamani": uretim_zamani,
        "kaynak_ajan": "Ajan_1_WebToplayici",
        "hedef_ajan": "Ajan_2_RiskAnaliz",
        "veri": {
            "mgm_uyarilari": mgm if mgm is not None else [
                {
                    "il": "Trabzon",
                    "seviye": "turuncu",
                    "tur": "yogun_kar",
                    "kaynak_url": "https://www.mgm.gov.tr/Meteouyari/turkiye.aspx?Gun=1",
                    "erisim_tarihi": uretim_zamani[:10],
                }
            ],
            "kgm_yol_durumu": kgm if kgm is not None else [
                {
                    "guzergah": "Ilgar Geçidi",
                    "durum": "kapali",
                    "neden": "kar_ve_tipi",
                    "kaynak_url": "https://www.kgm.gov.tr/Sayfalar/KGM/SiteTr/YolDanisma/GunlukYolDurumuBulteni.aspx",
                    "erisim_tarihi": uretim_zamani[:10],
                },
                {
                    "guzergah": "Pozantı Kavşağı (Ankara-Niğde Otoyolu)",
                    "durum": "tek_serit",
                    "neden": "ust_yapi_calismasi",
                    "kaynak_url": "https://www.kgm.gov.tr/Sayfalar/KGM/SiteTr/YolDanisma/GunlukYolDurumuBulteni.aspx",
                    "erisim_tarihi": uretim_zamani[:10],
                },
            ],
            "akaryakit_fiyatlari": [
                {
                    "il": "Trabzon",
                    "urun": "motorin",
                    "fiyat_tl": 86.50,
                    "birim": birim,
                    "kaynak_url": "https://www.petrolofisi.com.tr/akaryakit-fiyatlari",
                    "erisim_tarihi": uretim_zamani[:10],
                },
                {
                    "il": "Istanbul",
                    "urun": "motorin",
                    "fiyat_tl": 84.60,
                    "birim": birim,
                    "kaynak_url": "https://www.petrolofisi.com.tr/akaryakit-fiyatlari",
                    "erisim_tarihi": uretim_zamani[:10],
                },
            ],
        },
    }


class SimulasyonG3Testleri(unittest.TestCase):
    def test_varsayilan_8_sehir_ve_tekrarlanabilirlik(self):
        v1 = simulasyon.simule_et(
            tohum=42, gun_sayisi=7, gunluk_sevkiyat=20, baslangic_tarihi_str="2026-11-20"
        )
        v2 = simulasyon.simule_et(
            tohum=42, gun_sayisi=7, gunluk_sevkiyat=20, baslangic_tarihi_str="2026-11-20"
        )
        self.assertEqual(v1, v2)
        self.assertEqual(len(v1), 140)
        simulasyon.dogrula(v1)
        sehirler = {r[2] for r in v1} | {r[3] for r in v1}
        self.assertEqual(sehirler, set(simulasyon.VARSAYILAN_SEHIRLER))

    def test_cli_dinamik_sehir_ve_agirlik_araligi(self):
        with tempfile.TemporaryDirectory() as tmp:
            cikti = os.path.join(tmp, "ozel.csv")
            sonuc = subprocess.run(
                [
                    sys.executable,
                    os.path.join(KOK_DIZIN, "src", "simulasyon.py"),
                    "--tohum", "7",
                    "--gun-sayisi", "3",
                    "--gunluk-sevkiyat", "5",
                    "--sehirler", "Istanbul,Ankara,Trabzon",
                    "--baslangic-tarihi", "2027-01-05",
                    "--fiyat-carpani", "1.15",
                    "--min-agirlik", "500",
                    "--max-agirlik", "800",
                    "--cikti-dosyasi", cikti,
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn("15 satir basariyla yazildi", sonuc.stdout)
            with open(cikti, "r", encoding="utf-8") as f:
                satirlar = list(csv.DictReader(f))
            self.assertEqual(len(satirlar), 15)
            for s in satirlar:
                self.assertIn(s["cikis_sehri"], {"Istanbul", "Ankara", "Trabzon"})
                self.assertIn(s["varis_sehri"], {"Istanbul", "Ankara", "Trabzon"})
                self.assertNotEqual(s["cikis_sehri"], s["varis_sehri"])
                self.assertTrue(500 <= int(s["agirlik_kg"]) <= 800)
                self.assertNotIn(",", s["ucret_tl"])

    def test_gecersiz_parametre_hatalari(self):
        with self.assertRaises(ValueError):
            simulasyon.simule_et(fiyat_carpani=0)
        with self.assertRaises(ValueError):
            simulasyon.simule_et(min_agirlik=500, max_agirlik=100)
        with self.assertRaises(ValueError):
            simulasyon.simule_et(sehirler=["Istanbul", "Istanbul"])


class Ajan2RiskTestleri(unittest.TestCase):
    def setUp(self):
        self.csv_yolu = os.path.join(KOK_DIZIN, "data", "lojistik_sevkiyat_g3_ornek.csv")

    def test_bayat_veri_geri_gonderilir(self):
        with tempfile.TemporaryDirectory() as tmp:
            ajan1_yolu = os.path.join(tmp, "bayat.json")
            with open(ajan1_yolu, "w", encoding="utf-8") as f:
                json.dump(_ornek_ajan1_paketi(uretim_zamani="2026-11-10T09:00:00Z"), f)
            with self.assertRaises(ajan2_risk.GeriGonderimHatasi) as ctx:
                ajan2_risk.al_ve_dogrula(
                    ajan1_yolu, self.csv_yolu, referans_tarih=date(2026, 11, 26), max_yas_gun=3
                )
            self.assertIn("bayat", str(ctx.exception).lower())

    def test_uyumsuz_birim_geri_gonderilir(self):
        with tempfile.TemporaryDirectory() as tmp:
            ajan1_yolu = os.path.join(tmp, "birim.json")
            with open(ajan1_yolu, "w", encoding="utf-8") as f:
                json.dump(_ornek_ajan1_paketi(birim="USD/GAL"), f)
            with self.assertRaises(ajan2_risk.GeriGonderimHatasi) as ctx:
                ajan2_risk.al_ve_dogrula(
                    ajan1_yolu, self.csv_yolu, referans_tarih=date(2026, 11, 26)
                )
            self.assertIn("uyumsuz birim", str(ctx.exception).lower())

    def test_mgm_kgm_risk_puanlama_ve_teslim_paketi(self):
        with tempfile.TemporaryDirectory() as tmp:
            ajan1_yolu = os.path.join(tmp, "ajan1.json")
            cikti_json = os.path.join(tmp, "ajan2.json")
            cikti_csv = os.path.join(tmp, "ajan2.csv")
            with open(ajan1_yolu, "w", encoding="utf-8") as f:
                json.dump(_ornek_ajan1_paketi(), f)

            ajan1_veri, sevkiyatlar = ajan2_risk.al_ve_dogrula(
                ajan1_yolu, self.csv_yolu, referans_tarih=date(2026, 11, 26)
            )
            analiz = ajan2_risk.isle_risk_analizi(ajan1_veri, sevkiyatlar)
            paket = ajan2_risk.teslim_paketi_hazirla(
                analiz, ajan1_veri, cikti_json, cikti_csv, uretim_zamani="2026-11-26T10:00:00Z"
            )

            self.assertEqual(paket["hedef_ajan"], "Ajan_3_Denetim")
            self.assertGreater(paket["ozet"]["yuksek_ve_kritik_risk_sayisi"], 0)

            # İptal sevkiyatlarda teslim süresi kesinlikle boş kalmalı
            iptaller = [r for r in analiz["sevkiyat_riskleri"] if r["durum"] == "iptal"]
            self.assertGreater(len(iptaller), 0)
            for r in iptaller:
                self.assertEqual(r["tahmini_teslim_suresi_saat"], "")

            # Trabzon karayolu sevkiyatlarında MGM turuncu (+50) + KGM kapali (+35, +12 saat) yansımalı
            trabzon_kara = [
                r for r in analiz["sevkiyat_riskleri"]
                if r["durum"] != "iptal" and r["tasima_modu"] == "kara" and "Trabzon" in r["rota"]
            ]
            self.assertGreater(len(trabzon_kara), 0)
            for r in trabzon_kara:
                self.assertGreaterEqual(r["risk_puani"], 85)
                self.assertGreaterEqual(r["ek_gecikme_saat"], 12.0)
                self.assertTrue(len(r["dayanak_kaynaklar"]) >= 2)


if __name__ == "__main__":
    unittest.main()
