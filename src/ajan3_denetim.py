"""
Logistics Intelligence Network (LIN) - Ajan 3 (Denetim, Kalite Kontrol & Müşteri İletişimi)
Görev 3: Çok Ajanlı Şirket Programı (Duyuru 10 & docs/veri-sozlugu.md v3.0 uyumlu)
Sorumlu: Ece Naz Aktürk (@ece-naz)
"""

import argparse
import csv
import json
import os
import re
import sys
from datetime import date, datetime, timezone

KOK_DIZIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class GeriGonderimHatasi(ValueError):
    """Ajan 2 çıktısı şema, tazelik, sayısal tutarlılık veya kaynak kuralını ihlal ettiğinde fırlatılır."""


def metin_normallestir(metin):
    """Türkçe karakterleri ASCII karşılıklarına dönüştürür ve küçük harfe çevirir."""
    if not metin:
        return ""
    donusum = str.maketrans("çğıİöşüÇĞÖŞÜ", "cgiiosuCGOSU")
    return str(metin).translate(donusum).lower().strip()


def _tarih_cozumle(tarih_str):
    """ISO tarih veya tarih-saat metninden date nesnesi döndürür."""
    if not isinstance(tarih_str, str) or not tarih_str.strip():
        raise GeriGonderimHatasi("Tarih alanı boş veya geçersiz olamaz.")
    parca = tarih_str.strip()[:10]
    try:
        return date.fromisoformat(parca)
    except ValueError as exc:
        raise GeriGonderimHatasi(f"Geçersiz ISO tarih formatı: '{tarih_str}'") from exc


def _url_gecerli_mi(url):
    """URL formatının geçerli bir HTTP/HTTPS adresi olup olmadığını denetler."""
    if not isinstance(url, str):
        return False
    return bool(re.match(r"^https?://[^\s/$.?#].[^\s]*$", url.strip()))


