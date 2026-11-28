"""
Görev 3: src/ajan3_denetim.py Birim ve Entegrasyon Testleri
Sorumlu: DQ / Ajan 3 — Ece Naz Aktürk (@ece-naz)
"""

import copy
import json
import os
import sys
import tempfile
import unittest

KOK_DIZIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK_DIZIN, "src"))

import ajan3_denetim


def _ornek_gecerli_ajan2_paketi():
    return {
        "mesaj_id": "MSG-G3-TEST-A2-001",
        "uretim_zamani": "2026-11-26T10:00:00Z",
        "kaynak_ajan": "Ajan_2_RiskAnaliz",
        "hedef_ajan": "Ajan_3_Denetim",
        "referans_mesaj_id": "MSG-G3-TEST-001",
        "kaynaklar": [
            {
                "kaynak": "KGM",
                "kaynak_url": "https://www.kgm.gov.tr/Sayfalar/KGM/SiteTr/YolDanisma/GunlukYolDurumuBulteni.aspx",
                "erisim_tarihi": "2026-11-26",
            }
        ],
        "ozet": {
            "toplam_sevkiyat": 140,
            "aktif_sevkiyat": 134,
            "iptal_sevkiyat": 6,
            "yuksek_ve_kritik_risk_sayisi": 1,
            "ortalama_risk_puani": 13.13,
            "ortalama_motorin_tl": 86.10,
            "genel_yakit_carpani": 1.0129,
        },
        "yuksek_riskli_sevkiyatlar": [
            {
                "sevkiyat_id": "SVK-G3-0093",
                "tarih": "2026-11-24",
                "rota": "Trabzon -> Adana",
                "tasima_modu": "kara",
                "durum": "gecikmeli",
                "baz_ucret_tl": "5253.50",
                "yakit_etkili_ucret_tl": "5345.96",
                "risk_puani": 70,
                "risk_seviyesi": "yuksek",
                "ek_gecikme_saat": 16.0,
                "tahmini_teslim_suresi_saat": "57.1",
                "risk_nedenleri": [
                    "operasyonel_gecikme",
                    "kgm_kapali_Ilgar Geçidi",
                ],
                "dayanak_kaynaklar": [
                    {
                        "kaynak": "KGM",
                        "detay": "Ilgar Geçidi (kapali)",
                        "kaynak_url": "https://www.kgm.gov.tr/Sayfalar/KGM/SiteTr/YolDanisma/GunlukYolDurumuBulteni.aspx",
                        "erisim_tarihi": "2026-11-26",
                    }
                ],
            }
        ],
    }


