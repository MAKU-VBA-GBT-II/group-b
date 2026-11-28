---
name: be-simulasyon
description: Görev 3 çok ajanlı lojistik programı için dinamik şehir, tarih, ağırlık ve fiyat çarpanı parametreleriyle tekrarlanabilir sentetik sevkiyat verisi üretir.
---

# be-simulasyon — Dinamik Parametreli Lojistik Sevkiyat Simülasyonu (v3.0)

## Amaç
Bu skill, `docs/veri-sozlugu.md` (v3.0) şemasına birebir uygun olarak, dış web kaynaklarından (MGM, KGM, Akaryakıt) gelen parametrelerle uyumlu, komut satırından ayarlanabilir ve sabit tohumla (seed) %100 tekrarlanabilir sentetik lojistik sevkiyat verisi üretir ve şema doğrulamasını gerçekleştirir.

## Girdiler
- **Şema Tanımı:** `docs/veri-sozlugu.md` (v3.0)
- **Tohum (Seed):** Varsayılan `42` (`--tohum` / `--seed`)
- **Gün Sayısı:** Varsayılan `7` gün (`--gun-sayisi` / `--days`)
- **Günlük Sevkiyat:** Varsayılan `20` adet (`--gunluk-sevkiyat` / `--daily-shipments`)
- **Başlangıç Tarihi:** Varsayılan `2026-11-20` (`--baslangic-tarihi`, ISO `YYYY-MM-DD`)
- **Şehir Listesi:** Varsayılan 8 merkez (`--sehirler`, virgülle ayrılmış liste)
- **Fiyat Çarpanı:** Varsayılan `1.0` (`--fiyat-carpani`, akaryakıt kaynaklı navlun çarpanı)
- **Ağırlık Aralığı:** Varsayılan `50`–`10000` kg (`--min-agirlik`, `--max-agirlik`)
- **Gecikme Olasılığı:** Varsayılan `0.15` (`--gecikme-olasiligi` / `--delay-prob`)
- **İptal Olasılığı:** Varsayılan `0.05` (`--iptal-olasiligi` / `--cancel-prob`)

## Çıktı Formatı Kuralları
1. **Hedef Dosya:** Varsayılan olarak `data/lojistik_sevkiyat_g3_ornek.csv` dosya yoluna UTF-8 ve virgül (`,`) ayracıyla kaydedilir (`--cikti-dosyasi` ile özelleştirilebilir).
2. **Sütun Yapısı (10 Alan):**
   `sevkiyat_id,tarih,cikis_sehri,varis_sehri,tasima_modu,agirlik_kg,mesafe_km,ucret_tl,teslim_suresi_saat,durum`
3. **Kimlik Standardı:** `sevkiyat_id` alanı `SVK-G3-0001` formatında sıralı ve benzersiz olmalıdır (`--id-oneki` ile önek özelleştirilebilir).
4. **Şehir Kısıtları:** Varsayılan 8 lojistik merkez (`Istanbul`, `Ankara`, `Izmir`, `Bursa`, `Antalya`, `Adana`, `Trabzon`, `Gaziantep`) kullanılır; çıkış şehri ile varış şehri kesinlikle aynı olamaz (`cikis_sehri != varis_sehri`).
5. **Taşıma Modları:** 4 mod kullanılır (`kara`, `deniz`, `hava`, `demiryolu`). Hava taşımacılığında mesafe `0.82` hava hattı katsayısıyla hesaplanır.
6. **Sayısal ve Format Kuralları:**
   - `agirlik_kg`: `--min-agirlik` ile `--max-agirlik` arası tam sayı.
   - `mesafe_km`: Pozitif tam sayı.
   - `ucret_tl`: Nokta ondalıklı tam 2 ondalıklı sayı (`((agirlik_kg * 0.50) + (mesafe_km * mod_carpani * 1.60)) * fiyat_carpani`).
   - `teslim_suresi_saat`: Nokta ondalıklı tam 1 ondalıklı sayı; **`durum == 'iptal'` ise kesinlikle boş bırakılmalıdır**.
   - `durum`: `zamaninda`, `gecikmeli`, `iptal`.
7. **Ön Doğrulama:** Betik, veriyi diske yazmadan önce `dogrula()` fonksiyonuyla sözlük kurallarını sınar; kural ihlali durumunda `ValueError` fırlatır.

## Örnek Girdi ve Çıktı

### Örnek Girdi:
```bash
python src/simulasyon.py --tohum 42 --gun-sayisi 7 --gunluk-sevkiyat 20 --baslangic-tarihi 2026-11-20
```

### Örnek Çıktı Başlığı ve İlk Satırlar:
```csv
sevkiyat_id,tarih,cikis_sehri,varis_sehri,tasima_modu,agirlik_kg,mesafe_km,ucret_tl,teslim_suresi_saat,durum
SVK-G3-0001,2026-11-20,Antalya,Istanbul,kara,4538,700,3389.00,24.0,gecikmeli
SVK-G3-0002,2026-11-20,Antalya,Bursa,kara,6518,545,4131.00,11.4,zamaninda
```

## Reddetme Durumları
1. **Gerçek Kişisel Veri / Şirket Verisi Talebi:** Şahıs ad-soyadı, TC Kimlik, telefon, gerçek adres veya gizli müşteri verisi eklenmesi talepleri reddedilir. Yalnızca sentetik veriler üretilir.
2. **Sabit Tohumsuz / Rastgelelik Kontrolü Olmayan Üretim:** Tohumsuz veya tekrarlanamaz üretim talepleri reddedilir.
3. **Şema Dışı Alan veya Kural İhlali:** `docs/veri-sozlugu.md` v3.0 standardına uymayan sütun yapısı, virgül ondalık ayracı veya iptal sevkiyata süre atama talepleri reddedilir.
4. **Geçersiz Parametre Değerleri:** Negatif/sıfır gün, sevkiyat veya fiyat çarpanı, geçersiz ağırlık aralığı, 2'den az şehir veya toplamı `1.0`'a ulaşan olasılık değerlerinde `ValueError` üretilir.

## Nasıl Çalıştırılır
```bash
# Varsayılan G3 ayarlarıyla (tohum=42, 7 gün, 20 günlük sevkiyat -> 140 satır, 8 şehir):
python src/simulasyon.py

# Web uyarısı alan iller ve yakıt katsayısı ile özel üretim:
python src/simulasyon.py --sehirler "Istanbul,Ankara,Izmir,Trabzon" --fiyat-carpani 1.08 --min-agirlik 500 --max-agirlik 5000
```