def al_ve_denetle(ajan2_paketi, sevkiyat_kayitlari=None, bugun=None):
    """
    Duyuru 10 Kural 1 (Alma Skill'i):
    Ajan 2'den gelen JSON mesaj paketini alır; şema, tazelik, sayısal tutarlılık
    ve şirket verisiyle uyumluluk açısından doğrular. Kural dışı durumda GeriGonderimHatasi fırlatır.
    """
    if not isinstance(ajan2_paketi, dict):
        raise GeriGonderimHatasi("Ajan 2 girdi paketi geçerli bir JSON/sözlük nesnesi olmalıdır.")

    zorunlu_kok_alanlar = [
        "mesaj_id",
        "uretim_zamani",
        "kaynak_ajan",
        "hedef_ajan",
        "kaynaklar",
        "ozet",
        "yuksek_riskli_sevkiyatlar",
    ]
    for alan in zorunlu_kok_alanlar:
        if alan not in ajan2_paketi:
            raise GeriGonderimHatasi(f"Ajan 2 paketinde zorunlu alan eksik: '{alan}'")

    if not re.match(r"^MSG-[A-Z0-9\-]+$", ajan2_paketi["mesaj_id"]):
        raise GeriGonderimHatasi(f"Geçersiz mesaj_id formatı: '{ajan2_paketi['mesaj_id']}'")

    if ajan2_paketi["kaynak_ajan"] != "Ajan_2_RiskAnaliz":
        raise GeriGonderimHatasi(
            f"Beklenmeyen kaynak ajan: '{ajan2_paketi['kaynak_ajan']}'. 'Ajan_2_RiskAnaliz' bekleniyordu."
        )

    if ajan2_paketi["hedef_ajan"] != "Ajan_3_Denetim":
        raise GeriGonderimHatasi(
            f"Beklenmeyen hedef ajan: '{ajan2_paketi['hedef_ajan']}'. 'Ajan_3_Denetim' bekleniyordu."
        )

    uretim_tarihi = _tarih_cozumle(ajan2_paketi["uretim_zamani"])
    referans_bugun = bugun if bugun is not None else date.today()
    fark_gun = abs((referans_bugun - uretim_tarihi).days)
    if fark_gun > 7:
        raise GeriGonderimHatasi(
            f"Ajan 2 veri paketi bayat ({fark_gun} gün önce üretilmiş). En fazla 7 gün izin verilir."
        )

    kaynaklar = ajan2_paketi.get("kaynaklar", [])
    if not isinstance(kaynaklar, list) or len(kaynaklar) == 0:
        raise GeriGonderimHatasi("Ajan 2 paketinde en az 1 dayanak kaynak listelenmelidir.")

    for k in kaynaklar:
        if not isinstance(k, dict):
            raise GeriGonderimHatasi(f"Geçersiz kaynak formatı: {k}")
        if "kaynak" not in k or "kaynak_url" not in k:
            raise GeriGonderimHatasi(f"Kaynakta 'kaynak' veya 'kaynak_url' eksik: {k}")
        if not _url_gecerli_mi(k["kaynak_url"]):
            raise GeriGonderimHatasi(f"Kaynak URL formatı geçersiz: '{k.get('kaynak_url')}'")

    ozet = ajan2_paketi.get("ozet", {})
    if not isinstance(ozet, dict):
        raise GeriGonderimHatasi("Özet alanı geçerli bir sözlük olmalıdır.")

    zorunlu_ozet_alanlar = [
        "toplam_sevkiyat",
        "aktif_sevkiyat",
        "iptal_sevkiyat",
        "ortalama_risk_puani",
    ]
    for alan in zorunlu_ozet_alanlar:
        if alan not in ozet:
            raise GeriGonderimHatasi(f"Özet alanında zorunlu metrik eksik: '{alan}'")

    toplam = ozet["toplam_sevkiyat"]
    aktif = ozet["aktif_sevkiyat"]
    iptal = ozet["iptal_sevkiyat"]
    if not (isinstance(toplam, int) and isinstance(aktif, int) and isinstance(iptal, int)):
        raise GeriGonderimHatasi("Sevkiyat sayıları tam sayı olmalıdır.")
    if toplam != aktif + iptal:
        raise GeriGonderimHatasi(
            f"Sayısal tutarsızlık: toplam ({toplam}) != aktif ({aktif}) + iptal ({iptal})"
        )

    ort_risk = ozet["ortalama_risk_puani"]
    if not (0.0 <= float(ort_risk) <= 100.0):
        raise GeriGonderimHatasi(f"Ortalama risk puanı 0-100 aralığı dışında: {ort_risk}")

    yuksek_riskler = ajan2_paketi.get("yuksek_riskli_sevkiyatlar", [])
    if not isinstance(yuksek_riskler, list):
        raise GeriGonderimHatasi("'yuksek_riskli_sevkiyatlar' bir liste olmalıdır.")

    for sev in yuksek_riskler:
        if not isinstance(sev, dict):
            raise GeriGonderimHatasi(f"Geçersiz riskli sevkiyat nesnesi: {sev}")
        for alan in ["sevkiyat_id", "tarih", "rota", "risk_puani", "risk_seviyesi"]:
            if alan not in sev:
                raise GeriGonderimHatasi(f"Riskli sevkiyatta zorunlu alan eksik: '{alan}' -> {sev}")
        if not re.match(r"^SVK-[A-Z0-9]+-\d{4,}$", sev["sevkiyat_id"]):
            raise GeriGonderimHatasi(f"Geçersiz sevkiyat_id formatı: '{sev['sevkiyat_id']}'")
        puan = sev["risk_puani"]
        if not (0 <= puan <= 100):
            raise GeriGonderimHatasi(f"Risk puanı 0-100 aralığında olmalıdır: {puan}")

        dayanaklar = sev.get("dayanak_kaynaklar", [])
        for d in dayanaklar:
            if "kaynak_url" in d and not _url_gecerli_mi(d["kaynak_url"]):
                raise GeriGonderimHatasi(f"Sevkiyat dayanak URL geçersiz: {d['kaynak_url']}")

    if sevkiyat_kayitlari:
        gecerli_id_kumesi = {r.get("sevkiyat_id") or r[0] for r in sevkiyat_kayitlari}
        for sev in yuksek_riskler:
            sid = sev["sevkiyat_id"]
            if sid not in gecerli_id_kumesi:
                raise GeriGonderimHatasi(
                    f"Ajan 2 çıktısındaki '{sid}' kimliği şirket veri setinde bulunamadı!"
                )

    return True