class TestAjan3Denetim(unittest.TestCase):
    def test_01_gecerli_ajan2_paketi_dogrulama(self):
        """Geçerli bir Ajan 2 girdi paketi al_ve_denetle filtresinden başarıyla geçmelidir."""
        paket = _ornek_gecerli_ajan2_paketi()
        sonuc = ajan3_denetim.al_ve_denetle(paket)
        self.assertTrue(sonuc)

    def test_02_eksik_alan_geri_gonderim(self):
        """Zorunlu bir kök alan eksik olduğunda GeriGonderimHatasi fırlatılmalıdır."""
        paket = _ornek_gecerli_ajan2_paketi()
        del paket["mesaj_id"]
        with self.assertRaises(ajan3_denetim.GeriGonderimHatasi) as ctx:
            ajan3_denetim.al_ve_denetle(paket)
        self.assertIn("mesaj_id", str(ctx.exception))

    def test_03_sayisal_tutarsizlik_geri_gonderim(self):
        """toplam_sevkiyat != aktif + iptal olduğunda tutarsızlık tespit edilmeli ve iade edilmelidir."""
        paket = _ornek_gecerli_ajan2_paketi()
        paket["ozet"]["toplam_sevkiyat"] = 150  # 134 + 6 = 140 != 150
        with self.assertRaises(ajan3_denetim.GeriGonderimHatasi) as ctx:
            ajan3_denetim.al_ve_denetle(paket)
        self.assertIn("tutarsızlık", str(ctx.exception).lower())

    def test_04_gecersiz_risk_puani_geri_gonderim(self):
        """0-100 aralığı dışındaki risk puanı iade gerekçesi olmalıdır."""
        paket = _ornek_gecerli_ajan2_paketi()
        paket["yuksek_riskli_sevkiyatlar"][0]["risk_puani"] = 105
        with self.assertRaises(ajan3_denetim.GeriGonderimHatasi) as ctx:
            ajan3_denetim.al_ve_denetle(paket)
        self.assertIn("0-100", str(ctx.exception))

    def test_05_gecersiz_url_geri_gonderim(self):
        """http/https olmayan geçersiz kaynak URL'si reddedilmelidir."""
        paket = _ornek_gecerli_ajan2_paketi()
        paket["kaynaklar"][0]["kaynak_url"] = "ftp://gecersiz.kaynak"
        with self.assertRaises(ajan3_denetim.GeriGonderimHatasi) as ctx:
            ajan3_denetim.al_ve_denetle(paket)
        self.assertIn("URL", str(ctx.exception))

    def test_06_esik_suzme_ve_onay(self):
        """denetle_ve_suz fonksiyonu eşik üstü riskli sevkiyatları doğru süzmeli ve onaylamalıdır."""
        paket = _ornek_gecerli_ajan2_paketi()
        sonuc = ajan3_denetim.denetle_ve_suz(paket, kritik_esik=65)
        self.assertEqual(sonuc["onaylanan_adet"], 1)
        self.assertEqual(sonuc["onaylanan_sevkiyatlar"][0]["sevkiyat_id"], "SVK-G3-0093")

    def test_07_musteri_mesaji_uretimi(self):
        """Üretilen müşteri mesajında takip no, güzergah ve resmi tıklanabilir link bulunmalıdır."""
        paket = _ornek_gecerli_ajan2_paketi()
        sev = paket["yuksek_riskli_sevkiyatlar"][0]
        bildirim = ajan3_denetim.musteri_mesaji_hazirla(sev)

        self.assertEqual(bildirim["sevkiyat_id"], "SVK-G3-0093")
        mesaj_metni = bildirim["musteri_mesaji_metni"]
        self.assertIn("SVK-G3-0093", mesaj_metni)
        self.assertIn("Trabzon -> Adana", mesaj_metni)
        self.assertIn("https://www.kgm.gov.tr", mesaj_metni)
        self.assertIn("[Resmi Duyuru Bağlantısı]", mesaj_metni)

    def test_08_uctan_uca_calistir(self):
        """calistir() fonksiyonu geçici dizinde JSON paketini ve Markdown raporunu eksiksiz üretmelidir."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cikti_json = os.path.join(tmpdir, "ajan3_mesaj.json")
            cikti_md = os.path.join(tmpdir, "ajan3_rapor.md")

            paket = ajan3_denetim.calistir(
                cikti_json_yolu=cikti_json,
                cikti_md_yolu=cikti_md,
                kritik_esik=65,
            )

            self.assertTrue(os.path.exists(cikti_json))
            self.assertTrue(os.path.exists(cikti_md))
            self.assertEqual(paket["kaynak_ajan"], "Ajan_3_Denetim")
            self.assertEqual(paket["hedef_ajan"], "Cekirdek_Ve_Arayuz")
            self.assertEqual(len(paket["musteri_bildirim_mesajlari"]), 1)

    def test_09_standart_red_zarfi_uretimi(self):
        """Duyuru 11 standardı red zarfı beklenen alanları eksiksiz içermelidir."""
        red = ajan3_denetim.red_zarfi_uret(
            ajan2_paketi={"mesaj_id": "MSG-G3-TEST-A2-001"},
            gerekce="Sayısal tutarsızlık",
            sorunlu_alanlar=["ozet.toplam_sevkiyat"],
            hata_kodu="ERR_NUMERICAL_INCONSISTENCY",
        )
        self.assertEqual(red["durum"], "red")
        self.assertEqual(red["kaynak_ajan"], "Ajan_3_Denetim")
        self.assertEqual(red["hedef_ajan"], "Ajan_2_RiskAnaliz")
        self.assertEqual(red["hata_kodu"], "ERR_NUMERICAL_INCONSISTENCY")
        self.assertIn("ozet.toplam_sevkiyat", red["sorunlu_alanlar"])


if __name__ == "__main__":
    unittest.main()
