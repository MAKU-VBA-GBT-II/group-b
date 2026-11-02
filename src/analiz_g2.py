#!/usr/bin/env python3
"""
Görev 2: Lojistik Sevkiyat Simülasyon Verisi Analiz Betiği
Rol: DQ (Data Quality) — Ece Naz Aktürk
Depo: MAKU-VBA-GBT-II/group-b
Girdi: data/lojistik_sevkiyat_g2.csv
Çıktı: docs/analiz-g2.md için 5 zorunlu analiz metriği ve özet bulgular
"""

import argparse
import csv
import datetime
import os
import sys
from collections import defaultdict


def analiz_et(csv_yolu):
    if not os.path.exists(csv_yolu):
        print(f"[HATA] CSV dosyası bulunamadı: {csv_yolu}", file=sys.stderr)
        sys.exit(1)

    with open(csv_yolu, mode="r", encoding="utf-8") as f:
        okuyucu = csv.DictReader(f)
        satirlar = list(okuyucu)

    toplam_sevkiyat = len(satirlar)
    if toplam_sevkiyat == 0:
        print("[HATA] CSV dosyası boş!", file=sys.stderr)
        sys.exit(1)

    toplam_ciro = sum(float(r["ucret_tl"]) for r in satirlar)
    iptal_olmayanlar = [r for r in satirlar if r["durum"] != "iptal"]
    iptal_sayisi = toplam_sevkiyat - len(iptal_olmayanlar)
    ortalama_teslim_suresi = sum(float(r["teslim_suresi_saat"]) for r in iptal_olmayanlar) / len(iptal_olmayanlar)
    ortalama_agirlik = sum(float(r["agirlik_kg"]) for r in satirlar) / toplam_sevkiyat

    print("=" * 70)
    print("GRUP-B LOJİSTİK SEVKİYAT ANALİZ RAPORU (GÖREV 2)")
    print("=" * 70)
    print(f"Veri Dosyası           : {csv_yolu}")
    print(f"Toplam Satır (Kayıt)   : {toplam_sevkiyat}")
    print(f"İptal Kayıt Sayısı     : {iptal_sayisi} (%{(iptal_sayisi / toplam_sevkiyat) * 100:.1f})")
    print(f"Toplam Ciro (Navlun)   : {toplam_ciro:,.2f} TL")
    print(f"Ortalama Ağırlık       : {ortalama_agirlik:.2f} kg")
    print(f"Ortalama Teslim Süresi : {ortalama_teslim_suresi:.2f} saat (İptaller hariç {len(iptal_olmayanlar)} kayıt üzerinden)")
    print("=" * 70)

    # 1. Mod Kırılımı
    mod_istatistik = defaultdict(lambda: {"toplam": 0, "zamaninda": 0, "gecikmeli": 0, "iptal": 0, "ciro": 0.0})
    for r in satirlar:
        m = r["tasima_modu"]
        mod_istatistik[m]["toplam"] += 1
        mod_istatistik[m]["ciro"] += float(r["ucret_tl"])
        d = r["durum"]
        mod_istatistik[m][d] += 1

    print("\n[METRİK 4] TAŞIMA MODUNA GÖRE SEVKİYAT VE GECİKME KIRILIMI:")
    print("-" * 75)
    print(f"{'Taşıma Modu':<12} {'Toplam':<8} {'Zamanında':<10} {'Gecikmeli':<10} {'İptal':<8} {'Gecikme %':<10} {'Ciro (TL)':<15}")
    print("-" * 75)
    for m, s in sorted(mod_istatistik.items()):
        payda = s["zamaninda"] + s["gecikmeli"]
        gecikme_orani = (s["gecikmeli"] / payda * 100) if payda > 0 else 0.0
        print(f"{m:<12} {s['toplam']:<8} {s['zamaninda']:<10} {s['gecikmeli']:<10} {s['iptal']:<8} %{gecikme_orani:<9.1f} {s['ciro']:<15,.2f}")

    # 2. Haftalık Zaman Serisi (ISO Haftası)
    hafta_istatistik = defaultdict(lambda: {"adet": 0, "ciro": 0.0, "tarihler": []})
    for r in satirlar:
        dt = datetime.date.fromisoformat(r["tarih"])
        iso_yil, iso_hafta, _ = dt.isocalendar()
        anahtar = f"{iso_yil}-W{iso_hafta:02d}"
        hafta_istatistik[anahtar]["adet"] += 1
        hafta_istatistik[anahtar]["ciro"] += float(r["ucret_tl"])
        hafta_istatistik[anahtar]["tarihler"].append(r["tarih"])

    print("\n[METRİK 3] HAFTALIK SEVKİYAT HACMİ VE GELİR TRENDİ (ZAMAN SERİSİ):")
    print("-" * 75)
    print(f"{'Hafta':<12} {'Tarih Aralığı':<25} {'Sevkiyat':<10} {'Haftalık Ciro (TL)':<20}")
    print("-" * 75)
    for h in sorted(hafta_istatistik.keys()):
        w = hafta_istatistik[h]
        tarih_araligi = f"{min(w['tarihler'])} / {max(w['tarihler'])}"
        print(f"{h:<12} {tarih_araligi:<25} {w['adet']:<10} {w['ciro']:<20,.2f}")

    # 3. Top-5 Rota
    rota_istatistik = defaultdict(lambda: {"adet": 0, "ciro": 0.0})
    for r in satirlar:
        rt = f"{r['cikis_sehri']} -> {r['varis_sehri']}"
        rota_istatistik[rt]["adet"] += 1
        rota_istatistik[rt]["ciro"] += float(r["ucret_tl"])

    top5_rota = sorted(rota_istatistik.items(), key=lambda x: x[1]["adet"], reverse=True)[:5]
    print("\n[METRİK 5] EN YOĞUN TOP-5 SEVKİYAT ROTASI:")
    print("-" * 75)
    print(f"{'Sıra':<6} {'Rota':<30} {'Sevkiyat Adedi':<16} {'Hacim Payı %':<14} {'Toplam Gelir (TL)':<15}")
    print("-" * 75)
    for i, (rt, s) in enumerate(top5_rota, start=1):
        pay = (s["adet"] / toplam_sevkiyat) * 100
        print(f"{i:<6} {rt:<30} {s['adet']:<16} %{pay:<13.1f} {s['ciro']:<15,.2f}")
    print("=" * 75)


def main():
    varsayilan_yol = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "lojistik_sevkiyat_g2.csv"
    )

    parser = argparse.ArgumentParser(description="Görev 2 Analiz Betiği — LIN Group-B")
    parser.add_argument(
        "--csv-yolu",
        type=str,
        default=varsayilan_yol,
        help="Analiz edilecek CSV dosya yolu (Varsayılan: data/lojistik_sevkiyat_g2.csv)"
    )
    args = parser.parse_args()
    analiz_et(args.csv_yolu)


if __name__ == "__main__":
    main()