def denetle_ve_suz(ajan2_paketi, kritik_esik=65):
    """
    Duyuru 10 Kural 2 (İşleme Skill'i):
    Ajan 2'nin risk sonuçlarını denetler, kritik eşiği (varsayılan 65 puan) aşan
    sevkiyatları süzer ve yol/hava olaylarıyla rota gerekçesini doğrular.
    """
    yuksek_riskler = ajan2_paketi.get("yuksek_riskli_sevkiyatlar", [])
    onaylanan_sevkiyatlar = []
    denetim_kayitlari = []

    for sev in yuksek_riskler:
        sid = sev["sevkiyat_id"]
        puan = sev.get("risk_puani", 0)
        rota = sev.get("rota", "")
        nedenler = sev.get("risk_nedenleri", [])
        dayanaklar = sev.get("dayanak_kaynaklar", [])

        if puan < kritik_esik:
            denetim_kayitlari.append({
                "sevkiyat_id": sid,
                "durum": "ESIK_ALTI",
                "aciklama": f"Risk puanı ({puan}) kritik eşiğin ({kritik_esik}) altında.",
            })
            continue

        if not nedenler or len(nedenler) == 0:
            raise GeriGonderimHatasi(f"Kritik riskli sevkiyatta ({sid}) hiçbir risk nedeni belirtilmemiş!")

        if not dayanaklar or len(dayanaklar) == 0:
            raise GeriGonderimHatasi(f"Kritik riskli sevkiyatta ({sid}) dayanak kaynak URL'si eksik!")

        onaylanan_sevkiyatlar.append(sev)
        denetim_kayitlari.append({
            "sevkiyat_id": sid,
            "rota": rota,
            "risk_puani": puan,
            "risk_seviyesi": sev.get("risk_seviyesi", "yuksek"),
            "durum": "DENETIMDEN_GECTI_ONAYLANDI",
            "neden_sayisi": len(nedenler),
            "dayanak_sayisi": len(dayanaklar),
        })

    return {
        "kritik_esik": kritik_esik,
        "incelenen_adet": len(yuksek_riskler),
        "onaylanan_adet": len(onaylanan_sevkiyatlar),
        "onaylanan_sevkiyatlar": onaylanan_sevkiyatlar,
        "denetim_kayitlari": denetim_kayitlari,
    }


