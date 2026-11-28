---
name: ajan2-alma
description: Ajan 2 için Ajan 1 web veri paketini ve şirket sevkiyat verisini okur; eksik alan, bayat tarih, uyumsuz birim ve kaynak URL eksiklerini denetler.
---

# ajan2-alma — Ajan 2 Girdi Alma ve Doğrulama Skill'i

## Amaç
Ajan 1'den gelen ortak JSON mesajını (`data/ornek-ajan1.json` veya `data/ajan1_mesaj.json`) ve şirket içi sentetik sevkiyat verisini (`data/lojistik_sevkiyat_g3_ornek.csv`) alır; `docs/mesaj-bicimi.md` ve `docs/veri-sozlugu.md` (v3.0) standartlarına göre doğrular. Eksik, bayat veya uyumsuz veri tespitinde standart red zarfı üreterek işi gerekçesiyle Ajan 1'e geri gönderir.

## Girdiler
- Ajan 1 mesaj paketi: `--ajan1-json` (varsayılan: `data/ornek-ajan1.json`)
- Sevkiyat veri seti: `--sevkiyat-csv` (varsayılan: `data/lojistik_sevkiyat_g3_ornek.csv`)
- Red zarfı çıktı dosyası: `--cikti-red-json` (hata durumunda üretilecek red JSON dosyası)
- Tazelik sınırı: `--max-yas-gun` (varsayılan `3` gün)
- Referans tarih: `--referans-tarih` (opsiyonel YYYY-MM-DD)

## Kontrol Kuralları
1. **Zorunlu Zarf Alanları:** `mesaj_id`, `uretim_zamani`, `kaynak_ajan`, `hedef_ajan`, `veri` alanları boş olamaz (`ERR_MISSING_FIELD`).
2. **Tazelik Denetimi:** `uretim_zamani` ve dış kaynak `erisim_tarihi` değerleri referans tarihten `max_yas_gun` (3 gün) günden eski olamaz (`ERR_STALE_DATA`).
3. **Birim & Değer Denetimi:** `akaryakit_fiyatlari` listesinde her kayıtta `birim == "TL/LT"` ve `fiyat_tl > 0` olmalıdır (`ERR_UNIT_MISMATCH`).
4. **Kaynak İzlenebilirliği:** Her MGM, KGM ve akaryakıt kaydında geçerli `http://` veya `https://` `kaynak_url` bulunmalıdır.
5. **Sevkiyat Şeması:** CSV dosyası v3.0 10 sütununa uymalı, `cikis_sehri != varis_sehri` olmalı, ücrette virgül ondalık bulunmamalı ve `iptal` satırlarında `teslim_suresi_saat` boş olmalıdır.

## Standart Geri Gönderme (Red) Zarfı
Herhangi bir kural ihlal edildiğinde `GeriGonderimHatasi` fırlatılır ve `docs/mesaj-bicimi.md` formatında aşağıdaki red zarfı kaydedilir:
```json
{
  "mesaj_id": "MSG-G3-YYYYMMDD-RED-001",
  "uretim_zamani": "2026-11-28T12:00:00Z",
  "kaynak_ajan": "Ajan_2_RiskAnaliz",
  "hedef_ajan": "Ajan_1_WebToplayici",
  "referans_mesaj_id": "MSG-G3-...",
  "durum": "red",
  "gerekce": "Ajan 1 verisi bayat: ... (> 3 gün).",
  "sorunlu_alanlar": ["uretim_zamani"],
  "hata_kodu": "ERR_STALE_DATA"
}
```

## Nasıl Çalıştırılır
```bash
# Başarılı girdi doğrulama:
python src/ajan2_risk.py --ajan1-json data/ornek-ajan1.json --sevkiyat-csv data/lojistik_sevkiyat_g3_ornek.csv

# Red testi ve red zarfı kaydı:
python src/ajan2_risk.py --ajan1-json data/bozuk_girdi.json --cikti-red-json data/ajan2_red_ornek.json
```
