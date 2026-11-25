---
name: ajan2-alma
description: Ajan 2 için Ajan 1 web veri paketini ve şirket sevkiyat verisini okur; eksik alan, bayat tarih, uyumsuz birim ve kaynak URL eksiklerini denetler.
---

# ajan2-alma — Ajan 2 Girdi Alma ve Doğrulama Skill'i

## Amaç
Ajan 1'den gelen ortak JSON mesajını (`data/ajan1_mesaj.json`) ve şirket içi sentetik sevkiyat verisini (`data/lojistik_sevkiyat_g3_ornek.csv`) alır; `docs/veri-sozlugu.md` (v3.0) ile Duyuru 10 tazelik/birim kurallarına göre kontrol eder. Eksik veya tutarsız girdi tespit edilirse işi gerekçesiyle Ajan 1'e geri gönderir.

## Girdiler
- Ajan 1 mesaj paketi: `--ajan1-json` (varsayılan `data/ajan1_mesaj.json`)
- Sevkiyat veri seti: `--sevkiyat-csv` (varsayılan `data/lojistik_sevkiyat_g3_ornek.csv`)
- Tazelik sınırı: `--max-yas-gun` (varsayılan `3` gün)

## Kontrol Kuralları
1. **Zorunlu Zarf Alanları:** `mesaj_id`, `uretim_zamani`, `kaynak_ajan`, `hedef_ajan`, `veri` alanları boş olamaz.
2. **Tazelik Denetimi:** `uretim_zamani` ve dış kaynak `erisim_tarihi` değerleri referans tarihten `max_yas_gun` günden eski olamaz.
3. **Birim & Değer Denetimi:** `akaryakit_fiyatlari` boş olamaz; her kayıtta `birim == "TL/LT"` ve `fiyat_tl > 0` olmalıdır.
4. **Kaynak İzlenebilirliği:** Her MGM, KGM ve akaryakıt kaydında geçerli `http://` veya `https://` `kaynak_url` bulunmalıdır.
5. **Sevkiyat Şeması:** CSV dosyası v3.0 10 sütununa uymalı, `cikis_sehri != varis_sehri` olmalı, ücrette virgül ondalık bulunmamalı ve `iptal` satırlarında `teslim_suresi_saat` boş olmalıdır.

## Nasıl Çalıştırılır
```bash
python src/ajan2_risk.py --ajan1-json data/ajan1_mesaj.json --sevkiyat-csv data/lojistik_sevkiyat_g3_ornek.csv
```

## Geri Gönderim (Reddetme) Durumları
Aşağıdaki durumlarda `GeriGonderimHatasi` üretilir ve süreç çıkış kodu `2` ile Ajan 1'e iade edilir:
1. Bayat tarih (`(referans_tarih - veri_tarihi).days > 3`).
2. `TL/LT` dışı uyumsuz akaryakıt birimi veya sıfır/negatif fiyat.
3. `kaynak_url` eksikliği veya şema dışı CSV formatı.