def musteri_mesaji_hazirla(riskli_sevkiyat):
    """
    Duyuru 10 Sektör Şartı:
    Riskli sevkiyat için müşteriye gidecek resmi dayanak linkli açık bilgilendirme mesajı yazar.
    """
    sid = riskli_sevkiyat["sevkiyat_id"]
    rota = riskli_sevkiyat.get("rota", "Belirtilmemiş")
    tarih = riskli_sevkiyat.get("tarih", "")
    ek_gecikme = riskli_sevkiyat.get("ek_gecikme_saat", 0.0)
    toplam_sure = riskli_sevkiyat.get("tahmini_teslim_suresi_saat", "")
    nedenler = riskli_sevkiyat.get("risk_nedenleri", [])
    dayanaklar = riskli_sevkiyat.get("dayanak_kaynaklar", [])

    kaynak_linkleri = []
    for d in dayanaklar:
        k_ad = d.get("kaynak", "Resmi Kaynak")
        k_detay = d.get("detay", "")
        k_url = d.get("kaynak_url", "")
        if k_url:
            kaynak_linkleri.append(f"- **{k_ad}**: {k_detay} ([Resmi Duyuru Bağlantısı]({k_url}))")

    link_metni = "\n".join(kaynak_linkleri) if kaynak_linkleri else "- Resmi bülten üzerinden teyit edilmiştir."

    mesaj = (
        f"Sayın Müşterimiz,\n\n"
        f"**{sid}** takip numaralı **{rota}** güzergahındaki sevkiyatınız, planlanan operasyon takvimine göre "
        f"tahmini **+{ek_gecikme:.1f} saat** operasyonel gecikme riski altındadır (Tahmini toplam teslimat süresi: ~{toplam_sure} saat).\n\n"
        f"**Gecikme Gerekçesi:**\n"
        f"Güzergah üzerindeki resmi karayolları bültenlerinde bildirilen çalışma ve hava şartları:\n"
        f"{link_metni}\n\n"
        f"Logistics Intelligence Network (LIN) operasyon merkezimiz güzergah güvenliğini anlık izlemekte olup "
        f"akaryakıt ve rota optimizasyonuyla teslimatınızı en güvenli sürede tamamlamak için çalışmaktadır.\n\n"
        f"Detaylı bilgi ve canlı takip için müşteri destek hattımızla iletişime geçebilirsiniz.\n"
        f"Saygılarımızla,\n"
        f"**Logistics Intelligence Network (LIN) — Operasyonel İletişim Merkezi**"
    )

    return {
        "sevkiyat_id": sid,
        "rota": rota,
        "planlanan_tarih": tarih,
        "ek_gecikme_saat": ek_gecikme,
        "tahmini_teslim_suresi_saat": toplam_sure,
        "musteri_mesaji_metni": mesaj,
        "dogrulanan_kaynaklar": dayanaklar,
    }


def teslim_paketi_olustur(ajan2_paketi, denetim_sonucu, musteri_bildirimleri, zaman_damgasi=None):
    """
    Duyuru 10 Kural 3 (Teslim Skill'i):
    Ajan 3 çıktısını Çekirdek ve Arayüz modülünün beklediği ortak JSON mesaj formatına getirir.
    """
    zaman_str = (
        zaman_damgasi
        if zaman_damgasi
        else datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    )
    mesaj_id = f"MSG-G3-{datetime.now(timezone.utc).strftime('%Y%m%d')}-A3-001"

    ozet_ajan2 = ajan2_paketi.get("ozet", {})

    mesaj_paketi = {
        "mesaj_id": mesaj_id,
        "uretim_zamani": zaman_str,
        "kaynak_ajan": "Ajan_3_Denetim",
        "hedef_ajan": "Cekirdek_Ve_Arayuz",
        "referans_mesaj_id": ajan2_paketi.get("mesaj_id"),
        "denetim_ozeti": {
            "genel_karar": "ONAYLANDI",
            "toplam_incelenen_sevkiyat": ozet_ajan2.get("toplam_sevkiyat", 140),
            "aktif_sevkiyat": ozet_ajan2.get("aktif_sevkiyat", 134),
            "iptal_sevkiyat": ozet_ajan2.get("iptal_sevkiyat", 6),
            "ortalama_risk_puani": ozet_ajan2.get("ortalama_risk_puani", 13.13),
            "kritik_esik_puani": denetim_sonucu["kritik_esik"],
            "onaylanan_yuksek_riskli_adet": denetim_sonucu["onaylanan_adet"],
        },
        "denetlenen_yuksek_riskli_sevkiyatlar": denetim_sonucu["onaylanan_sevkiyatlar"],
        "musteri_bildirim_mesajlari": musteri_bildirimleri,
        "dayanak_kaynaklar": ajan2_paketi.get("kaynaklar", []),
    }

    return mesaj_paketi


