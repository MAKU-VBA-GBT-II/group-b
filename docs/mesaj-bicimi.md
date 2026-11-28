# Ortak Mesaj Biçimi Belgesi — Çok Ajanlı Şirket Programı (Görev 3)

**Şirket:** Grup B — Logistics Intelligence Network (LIN)  
**Tarih:** 28 Kasım 2026  
**Sürüm:** v1.0 (İnşa Haftası 1 — Duyuru 11 Uyumlu)  
**İlgili Issue:** [#73](https://github.com/MAKU-VBA-GBT-II/group-b/issues/73)  
**Taraflar:** Ajan 1 (Web Veri Toplayıcı), Ajan 2 (Risk Analiz Motoru), Ajan 3 (Denetim & Teslim)

---

## 1. Genel Kurallar ve İlkeler

1. **İletişim Standardı:** Tüm ajanlar arası veri aktarımı `data/` altındaki doğrulanmış JSON paketleri (ve tamamlayıcı CSV raporları) üzerinden yürütülür.
2. **İzlenebilirlik:** Her veri nesnesinde zorunlu olarak `kaynak`, `kaynak_url` ve `erisim_tarihi` / `uretim_zamani` bilgisi bulunur.
3. **Standart Zarf Yapısı:** Her mesaj standart bir üst zarfa (`mesaj_id`, `uretim_zamani`, `kaynak_ajan`, `hedef_ajan`, `durum`, `veri`) sahiptir.
4. **Geri Gönderme (Red) Protokolü:** Girdiyi alan ajan, şema, eksik alan, bayat veri (> 3 gün) veya birim uyumsuzluğu tespit ettiğinde standart red zarfı ile işi gerekçeli olarak önceki ajana geri gönderir.

---

## 2. Ajan 1 → Ajan 2 Çıktı Biçimi (`data/ornek-ajan1.json`)

Ajan 1 (Web Veri Toplayıcı), dış kamu/piyasa kaynaklarından (MGM, KGM, Akaryakıt) topladığı verileri bu formatta iletir:

```json
{
  "mesaj_id": "MSG-G3-20261128-A1-001",
  "uretim_zamani": "2026-11-28T09:00:00Z",
  "kaynak_ajan": "Ajan_1_WebToplayici",
  "hedef_ajan": "Ajan_2_RiskAnaliz",
  "durum": "onay",
  "veri": {
    "mgm_uyarilari": [
      {
        "il": "Trabzon",
        "seviye": "turuncu",
        "tur": "yogun_kar",
        "kaynak": "MGM",
        "kaynak_url": "https://www.mgm.gov.tr/Meteouyari/turkiye.aspx?Gun=1",
        "erisim_tarihi": "2026-11-28"
      }
    ],
    "kgm_yol_durumu": [
      {
        "guzergah": "Ilgar Geçidi",
        "durum": "kapali",
        "neden": "kar_ve_tipi",
        "kaynak": "KGM",
        "kaynak_url": "https://www.kgm.gov.tr/Sayfalar/KGM/SiteTr/YolDanisma/GunlukYolDurumuBulteni.aspx",
        "erisim_tarihi": "2026-11-28"
      }
    ],
    "akaryakit_fiyatlari": [
      {
        "il": "Trabzon",
        "urun": "motorin",
        "fiyat_tl": 86.50,
        "birim": "TL/LT",
        "kaynak": "AKARYAKIT",
        "kaynak_url": "https://www.petrolofisi.com.tr/akaryakit-fiyatlari",
        "erisim_tarihi": "2026-11-28"
      }
    ]
  }
}
```

### Alan Tanımları
- `mesaj_id`: `MSG-G3-YYYYMMDD-A1-XXX` formatında benzersiz mesaj kimliği.
- `uretim_zamani`: ISO-8601 UTC formatında üretim zaman damgası.
- `durum`: `"onay"` (başarılı veri paketi) veya `"red"`.
- `veri.mgm_uyarilari[]`: `il` (String), `seviye` (`sari`|`turuncu`|`kirmizi`), `tur` (String), `kaynak_url` (URL), `erisim_tarihi` (YYYY-MM-DD).
- `veri.kgm_yol_durumu[]`: `guzergah` (String), `durum` (`kapali`|`tek_serit`), `neden` (String), `kaynak_url` (URL), `erisim_tarihi` (YYYY-MM-DD).
- `veri.akaryakit_fiyatlari[]`: `il` (String), `urun` (String), `fiyat_tl` (Float, pozitif), `birim` (`"TL/LT"` zorunlu), `kaynak_url` (URL), `erisim_tarihi` (YYYY-MM-DD).

---

## 3. Ajan 2 → Ajan 3 Çıktı Biçimi (`data/ornek-ajan2.json`)

Ajan 2 (Risk Analiz Motoru), Ajan 1 dış verilerini şirket içi sentetik sevkiyatlarla birleştirerek rota risk puanları ve tahmini gecikmeleri hesaplar:

```json
{
  "mesaj_id": "MSG-G3-20261128-A2-001",
  "uretim_zamani": "2026-11-28T09:30:00Z",
  "kaynak_ajan": "Ajan_2_RiskAnaliz",
  "hedef_ajan": "Ajan_3_Denetim",
  "referans_mesaj_id": "MSG-G3-20261128-A1-001",
  "durum": "onay",
  "kaynaklar": [
    {
      "kaynak": "KGM",
      "kaynak_url": "https://www.kgm.gov.tr/Sayfalar/KGM/SiteTr/YolDanisma/GunlukYolDurumuBulteni.aspx",
      "erisim_tarihi": "2026-11-28"
    },
    {
      "kaynak": "AKARYAKIT",
      "kaynak_url": "https://www.petrolofisi.com.tr/akaryakit-fiyatlari",
      "erisim_tarihi": "2026-11-28"
    }
  ],
  "ozet": {
    "toplam_sevkiyat": 140,
    "aktif_sevkiyat": 134,
    "iptal_sevkiyat": 6,
    "yuksek_ve_kritik_risk_sayisi": 1,
    "ortalama_risk_puani": 13.13,
    "ortalama_motorin_tl": 86.1,
    "genel_yakit_carpani": 1.0129,
    "en_riskli_rotalar": [
      {
        "rota": "Gaziantep -> Trabzon",
        "aktif_sevkiyat": 1,
        "ortalama_risk_puani": 55.0,
        "yuksek_riskli_adet": 0
      }
    ]
  },
  "yuksek_riskli_sevkiyatlar": [
    {
      "sevkiyat_id": "SVK-G3-0017",
      "tarih": "2026-11-20",
      "rota": "Trabzon -> Adana",
      "tasima_modu": "kara",
      "durum": "gecikmeli",
      "baz_ucret_tl": "1479.10",
      "yakit_etkili_ucret_tl": "1505.23",
      "risk_puani": 65,
      "risk_seviyesi": "yuksek",
      "ek_gecikme_saat": 12.0,
      "tahmini_teslim_suresi_saat": "53.5",
      "risk_nedenleri": ["operasyonel_gecikme", "kgm_kapali_Ilgar Geçidi"],
      "dayanak_kaynaklar": [
        {
          "kaynak": "KGM",
          "detay": "Ilgar Geçidi (kapali)",
          "kaynak_url": "https://www.kgm.gov.tr/Sayfalar/KGM/SiteTr/YolDanisma/GunlukYolDurumuBulteni.aspx",
          "erisim_tarihi": "2026-11-28"
        }
      ]
    }
  ]
}
```

---

## 4. Standart Geri Gönderme (Red) Zarfı

Bir ajan (Ajan 2 veya Ajan 3) gelen paketi doğrularken kural ihlali (eksik alan, bayat veri, uyumsuz birim veya mantıksal tutarsızlık) bulursa, aşağıdaki standart red paketini üretir:

```json
{
  "mesaj_id": "MSG-G3-20261128-RED-001",
  "uretim_zamani": "2026-11-28T09:15:00Z",
  "kaynak_ajan": "Ajan_2_RiskAnaliz",
  "hedef_ajan": "Ajan_1_WebToplayici",
  "referans_mesaj_id": "MSG-G3-20261128-A1-001",
  "durum": "red",
  "gerekce": "Akaryakıt verisinde birim uyumsuzluğu tespit edildi: 'USD/GAL' bulundu, beklenen 'TL/LT'.",
  "sorunlu_alanlar": [
    "veri.akaryakit_fiyatlari[0].birim"
  ],
  "hata_kodu": "ERR_UNIT_MISMATCH"
}
```

### Red Zarfı Alanları
| Alan Adı | Tip | Zorunlu | Açıklama |
|---|---|:---:|---|
| `mesaj_id` | String | Evet | `MSG-G3-YYYYMMDD-RED-XXX` formatında kimlik |
| `uretim_zamani` | String | Evet | ISO-8601 UTC zaman damgası |
| `kaynak_ajan` | String | Evet | Reddeden ajan (örn: `Ajan_2_RiskAnaliz`, `Ajan_3_Denetim`) |
| `hedef_ajan` | String | Evet | Reddedilen/düzeltmesi istenen ajan (örn: `Ajan_1_WebToplayici`) |
| `referans_mesaj_id` | String | Evet | Reddedilen gelen mesajın kimliği |
| `durum` | String | Evet | Sabit `"red"` |
| `gerekce` | String | Evet | İnsan ve yapay zeka tarafından okunabilir açık red sebebi |
| `sorunlu_alanlar` | Array[String] | Evet | Hatalı veya eksik alanların JSON path listesi |
| `hata_kodu` | String | Evet | Standart hata kodu (`ERR_SCHEMA_MISSING`, `ERR_STALE_DATA`, `ERR_UNIT_MISMATCH`, vb.) |
