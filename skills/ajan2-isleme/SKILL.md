---
name: ajan2-isleme
description: Ajan 2 için MGM uyarıları, KGM yol bülteni ve akaryakıt fiyatlarını sevkiyat rotalarıyla eşleştirip Python ile 0-100 rota risk puanı ve gecikme tahmini hesaplar.
---

# ajan2-isleme — Ajan 2 Risk Puanlama ve Maliyet İşleme Skill'i

## Amaç
`ajan2-alma` adımından geçen dış piyasa/kamu verilerini şirketimizin sentetik sevkiyat rotalarıyla Python (`src/ajan2_risk.py`) kullanarak birleştirir; her sevkiyat ve rota için 0–100 risk puanı, ek gecikme süresi ve akaryakıt etkili maliyet çarpanı hesaplar.

## İşleme Kuralları (`docs/veri-sozlugu.md` v3.0 & `docs/oneri.md`)
1. **MGM Meteorolojik Risk:** Çıkış veya varış ilinde uyarı varsa:
   - `sari`: `+25` puan
   - `turuncu`: `+50` puan
   - `kirmizi`: `+75` puan
2. **KGM Yol Durumu Riski (`tasima_modu == "kara"`):** Güzergah/koridor eşleşen karayolu sevkiyatlarında:
   - `kapali`: `+35` puan ve tahmini teslim süresine `+12.0` saat eklenir.
   - `tek_serit`: `+15` puan ve tahmini teslim süresine `+4.0` saat eklenir.
3. **Akaryakıt Etkisi:** Ajan 1'deki il bazlı motorin fiyatları `85.0 TL/LT` baz değeriyle oranlanarak `yakit_etkili_ucret_tl` hesaplanır; `%2` üzeri artışta `+5` maliyet risk puanı eklenir.
4. **Operasyonel Durum:** `durum == "gecikmeli"` kayıtları `+20` baz risk alır. `durum == "iptal"` kayıtlarında risk `0`, teslim süresi **boş (`""`)** bırakılır.
5. **Sınıflandırma:** Toplam risk puanı `100` ile sınırlandırılır (`dusuk`: 0–29, `orta`: 30–59, `yuksek`: 60–79, `kritik`: 80–100).

## Örnek Kullanım
```bash
python src/ajan2_risk.py --ajan1-json data/ajan1_mesaj.json --sevkiyat-csv data/lojistik_sevkiyat_g3_ornek.csv
```

## Reddetme Durumları
1. Sentetik olmayan gerçek müşteri/kişi verisi ekleme talepleri reddedilir.
2. İptal sevkiyatlara teslim süresi veya ek gecikme saati atayan hesaplamalar reddedilir.
3. Sabit/uydurma risk puanı yerine Ajan 1 kaynaklarına dayanmayan sonuçlar reddedilir.