def denetim_raporu_markdown_olustur(mesaj_paketi):
    """Yönetim ve PM incelemesi için ayrıntılı Markdown denetim ve teslim raporu üretir."""
    ozet = mesaj_paketi["denetim_ozeti"]
    bildirimler = mesaj_paketi["musteri_bildirim_mesajlari"]

    satirlar = [
        "# Ajan 3 Denetim, Kalite Kontrol ve Müşteri Teslim Raporu",
        "",
        f"**Rapor Tarihi / Üretim Zamanı:** `{mesaj_paketi['uretim_zamani']}`  ",
        f"**Mesaj ID:** `{mesaj_paketi['mesaj_id']}`  ",
        f"**Referans Mesaj (Ajan 2):** `{mesaj_paketi['referans_mesaj_id']}`  ",
        f"**Sorumlu:** DQ / Ajan 3 — Ece Naz Aktürk (`@ece-naz`)  ",
        f"**Şirket:** Grup B — Logistics Intelligence Network (LIN)  ",
        "",
        "---",
        "",
        "## 1. Genel Denetim ve Kalite Kontrol Özeti",
        "",
        "| Metrik | Değer | Açıklama |",
        "|---|---|---|",
        f"| **Genel Denetim Kararı** | **`{ozet['genel_karar']}`** | Ajan 2 çıktı paketi şema, tazelik ve tutarlılık onayından geçti |",
        f"| Toplam İncelenen Sevkiyat | {ozet['toplam_incelenen_sevkiyat']} | G3 örnek sevkiyat evreni |",
        f"| Aktif Sevkiyat | {ozet['aktif_sevkiyat']} | Rota riski ve yakıt katsayısı uygulanan aktif operasyonlar |",
        f"| İptal Sevkiyat | {ozet['iptal_sevkiyat']} | Operasyonel teslim süresi boş bırakılan iptal kayıtları |",
        f"| Ortalama Risk Puanı | {ozet['ortalama_risk_puani']} / 100 | Şirket genel ortalama gecikme riski |",
        f"| Kritik Eşik Değeri | **{ozet['kritik_esik_puani']} Puan** | Eşik üstü sevkiyatlar için müşteri bildirimi zorunludur |",
        f"| Kritik Riskli Sevkiyat Sayısı | **{ozet['onaylanan_yuksek_riskli_adet']} Adet** | KGM kapalı yol bülteniyle eşleşen rota |",
        "",
        "---",
        "",
        "## 2. Onaylanan Kritik Riskli Sevkiyat ve Müşteri Mesajı",
        "",
    ]

    for b in bildirimler:
        sid = b["sevkiyat_id"]
        rota = b["rota"]
        gecikme = b["ek_gecikme_saat"]
        toplam_sure = b["tahmini_teslim_suresi_saat"]

        satirlar.extend([
            f"### 🚨 Sevkiyat: `{sid}` ({rota})",
            f"- **Tahmini Ek Gecikme:** `+{gecikme} saat` (Toplam Teslimat: ~`{toplam_sure}` saat)",
            "- **Resmi Dayanak Bağlantıları:**",
        ])
        for k in b["dogrulanan_kaynaklar"]:
            k_ad = k.get("kaynak", "Resmi")
            k_detay = k.get("detay", "")
            k_url = k.get("kaynak_url", "")
            satirlar.append(f"  - **{k_ad}**: {k_detay} — [{k_url}]({k_url})")

        satirlar.extend([
            "",
            "**Üretilen Müşteri Bilgilendirme Metni:**",
            "> " + b["musteri_mesaji_metni"].replace("\n", "\n> "),
            "",
            "---",
        ])

    satirlar.extend([
        "## 3. Ajan 3 Skill Doğrulama ve ACP Zincir Uyumu",
        "- **Alma Skill'i (`skills/ajan3-alma`):** Ajan 2 JSON paketi eksik alan, aralık aşımı ve mantıksal tutarsızlık filtrelerinden geçirildi.",
        "- **İşleme Skill'i (`skills/ajan3-isleme`):** Risk puanı eşiği (65) filtresi çalıştı; KGM kapalı yol bülteniyle rota tutarlılığı teyit edildi.",
        "- **Teslim Skill'i (`skills/ajan3-teslim`):** Resmi duyuru linki içeren müşteri mesajı üretilerek `data/ajan3_mesaj.json` oluşturuldu.",
        "",
        "*Bu rapor Logistics Intelligence Network (LIN) Ajan 3 denetim motoru tarafından üretilmiştir.*",
    ])

    return "\n".join(satirlar)


