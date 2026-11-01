---
name: be-simulasyon
description: Görev 2 mini ürünü için parametreli ve tekrarlanabilir lojistik sevkiyat simülasyon verisi üretir.
---

# be-simulasyon — Parametreli Lojistik Sevkiyat Simülasyonu

## Amaç
Bu skill, `docs/veri-sozlugu.md` şemasına birebir uygun olarak, komut satırından parametrelendirilebilir, rastgelelik tohumuyla (seed) %100 tekrarlanabilir sentetik lojistik sevkiyat verisi üretir ve veri kalitesi doğrulamasını gerçekleştirir.

## Girdiler
- **Şema Tanımı:** `docs/veri-sozlugu.md`
- **Tohum (Seed):** Varsayılan `42` (ayarlanabilir `--tohum` / `--seed`)
- **Gün Sayısı:** Varsayılan `60` gün (ayarlanabilir `--gun-sayisi` / `--days`)
- **Günlük Ortalama Sevkiyat:** Varsayılan `15` adet (ayarlanabilir `--gunluk-sevkiyat` / `--daily-shipments`)
- **Gecikme Olasılığı:** Varsayılan `0.15` (ayarlanabilir `--gecikme-olasiligi` / `--delay-prob`)
- **İptal Olasılığı:** Varsayılan `0.05` (ayarlanabilir `--iptal-olasiligi` / `--cancel-prob`)

## Çıktı Formatı Kuralları
1. **Hedef Dosya:** `data/lojistik_sevkiyat_g2.csv` dosya yoluna UTF-8 ve virgül ayracıyla kaydedilir.
2. **Sütun Yapısı (10 Alan):**
   `sevkiyat_id,tarih,cikis_sehri,varis_sehri,tasima_modu,agirlik_kg,mesafe_km,ucret_tl,teslim_suresi_saat,durum`
3. **Kimlik Standardı:** `sevkiyat_id` alanı `SVK-G2-0001` formatında sıralı ve benzersiz olmalıdır.
4. **Şehir Kısıtları:** 8 lojistik merkez (`Istanbul`, `Ankara`, `Izmir`, `Bursa`, `Antalya`, `Adana`, `Trabzon`, `Gaziantep`) kullanılır; çıkış şehri ile varış şehri kesinlikle aynı olamaz (`cikis_sehri != varis_sehri`).
5. **Taşıma Modları:** 4 mod kullanılır (`kara`, `deniz`, `hava`, `demiryolu`). Hava taşımacılığında mesafe hava hattı katsayısıyla hesaplanır.
6. **Sayısal ve Format Kuralları:**
   - `agirlik_kg`: 50 ile 10000 kg arası tam sayı.
   - `mesafe_km`: Pozitif tam sayı (100 - 1800 km).
   - `ucret_tl`: Tam 2 ondalıklı sayı (`(agirlik_kg * 0.50) + (mesafe_km * mod_carpani * 1.6)`).
   - `teslim_suresi_saat`: Tam 1 ondalıklı sayı; **durum == 'iptal' ise kesinlikle boş bırakılmalıdır**.
   - `durum`: `zamaninda`, `gecikmeli`, `iptal`.
7. **Ön Doğrulama:** Betik, veriyi diske yazmadan önce `dogrula()` fonksiyonuyla sözlük kurallarını sınar; kural ihlali durumunda `ValueError` fırlatır.

## Örnek Girdi ve Çıktı

### Örnek Girdi:
```bash
python src/simulasyon.py --tohum 42 --gun-sayisi 60 --gunluk-sevkiyat 15
```

### Örnek Çıktı Başlığı ve İlk Satırlar:
```csv
sevkiyat_id,tarih,cikis_sehri,varis_sehri,tasima_modu,agirlik_kg,mesafe_km,ucret_tl,teslim_suresi_saat,durum
SVK-G2-0001,2026-01-01,Istanbul,Ankara,kara,1250,450,1345.00,10.2,zamaninda
SVK-G2-0002,2026-01-01,Izmir,Antalya,kara,3400,460,2436.00,,iptal
SVK-G2-0003,2026-01-01,Ankara,Trabzon,hava,850,620,2905.00,5.4,gecikmeli
```

## Reddetme Durumları
1. **Gerçek Kişisel Veri / Şirket Verisi Talebi:** Şahıs ad-soyadı, TC Kimlik, telefon, gerçek adres veya şirket içi gizli finansal verilerin eklenmesi talepleri KVKK ve şirket politikası gereği **kesin olarak reddedilir**. Yalnızca sentetik veriler üretilir.
2. **Sabit Tohumsuz / Rastgelelik Kontrolü Olmayan Üretim:** Simülasyonun tekrarlanabilirliğini bozan, tohumsuz veya denetlenemeyen veri üretimi talepleri reddedilir.
3. **Şema Dışı Alan veya Kural İhlali:** `docs/veri-sozlugu.md` standardına uymayan sütun yapısı veya iptal sevkiyata süre atama gibi mantıksal aykırılıklar reddedilir.
4. **Geçersiz Parametre Değerleri:** Negatif gün sayısı, sıfır veya negatif sevkiyat sayısı, olasılık toplamlarının 1'i aşması durumlarında betik çalışmayı reddeder ve `ValueError` üretir.

## Nasıl Çalıştırılır
```bash
# Varsayılan ayarlarla (42 tohum, 60 gün, 15 günlük sevkiyat -> 900 satır):
python src/simulasyon.py

# Özel parametrelerle:
python src/simulasyon.py --tohum 100 --gun-sayisi 30 --gunluk-sevkiyat 20 --gecikme-olasiligi 0.10
```
