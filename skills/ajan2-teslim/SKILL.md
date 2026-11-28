---
name: ajan2-teslim
description: Ajan 2 risk analizi çıktısını ortak JSON mesaj formatına (Ajan_3_Denetim hedefli) ve CSV raporuna dönüştürür; kaynak URL ve zaman damgasını doğrular.
---

# ajan2-teslim — Ajan 2 Teslim ve Mesaj Paketleme Skill'i

## Amaç
`src/ajan2_risk.py` tarafından üretilen risk puanlarını, rota özetini ve yüksek riskli sevkiyat listesini `docs/mesaj-bicimi.md` sözleşmesine uygun olarak Ajan 3'ün (`Ajan_3_Denetim`) beklediği ortak JSON mesaj biçimine (`data/ornek-ajan2.json`) ve tam risk tablosuna (`data/ajan2_risk_analizi.csv`) dönüştürür.

## Çıktı Formatı ve Kurallar
1. **JSON Mesaj Zarfı (`data/ornek-ajan2.json`):**
   - `mesaj_id` (`MSG-G3-YYYYMMDD-A2-001`)
   - `uretim_zamani` (UTC ISO-8601)
   - `kaynak_ajan`: `"Ajan_2_RiskAnaliz"`
   - `hedef_ajan`: `"Ajan_3_Denetim"`
   - `durum`: `"onay"`
   - `referans_mesaj_id`: Ajan 1 mesaj ID'si
   - `kaynaklar`: Kullanılan tüm benzersiz dış `kaynak_url` ve `erisim_tarihi` listesi
   - `ozet` ve `yuksek_riskli_sevkiyatlar`
2. **CSV Raporu (`data/ajan2_risk_analizi.csv`):** Tüm sevkiyatların risk puanı, seviyesi, ek gecikme saati ve yakıt etkili ücreti.
3. **Teslim Öncesi Doğrulama:** `yuksek_riskli_sevkiyatlar` içindeki her kaydın en az bir geçerli `kaynak_url` + `erisim_tarihi` kanıtı taşıması zorunludur; aksi halde teslim paketi yazılmaz ve `GeriGonderimHatasi` fırlatılır.

## Örnek Çıktı Parçası
```json
{
  "mesaj_id": "MSG-G3-20261128-A2-001",
  "kaynak_ajan": "Ajan_2_RiskAnaliz",
  "hedef_ajan": "Ajan_3_Denetim",
  "referans_mesaj_id": "MSG-G3-20261128-A1-001",
  "durum": "onay"
}
```

## Reddetme Durumları
1. `kaynak_url` veya `uretim_zamani` taşımayan sayısal çıktıların Ajan 3'e iletilmesi reddedilir.
2. `hedef_ajan` alanı `Ajan_3_Denetim` olmayan teslim paketleri reddedilir.