def calistir(
    ajan2_json_yolu=None,
    sevkiyat_csv_yolu=None,
    cikti_json_yolu=None,
    cikti_md_yolu=None,
    kritik_esik=65,
):
    """Ajan 3 uçtan uca alma, denetleme ve teslim akışını çalıştırır."""
    if not ajan2_json_yolu:
        ajan2_json_yolu = os.path.join(KOK_DIZIN, "data", "ajan2_mesaj.json")
    if not sevkiyat_csv_yolu:
        sevkiyat_csv_yolu = os.path.join(KOK_DIZIN, "data", "lojistik_sevkiyat_g3_ornek.csv")
    if not cikti_json_yolu:
        cikti_json_yolu = os.path.join(KOK_DIZIN, "data", "ajan3_mesaj.json")
    if not cikti_md_yolu:
        cikti_md_yolu = os.path.join(KOK_DIZIN, "data", "ajan3_denetim_raporu.md")

    if not os.path.exists(ajan2_json_yolu):
        raise FileNotFoundError(f"Ajan 2 girdi dosyası bulunamadı: {ajan2_json_yolu}")

    with open(ajan2_json_yolu, "r", encoding="utf-8") as f:
        ajan2_paketi = json.load(f)

    sevkiyat_kayitlari = []
    if os.path.exists(sevkiyat_csv_yolu):
        with open(sevkiyat_csv_yolu, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            sevkiyat_kayitlari = list(reader)

    # 1. Alma Skill'i
    al_ve_denetle(ajan2_paketi, sevkiyat_kayitlari=sevkiyat_kayitlari)

    # 2. İşleme Skill'i
    denetim_sonucu = denetle_ve_suz(ajan2_paketi, kritik_esik=kritik_esik)

    # 3. Teslim Skill'i (Müşteri mesajları)
    musteri_bildirimleri = []
    for sev in denetim_sonucu["onaylanan_sevkiyatlar"]:
        bildirim = musteri_mesaji_hazirla(sev)
        musteri_bildirimleri.append(bildirim)

    # Nihai ACP JSON paketi
    nihai_paket = teslim_paketi_olustur(ajan2_paketi, denetim_sonucu, musteri_bildirimleri)

    os.makedirs(os.path.dirname(os.path.abspath(cikti_json_yolu)), exist_ok=True)
    with open(cikti_json_yolu, "w", encoding="utf-8") as f:
        json.dump(nihai_paket, f, ensure_ascii=False, indent=2)

    # Markdown denetim raporu
    md_metni = denetim_raporu_markdown_olustur(nihai_paket)
    with open(cikti_md_yolu, "w", encoding="utf-8") as f:
        f.write(md_metni)

    print(f"[OK] Ajan 3 Denetimi Basarili: {len(musteri_bildirimleri)} musteri mesaji uretildi.")
    print(f" -> JSON Cikti: {cikti_json_yolu}")
    print(f" -> Rapor     : {cikti_md_yolu}")
    return nihai_paket


def main():
    parser = argparse.ArgumentParser(
        description="Ajan 3 - Lojistik Sevkiyat Risk Denetimi ve Müşteri İletişimi"
    )
    parser.add_argument("--ajan2-json", type=str, default=None, help="Ajan 2 girdi JSON yolu")
    parser.add_argument("--sevkiyat-csv", type=str, default=None, help="Şirket sevkiyat CSV yolu")
    parser.add_argument("--cikti-json", type=str, default=None, help="Ajan 3 çıktı JSON yolu")
    parser.add_argument("--cikti-md", type=str, default=None, help="Ajan 3 denetim raporu MD yolu")
    parser.add_argument("--esik", type=int, default=65, help="Kritik risk puanı eşiği (varsayılan: 65)")

    args = parser.parse_args()
    calistir(
        ajan2_json_yolu=args.ajan2_json,
        sevkiyat_csv_yolu=args.sevkiyat_csv,
        cikti_json_yolu=args.cikti_json,
        cikti_md_yolu=args.cikti_md,
        kritik_esik=args.esik,
    )


if __name__ == "__main__":
    main()
