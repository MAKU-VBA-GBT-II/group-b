---
name: ajan3-alma
description: Ajan 3 için Ajan 2 risk analiz paketini alır; şema, tazelik, sayısal tutarlılık ve şirket veri seti uyumunu denetler.
---

# ajan3-alma — Ajan 3 Girdi Alma ve Doğrulama Skill'i

## Amaç
Ajan 2'den gelen risk analiz sonuç paketini (`data/ajan2_mesaj.json`) ve şirket sevkiyat veri setini (`data/lojistik_sevkiyat_g3_ornek.csv`) alır; `docs/veri-sozlugu.md` (v3.0) ve Duyuru 10 şartlarına göre doğrular. Eksik, bayat veya tutarsız girdi durumunda işi gerekçesiyle Ajan 2'ye geri gönderir.

## Girdiler
- Ajan 2 mesaj paketi: `--ajan2-json` (varsayılan `data/ajan2_mesaj.json`)
- Şirket sevkiyat verisi: `--sevkiyat-csv` (varsayılan `data/lojistik_sevkiyat_g3_ornek.csv`)

## Kontrol Kuralları
1. **Zarf ve Kimlik Denetimi:** `mesaj_id`, `uretim_zamani`, `kaynak_ajan` (`Ajan_2_RiskAnaliz`), `hedef_ajan` (`Ajan_3_Denetim`) alanları doğrulanır.
2. **Tazelik Denetimi:** Ajan 2 paketinin üretim zamanı 7 günden eski olamaz.
3. **Sayısal Tutarlılık:** `toplam_sevkiyat == aktif_sevkiyat + iptal_sevkiyat` eşitliği sağlanmalı, ortalama risk puanı 0–100 arasında olmalıdır.
4. **Kaynak İzlenebilirliği:** Paketteki tüm dayanak kaynaklarda geçerli `http://` veya `https://` `kaynak_url` bulunmalıdır.
5. **Veri Kümesi Eşleşmesi:** Riskli olarak bildirilen sevkiyat kimlikleri (`sevkiyat_id`) şirketin aktif sevkiyat veri setinde mevcut olmalıdır.

## Nasıl Çalıştırılır
```bash
python src/ajan3_denetim.py --ajan2-json data/ajan2_mesaj.json --sevkiyat-csv data/lojistik_sevkiyat_g3_ornek.csv
```

## Geri Gönderim (Reddetme) Protokolü (Duyuru 11 & docs/mesaj-bicimi.md §4)
Girdide kural ihlali tespit edildiğinde standart red zarfı (`durum: red`, `hata_kodu`, `sorunlu_alanlar`) üretilir ve iş gerekçesiyle Ajan 2'ye iade edilir:
1. `toplam_sevkiyat != aktif_sevkiyat + iptal_sevkiyat` sayısal uyumsuzluğu (`ERR_NUMERICAL_INCONSISTENCY`).
2. 0–100 aralığı dışında kalan risk puanları veya bayat tarihli paket (`ERR_STALE_DATA`).
3. Eksik `kaynak_url` veya şirket veri setinde bulunmayan `sevkiyat_id` (`ERR_SCHEMA_MISSING`).

Örnek red zarfı kanıtı: `data/ajan3_red_ornek.json`.
```bash
python src/ajan3_denetim.py --red-ornek
```
