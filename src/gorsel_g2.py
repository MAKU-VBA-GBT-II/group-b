"""FE (Grup B, Görev 2): 3 grafik üretici.

Girdi : data/lojistik_sevkiyat_g2.csv  (şema: docs/veri-sozlugu.md v2.0)
Çıktı : visuals/zaman_serisi_haftalik.png
        visuals/mod_gecikme_kirilimi.png
        visuals/teslimat_suresi_dagilimi.png
Veri dosyası yoksa yalnızca iskelet testi için ÖRNEK veri kullanılır ve
grafiklerin köşesine "ÖRNEK VERİ" yazılır.
Kararlar (DQ, #48): hafta = Pazartesi başlangıçlı ISO haftası; sevkiyat
sayısına iptaller dahil; gecikme oranı = gecikmeli / (zamaninda + gecikmeli) * 100.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

KOK = Path(__file__).resolve().parent.parent
VERI_YOLU = KOK / "data" / "lojistik_sevkiyat_g2.csv"
CIKTI = KOK / "visuals"

MODLAR = ["kara", "deniz", "hava", "demiryolu"]
GEREKLI = ["tarih", "tasima_modu", "durum", "teslim_suresi_saat", "ucret_tl"]
MAVI = "#378ADD"
TURUNCU = "#EF9F27"


def ornek_veri():
    """Yalnızca iskelet testi: şemaya benzeyen sentetik örnek (gerçek veri değil)."""
    rng = np.random.default_rng(42)
    n = 900
    tarih = pd.Timestamp("2026-01-01") + pd.to_timedelta(rng.integers(0, 60, n), unit="D")
    mod = rng.choice(MODLAR, n, p=[0.5, 0.15, 0.15, 0.2])
    durum = rng.choice(["zamaninda", "gecikmeli", "iptal"], n, p=[0.80, 0.15, 0.05])
    sure = np.round(rng.gamma(4.0, 6.0, n) + 4, 1)
    sure = np.where(durum == "iptal", np.nan, sure)
    ucret = np.round(rng.uniform(500, 9000, n), 2)
    return pd.DataFrame(
        {"tarih": tarih, "tasima_modu": mod, "durum": durum,
         "teslim_suresi_saat": sure, "ucret_tl": ucret}
    )


def veri_yukle():
    if VERI_YOLU.exists():
        df = pd.read_csv(VERI_YOLU, parse_dates=["tarih"])
        eksik = [s for s in GEREKLI if s not in df.columns]
        if eksik:
            raise ValueError(f"CSV'de eksik sütun var: {eksik}")
        return df, False
    print("UYARI: data/lojistik_sevkiyat_g2.csv bulunamadı, ÖRNEK veri kullanılıyor.")
    return ornek_veri(), True


def damga(fig, ornek):
    if ornek:
        fig.text(0.99, 0.01, "ÖRNEK VERİ (iskelet testi)", ha="right", fontsize=9, color="#A32D2D")


def tl_bicimi(x, _):
    return f"{x:,.0f}".replace(",", ".")


def haftalik_ozet(df):
    iso = df["tarih"].dt.isocalendar()
    df = df.assign(hafta=iso["year"].astype(str) + "-W" + iso["week"].astype(str).str.zfill(2))
    h = df.groupby("hafta").agg(
        sevkiyat=("tarih", "size"), ciro=("ucret_tl", "sum"), gun=("tarih", "nunique")
    ).reset_index()
    h["etiket"] = h["hafta"].where(h["gun"] >= 7, h["hafta"] + "*")
    return h


def grafik_zaman_serisi(df, ornek):
    h = haftalik_ozet(df)
    fig, (ust, alt) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    ust.plot(h["etiket"], h["sevkiyat"], marker="o", color=MAVI)
    ust.set_ylabel("Sevkiyat sayısı (adet)")
    ust.grid(alpha=0.3)
    alt.plot(h["etiket"], h["ciro"], marker="o", color=MAVI)
    alt.set_ylabel("Navlun geliri (TL)")
    alt.yaxis.set_major_formatter(FuncFormatter(tl_bicimi))
    alt.set_xlabel("Hafta (ISO, Pazartesi başlangıçlı)")
    alt.grid(alpha=0.3)
    fig.suptitle("Haftalık Sevkiyat Hacmi ve Navlun Geliri", fontsize=14, fontweight="bold")
    kisa = h[h["gun"] < 7]
    if not kisa.empty:
        not_metni = "* Eksik hafta: " + ", ".join(
            f"{r.hafta} yalnızca {r.gun} gün" for r in kisa.itertuples()
        )
        fig.text(0.01, 0.01, not_metni, fontsize=9, color="#5F5E5A")
    damga(fig, ornek)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.savefig(CIKTI / "zaman_serisi_haftalik.png", dpi=150)
    plt.close(fig)


def grafik_mod_kirilimi(df, ornek):
    adet = df.groupby("tasima_modu").size().reindex(MODLAR, fill_value=0)
    basarili = df[df["durum"] != "iptal"]
    toplam = basarili.groupby("tasima_modu").size().reindex(MODLAR, fill_value=0)
    geciken = basarili[basarili["durum"] == "gecikmeli"].groupby("tasima_modu").size()
    geciken = geciken.reindex(MODLAR, fill_value=0)
    oran = geciken / toplam.replace(0, np.nan) * 100

    fig, (sol, sag) = plt.subplots(1, 2, figsize=(11, 5))
    sol.bar(MODLAR, adet, color=MAVI)
    sol.bar_label(sol.containers[0])
    sol.set_xlabel("Taşıma modu")
    sol.set_ylabel("Sevkiyat sayısı (adet)")
    sol.set_title("Sevkiyat sayısı (iptaller dahil)", fontsize=11)
    sag.bar(MODLAR, oran, color=TURUNCU)
    sag.bar_label(sag.containers[0], fmt="%.1f")
    sol.set_ylim(0, adet.max() * 1.12)
    sag.set_ylim(0, oran.max() * 1.15)
    sag.set_xlabel("Taşıma modu")
    sag.set_ylabel("Gecikme oranı (%)")
    sag.set_title("Gecikme oranı (iptaller hariç)", fontsize=11)
    fig.suptitle("Taşıma Moduna Göre Sevkiyat Sayısı ve Gecikme Oranı", fontsize=14, fontweight="bold")
    damga(fig, ornek)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.savefig(CIKTI / "mod_gecikme_kirilimi.png", dpi=150)
    plt.close(fig)


def grafik_dagilim(df, ornek):
    sure = df.loc[df["durum"] != "iptal", "teslim_suresi_saat"].dropna()
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.hist(sure, bins=20, color=MAVI, edgecolor="white")
    ort = sure.mean()
    ax.axvline(ort, color=TURUNCU, linestyle="--", label=f"Ortalama: {ort:.1f} saat")
    ax.set_xlabel("Teslim süresi (saat)")
    ax.set_ylabel("Sevkiyat sayısı (adet)")
    ax.set_title("Başarılı Sevkiyatların Teslimat Süresi Dağılımı", fontsize=14, fontweight="bold")
    ax.legend()
    damga(fig, ornek)
    fig.tight_layout()
    fig.savefig(CIKTI / "teslimat_suresi_dagilimi.png", dpi=150)
    plt.close(fig)

def ozet_yazdir(df):
    """Grafiklerde çizilen sayıları yazdırır; docs/analiz-g2.md ile karşılaştırmak için."""
    h = haftalik_ozet(df)
    print("\n[Grafik 1] Haftalık özet (ISO haftası):")
    print(h[["hafta", "gun", "sevkiyat", "ciro"]].to_string(index=False))
    adet = df.groupby("tasima_modu").size().reindex(MODLAR, fill_value=0)
    basarili = df[df["durum"] != "iptal"]
    toplam = basarili.groupby("tasima_modu").size().reindex(MODLAR, fill_value=0)
    geciken = basarili[basarili["durum"] == "gecikmeli"].groupby("tasima_modu").size()
    geciken = geciken.reindex(MODLAR, fill_value=0)
    print("\n[Grafik 2] Mod bazında sevkiyat sayısı (iptaller dahil) ve gecikme oranı:")
    for m in MODLAR:
        oran = geciken[m] / toplam[m] * 100 if toplam[m] else float("nan")
        print(f"  {m}: {adet[m]} adet, gecikme oranı %{oran:.1f}")
    sure = basarili["teslim_suresi_saat"].dropna()
    print(f"\n[Grafik 3] Teslim süresi: {len(sure)} sevkiyat, ortalama {sure.mean():.1f} saat")
    print(f"\nToplam: {len(df)} sevkiyat, ciro {df['ucret_tl'].sum():,.2f} TL")
def main():
    CIKTI.mkdir(exist_ok=True)
    df, ornek = veri_yukle()
    grafik_zaman_serisi(df, ornek)
    grafik_mod_kirilimi(df, ornek)
    grafik_dagilim(df, ornek)
    ozet_yazdir(df)
    kaynak = "ÖRNEK veri" if ornek else "gerçek veri"
    print(f"3 grafik yazıldı ({kaynak}, {len(df)} satır): {CIKTI}")


if __name__ == "__main__":
    main()