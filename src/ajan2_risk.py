"""
Logistics Intelligence Network (LIN) - Ajan 2 (Sevkiyat & Rota Risk Motoru)
Görev 3: Çok Ajanlı Şirket Programı (Duyuru 10 & docs/veri-sozlugu.md v3.0 uyumlu)
Sorumlu: Aykut Çakıcı (@Aykuutt)
"""

import argparse
import csv
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date, datetime, timezone

BEKLENEN_SEVKIYAT_SUTUNLARI = [
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

MGM_RISK_PUANI = {
    "sari": 25,
    "turuncu": 50,
    "kirmizi": 75,
}

KGM_ETKI = {
    "kapali": {"risk": 35, "gecikme_saat": 12.0},
    "tek_serit": {"risk": 15, "gecikme_saat": 4.0},
}

# KGM bültenlerindeki bilinen geçit/otoyol koridorlarının etkilediği lojistik merkezler
KORIDOR_SEHIR_HARITASI = {
    "pozanti": {"Ankara", "Adana", "Gaziantep"},
    "ankara-nigde": {"Ankara", "Adana", "Gaziantep"},
    "ilgar": {"Trabzon"},
    "soganli": {"Trabzon"},
    "of-caykara": {"Trabzon"},
    "ovit": {"Trabzon"},
    "sahara": {"Trabzon"},
    "artvin": {"Trabzon"},
    "bornova": {"Izmir"},
    "izmir": {"Izmir"},
    "edirne": {"Istanbul"},
    "balikesir": {"Bursa", "Izmir"},
}


class GeriGonderimHatasi(ValueError):
    """Ajan 1 girdisi veya sevkiyat verisi şema/tazelik/birim kuralını ihlal ettiğinde fırlatılır."""


def metin_normallestir(metin):
    """Türkçe karakterleri ASCII karşılıklarına dönüştürür ve küçük harfe çevirir."""
    if not metin:
        return ""
    donusum = str.maketrans("çğıİöşüÇĞÖŞÜ", "cgiiosuCGOSU")
    return str(metin).translate(donusum).lower().strip()


def _tarih_cozumle(tarih_str):
    """ISO tarih veya tarih-saat metninden date nesnesi döndürür."""
    if not isinstance(tarih_str, str) or not tarih_str.strip():
        raise GeriGonderimHatasi("Tarih alanı boş olamaz.")
    parca = tarih_str.strip()[:10]
    try:
        return date.fromisoformat(parca)
    except ValueError as exc:
        raise GeriGonderimHatasi(f"Geçersiz ISO tarih formatı: '{tarih_str}'") from exc


def _url_gecerli_mi(url):
    return isinstance(url, str) and (url.startswith("https://") or url.startswith("http://"))


def _risk_seviyesi_belirle(puan):
    if puan >= 80:
        return "kritik"
    if puan >= 60:
        return "yuksek"
    if puan >= 30:
        return "orta"
    return "dusuk"


def al_ve_dogrula(ajan1_yolu, sevkiyat_yolu, referans_tarih=None, max_yas_gun=3):
    """
    Alma Skill'i: Ajan 1 JSON paketini ve şirket sevkiyat CSV dosyasını okur,
    şema, tazelik, birim ve kaynak URL zorunluluklarını doğrular.
    """
    if not os.path.exists(ajan1_yolu):
        raise GeriGonderimHatasi(f"Ajan 1 mesaj dosyası bulunamadı: {ajan1_yolu}")
    if not os.path.exists(sevkiyat_yolu):
        raise GeriGonderimHatasi(f"Sevkiyat CSV dosyası bulunamadı: {sevkiyat_yolu}")

    try:
        with open(ajan1_yolu, "r", encoding="utf-8-sig") as f:
            ajan1_veri = json.load(f)
    except json.JSONDecodeError as exc:
        raise GeriGonderimHatasi(f"Ajan 1 JSON ayrıştırılamadı: {exc}") from exc

    for zorunlu in ("mesaj_id", "uretim_zamani", "kaynak_ajan", "hedef_ajan", "veri"):
        if not ajan1_veri.get(zorunlu):
            raise GeriGonderimHatasi(f"Ajan 1 mesajında eksik zorunlu alan: '{zorunlu}'")

    bugun = referans_tarih if referans_tarih is not None else date.today()
    uretim_tarihi = _tarih_cozumle(ajan1_veri["uretim_zamani"])
    if (bugun - uretim_tarihi).days > max_yas_gun:
        raise GeriGonderimHatasi(
            f"Ajan 1 verisi bayat: üretim tarihi {uretim_tarihi.isoformat()}, "
            f"referans tarih {bugun.isoformat()} (> {max_yas_gun} gün)."
        )

    veri = ajan1_veri["veri"]
    if not isinstance(veri, dict):
        raise GeriGonderimHatasi("Ajan 1 mesajındaki 'veri' alanı nesne (dict) olmalıdır.")

    for bolum in ("mgm_uyarilari", "kgm_yol_durumu", "akaryakit_fiyatlari"):
        if bolum not in veri or not isinstance(veri[bolum], list):
            raise GeriGonderimHatasi(f"Ajan 1 'veri' içinde eksik veya hatalı liste: '{bolum}'")

    for idx, uyari in enumerate(veri["mgm_uyarilari"], start=1):
        if not uyari.get("il") or not uyari.get("seviye"):
            raise GeriGonderimHatasi(f"MGM uyarısı #{idx} içinde 'il' veya 'seviye' eksik.")
        if not _url_gecerli_mi(uyari.get("kaynak_url")):
            raise GeriGonderimHatasi(f"MGM uyarısı #{idx} geçerli 'kaynak_url' içermiyor.")
        if "erisim_tarihi" in uyari:
            erisim = _tarih_cozumle(uyari["erisim_tarihi"])
            if (bugun - erisim).days > max_yas_gun:
                raise GeriGonderimHatasi(f"MGM uyarısı #{idx} erişim tarihi bayat: {erisim.isoformat()}")

    for idx, yol in enumerate(veri["kgm_yol_durumu"], start=1):
        if not yol.get("guzergah") or not yol.get("durum"):
            raise GeriGonderimHatasi(f"KGM yol kaydı #{idx} içinde 'guzergah' veya 'durum' eksik.")
        if not _url_gecerli_mi(yol.get("kaynak_url")):
            raise GeriGonderimHatasi(f"KGM yol kaydı #{idx} geçerli 'kaynak_url' içermiyor.")
        if "erisim_tarihi" in yol:
            erisim = _tarih_cozumle(yol["erisim_tarihi"])
            if (bugun - erisim).days > max_yas_gun:
                raise GeriGonderimHatasi(f"KGM yol kaydı #{idx} erişim tarihi bayat: {erisim.isoformat()}")

    if not veri["akaryakit_fiyatlari"]:
        raise GeriGonderimHatasi("Ajan 1 'akaryakit_fiyatlari' listesi boş olamaz.")

    for idx, yakit in enumerate(veri["akaryakit_fiyatlari"], start=1):
        if not yakit.get("il"):
            raise GeriGonderimHatasi(f"Akaryakıt kaydı #{idx} içinde 'il' eksik.")
        if yakit.get("birim") != "TL/LT":
            raise GeriGonderimHatasi(
                f"Akaryakıt kaydı #{idx} uyumsuz birim: '{yakit.get('birim')}' (beklenen: 'TL/LT')."
            )
        try:
            fiyat = float(yakit.get("fiyat_tl", 0))
        except (TypeError, ValueError) as exc:
            raise GeriGonderimHatasi(f"Akaryakıt kaydı #{idx} geçersiz fiyat_tl.") from exc
        if fiyat <= 0:
            raise GeriGonderimHatasi(f"Akaryakıt kaydı #{idx} fiyatı pozitif olmalıdır: {fiyat}")
        if not _url_gecerli_mi(yakit.get("kaynak_url")):
            raise GeriGonderimHatasi(f"Akaryakıt kaydı #{idx} geçerli 'kaynak_url' içermiyor.")
        if "erisim_tarihi" in yakit:
            erisim = _tarih_cozumle(yakit["erisim_tarihi"])
            if (bugun - erisim).days > max_yas_gun:
                raise GeriGonderimHatasi(f"Akaryakıt kaydı #{idx} erişim tarihi bayat: {erisim.isoformat()}")

    with open(sevkiyat_yolu, "r", encoding="utf-8-sig") as f:
        okuyucu = csv.DictReader(f)
        if okuyucu.fieldnames != BEKLENEN_SEVKIYAT_SUTUNLARI:
            raise GeriGonderimHatasi(
                f"Sevkiyat CSV sütunları v3.0 şemasıyla uyuşmuyor: {okuyucu.fieldnames}"
            )
        sevkiyatlar = list(okuyucu)

    if not sevkiyatlar:
        raise GeriGonderimHatasi("Sevkiyat CSV dosyası boş olamaz.")

    for i, s in enumerate(sevkiyatlar, start=1):
        if s["cikis_sehri"] == s["varis_sehri"]:
            raise GeriGonderimHatasi(f"Sevkiyat satırı #{i}: çıkış ve varış şehri aynı ({s['cikis_sehri']}).")
        if "," in s["ucret_tl"]:
            raise GeriGonderimHatasi(f"Sevkiyat satırı #{i}: ücret virgül ondalık içeremez ({s['ucret_tl']}).")
        if s["durum"] == "iptal" and s["teslim_suresi_saat"] != "":
            raise GeriGonderimHatasi(f"Sevkiyat satırı #{i}: iptal kaydında teslim süresi boş olmalıdır.")
        if s["durum"] != "iptal":
            if not re.fullmatch(r"\d+(\.\d+)?", s["teslim_suresi_saat"]):
                raise GeriGonderimHatasi(
                    f"Sevkiyat satırı #{i}: geçersiz teslim_suresi_saat değeri '{s['teslim_suresi_saat']}'."
                )

    return ajan1_veri, sevkiyatlar


def _kgm_etkilenen_sehirler(guzergah_metni):
    """KGM güzergah metninden etkilenen merkez iller kümesini çıkarır."""
    norm = metin_normallestir(guzergah_metni)
    sehirler = set()
    for anahtar, il_kumesi in KORIDOR_SEHIR_HARITASI.items():
        if anahtar in norm:
            sehirler.update(il_kumesi)
    for merkez in ("Istanbul", "Ankara", "Izmir", "Bursa", "Antalya", "Adana", "Trabzon", "Gaziantep"):
        if metin_normallestir(merkez) in norm:
            sehirler.add(merkez)
    return sehirler


def isle_risk_analizi(ajan1_veri, sevkiyatlar, baz_motorin_tl=85.0):
    """
    İşleme Skill'i: Ajan 1 dış verilerini şirket içi sentetik sevkiyatlarla birleştirir,
    0-100 arası rota risk puanı, tahmini gecikme ve yakıt etkili maliyet hesaplar.
    """
    veri = ajan1_veri["veri"]
    genel_erisim = ajan1_veri["uretim_zamani"][:10]

    # 1. Yakıt fiyatları haritası
    yakit_haritasi = {}
    for y in veri["akaryakit_fiyatlari"]:
        yakit_haritasi[metin_normallestir(y["il"])] = y
    ort_motorin = sum(float(y["fiyat_tl"]) for y in veri["akaryakit_fiyatlari"]) / len(veri["akaryakit_fiyatlari"])
    genel_yakit_carpani = round(ort_motorin / baz_motorin_tl, 4)

    # 2. MGM uyarıları il bazlı indeksleme
    mgm_il_uyarilari = defaultdict(list)
    for u in veri["mgm_uyarilari"]:
        mgm_il_uyarilari[metin_normallestir(u["il"])].append(u)

    # 3. KGM yol kayıtlarını etkilenen şehirlere bağlama
    kgm_kayitlari = []
    for k in veri["kgm_yol_durumu"]:
        etkilenen = _kgm_etkilenen_sehirler(k["guzergah"])
        kgm_kayitlari.append((k, {metin_normallestir(s) for s in etkilenen}))

    sevkiyat_sonuclari = []
    rota_istatistik = defaultdict(lambda: {"adet": 0, "toplam_risk": 0, "yuksek_risk_adet": 0})

    for s in sevkiyatlar:
        cikis = s["cikis_sehri"]
        varis = s["varis_sehri"]
        cikis_norm = metin_normallestir(cikis)
        varis_norm = metin_normallestir(varis)
        mod = s["tasima_modu"]
        durum = s["durum"]
        baz_ucret = float(s["ucret_tl"])

        yakit_kaydi = yakit_haritasi.get(cikis_norm) or yakit_haritasi.get(varis_norm)
        if yakit_kaydi:
            sehir_yakit_carpani = round(float(yakit_kaydi["fiyat_tl"]) / baz_motorin_tl, 4)
        else:
            sehir_yakit_carpani = genel_yakit_carpani
        guncel_ucret = round(baz_ucret * sehir_yakit_carpani, 2)

        dayanaklar = []
        if yakit_kaydi:
            dayanaklar.append({
                "kaynak": "AKARYAKIT",
                "detay": f"{yakit_kaydi['il']} motorin {yakit_kaydi['fiyat_tl']} {yakit_kaydi['birim']}",
                "kaynak_url": yakit_kaydi["kaynak_url"],
                "erisim_tarihi": yakit_kaydi.get("erisim_tarihi", genel_erisim),
            })

        if durum == "iptal":
            sevkiyat_sonuclari.append({
                "sevkiyat_id": s["sevkiyat_id"],
                "tarih": s["tarih"],
                "rota": f"{cikis} -> {varis}",
                "tasima_modu": mod,
                "durum": durum,
                "baz_ucret_tl": f"{baz_ucret:.2f}",
                "yakit_etkili_ucret_tl": f"{guncel_ucret:.2f}",
                "risk_puani": 0,
                "risk_seviyesi": "iptal",
                "ek_gecikme_saat": None,
                "tahmini_teslim_suresi_saat": "",
                "risk_nedenleri": ["sevkiyat_iptal"],
                "dayanak_kaynaklar": dayanaklar,
            })
            continue

        risk_puani = 0
        ek_gecikme = 0.0
        nedenler = []

        if durum == "gecikmeli":
            risk_puani += 20
            nedenler.append("operasyonel_gecikme")

        # Yakıt baskısı
        if sehir_yakit_carpani >= 1.02:
            risk_puani += 5
            nedenler.append("yuksek_akaryakit_maliyeti")

        # MGM uyarısı kontrolü (çıkış veya varış ili)
        gorulen_mgm = set()
        for sehir_norm in (cikis_norm, varis_norm):
            for u in mgm_il_uyarilari.get(sehir_norm, []):
                seviye = metin_normallestir(u.get("seviye", ""))
                puan = MGM_RISK_PUANI.get(seviye, 15)
                anahtar = (u["il"], seviye, u.get("tur", ""))
                if anahtar not in gorulen_mgm:
                    gorulen_mgm.add(anahtar)
                    risk_puani += puan
                    nedenler.append(f"mgm_{seviye}_{u['il']}")
                    dayanaklar.append({
                        "kaynak": "MGM",
                        "detay": f"{u['il']} {seviye} ({u.get('tur', 'uyari')})",
                        "kaynak_url": u["kaynak_url"],
                        "erisim_tarihi": u.get("erisim_tarihi", genel_erisim),
                    })

        # KGM yol durumu kontrolü (karayolu sevkiyatları için güzergah/koridor eşleşmesi)
        if mod == "kara":
            for k, etkilenen_normlar in kgm_kayitlari:
                if cikis_norm in etkilenen_normlar or varis_norm in etkilenen_normlar:
                    yol_durumu = metin_normallestir(k.get("durum", ""))
                    etki = KGM_ETKI.get(yol_durumu, {"risk": 10, "gecikme_saat": 2.0})
                    risk_puani += etki["risk"]
                    ek_gecikme += etki["gecikme_saat"]
                    nedenler.append(f"kgm_{yol_durumu}_{k['guzergah']}")
                    dayanaklar.append({
                        "kaynak": "KGM",
                        "detay": f"{k['guzergah']} ({yol_durumu})",
                        "kaynak_url": k["kaynak_url"],
                        "erisim_tarihi": k.get("erisim_tarihi", genel_erisim),
                    })

        risk_puani = min(100, risk_puani)
        risk_seviyesi = _risk_seviyesi_belirle(risk_puani)
        mevcut_sure = float(s["teslim_suresi_saat"])
        yeni_sure = round(mevcut_sure + ek_gecikme, 1)

        rota_adi = f"{cikis} -> {varis}"
        rota_istatistik[rota_adi]["adet"] += 1
        rota_istatistik[rota_adi]["toplam_risk"] += risk_puani
        if risk_puani >= 60:
            rota_istatistik[rota_adi]["yuksek_risk_adet"] += 1

        sevkiyat_sonuclari.append({
            "sevkiyat_id": s["sevkiyat_id"],
            "tarih": s["tarih"],
            "rota": rota_adi,
            "tasima_modu": mod,
            "durum": durum,
            "baz_ucret_tl": f"{baz_ucret:.2f}",
            "yakit_etkili_ucret_tl": f"{guncel_ucret:.2f}",
            "risk_puani": risk_puani,
            "risk_seviyesi": risk_seviyesi,
            "ek_gecikme_saat": round(ek_gecikme, 1),
            "tahmini_teslim_suresi_saat": f"{yeni_sure:.1f}",
            "risk_nedenleri": nedenler if nedenler else ["normal_akıs"],
            "dayanak_kaynaklar": dayanaklar,
        })

    aktifler = [r for r in sevkiyat_sonuclari if r["durum"] != "iptal"]
    yuksek_riskliler = [r for r in aktifler if r["risk_puani"] >= 60]
    ort_risk = round(sum(r["risk_puani"] for r in aktifler) / len(aktifler), 2) if aktifler else 0.0

    top_rotalar = sorted(
        [
            {
                "rota": rota,
                "aktif_sevkiyat": st["adet"],
                "ortalama_risk_puani": round(st["toplam_risk"] / st["adet"], 2),
                "yuksek_riskli_adet": st["yuksek_risk_adet"],
            }
            for rota, st in rota_istatistik.items()
        ],
        key=lambda x: (-x["ortalama_risk_puani"], -x["yuksek_riskli_adet"], x["rota"]),
    )[:5]

    ozet = {
        "toplam_sevkiyat": len(sevkiyat_sonuclari),
        "aktif_sevkiyat": len(aktifler),
        "iptal_sevkiyat": len(sevkiyat_sonuclari) - len(aktifler),
        "yuksek_ve_kritik_risk_sayisi": len(yuksek_riskliler),
        "ortalama_risk_puani": ort_risk,
        "ortalama_motorin_tl": round(ort_motorin, 2),
        "genel_yakit_carpani": genel_yakit_carpani,
        "en_riskli_rotalar": top_rotalar,
    }

    return {
        "ozet": ozet,
        "sevkiyat_riskleri": sevkiyat_sonuclari,
        "yuksek_riskli_sevkiyatlar": sorted(
            yuksek_riskliler, key=lambda x: (-x["risk_puani"], x["sevkiyat_id"])
        ),
    }


def _benzersiz_kaynaklar_cikar(ajan1_veri):
    """Ajan 1 verisinden kullanılan benzersiz kaynak URL ve erişim tarihlerini derler."""
    kaynaklar = []
    gorulen = set()
    genel_tarih = ajan1_veri["uretim_zamani"][:10]
    for bolum, ad in (
        ("mgm_uyarilari", "MGM"),
        ("kgm_yol_durumu", "KGM"),
        ("akaryakit_fiyatlari", "AKARYAKIT"),
    ):
        for oge in ajan1_veri["veri"].get(bolum, []):
            url = oge.get("kaynak_url", "")
            tarih = oge.get("erisim_tarihi", genel_tarih)
            if url and (ad, url, tarih) not in gorulen:
                gorulen.add((ad, url, tarih))
                kaynaklar.append({"kaynak": ad, "kaynak_url": url, "erisim_tarihi": tarih})
    return kaynaklar


def teslim_paketi_hazirla(analiz_sonucu, ajan1_veri, cikti_json_yolu, cikti_csv_yolu, uretim_zamani=None):
    """
    Teslim Skill'i: Risk analiz sonucunu Ajan 3'ün beklediği ortak JSON mesaj biçimine
    ve CSV raporuna dönüştürür, kaynak ve zaman damgası doğrulaması yaparak diske yazar.
    """
    zaman_damgasi = uretim_zamani or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    tarih_kisa = zaman_damgasi[:10].replace("-", "")

    for r in analiz_sonucu["yuksek_riskli_sevkiyatlar"]:
        if not r["dayanak_kaynaklar"]:
            raise GeriGonderimHatasi(
                f"Teslim doğrulama hatası: {r['sevkiyat_id']} kaydında kaynak URL kanıtı eksik."
            )

    paket = {
        "mesaj_id": f"MSG-G3-{tarih_kisa}-A2-001",
        "uretim_zamani": zaman_damgasi,
        "kaynak_ajan": "Ajan_2_RiskAnaliz",
        "hedef_ajan": "Ajan_3_Denetim",
        "referans_mesaj_id": ajan1_veri["mesaj_id"],
        "kaynaklar": _benzersiz_kaynaklar_cikar(ajan1_veri),
        "ozet": analiz_sonucu["ozet"],
        "yuksek_riskli_sevkiyatlar": analiz_sonucu["yuksek_riskli_sevkiyatlar"],
    }

    os.makedirs(os.path.dirname(os.path.abspath(cikti_json_yolu)), exist_ok=True)
    with open(cikti_json_yolu, "w", encoding="utf-8") as f:
        json.dump(paket, f, ensure_ascii=False, indent=2)

    os.makedirs(os.path.dirname(os.path.abspath(cikti_csv_yolu)), exist_ok=True)
    csv_alanlari = [
        "sevkiyat_id",
        "tarih",
        "rota",
        "tasima_modu",
        "durum",
        "baz_ucret_tl",
        "yakit_etkili_ucret_tl",
        "risk_puani",
        "risk_seviyesi",
        "ek_gecikme_saat",
        "tahmini_teslim_suresi_saat",
        "risk_nedenleri",
        "kaynak_sayisi",
    ]
    with open(cikti_csv_yolu, "w", newline="", encoding="utf-8") as f:
        yazici = csv.DictWriter(f, fieldnames=csv_alanlari)
        yazici.writeheader()
        for r in analiz_sonucu["sevkiyat_riskleri"]:
            yazici.writerow({
                "sevkiyat_id": r["sevkiyat_id"],
                "tarih": r["tarih"],
                "rota": r["rota"],
                "tasima_modu": r["tasima_modu"],
                "durum": r["durum"],
                "baz_ucret_tl": r["baz_ucret_tl"],
                "yakit_etkili_ucret_tl": r["yakit_etkili_ucret_tl"],
                "risk_puani": r["risk_puani"],
                "risk_seviyesi": r["risk_seviyesi"],
                "ek_gecikme_saat": "" if r["ek_gecikme_saat"] is None else r["ek_gecikme_saat"],
                "tahmini_teslim_suresi_saat": r["tahmini_teslim_suresi_saat"],
                "risk_nedenleri": ";".join(r["risk_nedenleri"]),
                "kaynak_sayisi": len(r["dayanak_kaynaklar"]),
            })

    return paket


def main():
    parser = argparse.ArgumentParser(
        description="Görev 3 - Ajan 2: Sevkiyat & Rota Risk Analiz Motoru (LIN Group-B)"
    )
    kok_dizin = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    parser.add_argument(
        "--ajan1-json",
        type=str,
        default=os.path.join(kok_dizin, "data", "ajan1_mesaj.json"),
        help="Ajan 1'den gelen JSON girdi dosyası",
    )
    parser.add_argument(
        "--sevkiyat-csv",
        type=str,
        default=os.path.join(kok_dizin, "data", "lojistik_sevkiyat_g3_ornek.csv"),
        help="Şirket içi sentetik sevkiyat CSV dosyası",
    )
    parser.add_argument(
        "--cikti-json",
        type=str,
        default=os.path.join(kok_dizin, "data", "ajan2_mesaj.json"),
        help="Ajan 3'e iletilecek JSON çıktı dosyası",
    )
    parser.add_argument(
        "--cikti-csv",
        type=str,
        default=os.path.join(kok_dizin, "data", "ajan2_risk_analizi.csv"),
        help="Tüm sevkiyat risk tablosu CSV çıktı dosyası",
    )
    parser.add_argument(
        "--max-yas-gun",
        type=int,
        default=3,
        help="Dış veri tazelik eşiği (gün, varsayılan: 3)",
    )
    parser.add_argument(
        "--referans-tarih",
        type=str,
        default=None,
        help="Tazelik kontrolü için referans tarih YYYY-MM-DD (varsayılan: bugün)",
    )

    args = parser.parse_args()
    ref_tarih = date.fromisoformat(args.referans_tarih) if args.referans_tarih else None

    try:
        ajan1_veri, sevkiyatlar = al_ve_dogrula(
            args.ajan1_json,
            args.sevkiyat_csv,
            referans_tarih=ref_tarih,
            max_yas_gun=args.max_yas_gun,
        )
        analiz = isle_risk_analizi(ajan1_veri, sevkiyatlar)
        paket = teslim_paketi_hazirla(analiz, ajan1_veri, args.cikti_json, args.cikti_csv)
    except GeriGonderimHatasi as hata:
        print(f"[GERI GONDERIM - AJAN 2] {hata}", file=sys.stderr)
        sys.exit(2)

    ozet = paket["ozet"]
    print(
        f"[OK] Ajan 2 Risk Analizi tamamlandi: {ozet['toplam_sevkiyat']} sevkiyat incelendi, "
        f"{ozet['yuksek_ve_kritik_risk_sayisi']} yuksek/kritik riskli sevkiyat -> {args.cikti_json}"
    )


if __name__ == "__main__":
    main()
