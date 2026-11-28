---
name: ajan3-isleme
description: Ajan 3 için risk puanı eşik süzgecini uygular; yüksek riskli sevkiyatları ve yol/hava olaylarıyla rota gerekçesini denetler.
---

# ajan3-isleme — Ajan 3 Risk Eşik ve Tutarlılık Denetim Skill'i

## Amaç
Ajan 2'den gelen 140 sevkiyatlık risk analiz sonuçları içerisinden kritik risk eşiğini (varsayılan: 65 puan) aşan kayıtları filtreler. Sevkiyatın taşıma modu ve rotası ile dayandığı resmi KGM yol bülteni veya MGM meteorolojik uyarılarının mantıksal uyumunu denetler.

## Girdiler
- Ajan 2 veri paketi (doğrulanmış)
- Kritik risk puanı eşiği: `--esik` (varsayılan `65`)

## Denetim Kuralları
1. **Eşik Filtreleme:** Risk puanı $\ge 65$ olan sevkiyatlar müşteri bilgilendirme sürecine dahil edilir.
2. **Gerekçe Kontrolü:** Kritik riskli olarak işaretlenen her sevkiyatta en az 1 somut risk nedeni (`operasyonel_gecikme`, `kgm_kapali_...`, `mgm_...`) bulunmalıdır.
3. **Coğrafi / Rota Tutarlılığı:** Bildirilen kapalı yol veya hava olayı güzergah ile (çıkış veya varış ili koridoru) örtüşmelidir.

## Nasıl Çalıştırılır
```bash
python -c "from ajan3_denetim import denetle_ve_suz; import json; p = json.load(open('data/ajan2_mesaj.json')); print(denetle_ve_suz(p, kritik_esik=65))"
```
