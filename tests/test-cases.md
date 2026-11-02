# Görev 2 Lojistik Sevkiyat Veri Kalitesi Test Senaryoları (G2-TEST)

**Sürüm:** v2.0  
**Hazırlayan:** DQ — Ece Naz Aktürk (@ece-naz)  
**Referans Veri Sözlüğü:** [`docs/veri-sozlugu.md`](../docs/veri-sozlugu.md) (v2.0)  
**Test Edilen Dosya:** `data/lojistik_sevkiyat_g2.csv`  
**İlgili Issue:** [#50](https://github.com/MAKU-VBA-GBT-II/group-b/issues/50)

> Bu test senaryoları; Backend (BE) tarafından üretilen parametreli lojistik simülasyon verisinin şema standartlarına, veri tiplerine, değer aralıklarına, iş kurallarına ve tekrarlanabilirlik ilkelerine tam uyumunu denetler.

---

## Test Senaryoları Tablosu

| No | Senaryo | Test Adımları | Beklenen Sonuç | Gerçekleşen Sonuç |
|---:|---|---|---|---|
| **1** | **Veri Dosyası Varlığı ve Kodlama** | 1. `data/lojistik_sevkiyat_g2.csv` dosyasının depoda mevcut olduğunu doğrula.<br>2. Dosyayı UTF-8 kodlamasında açıp başlık ve satırları oku. | Dosya mevcuttur; UTF-8 kodlamasında virgül ayracıyla açılır, başlık ve veri satırları hatasız okunur. | |
| **2** | **Hedef Satır Sayısı Doğrulaması** | 1. CSV'deki satırları say (başlık hariç).<br>2. 60 gün × 15 sevkiyat/gün hacmini kontrol et. | Başlık hariç tam 900 veri satırı (başlıkla birlikte 901 satır) bulunur. | |
| **3** | **Sütun Sayısı, İsimleri ve Sırası** | 1. CSV başlık satırını oku.<br>2. Sütun isimlerini ve sırasını `docs/veri-sozlugu.md` ile karşılaştır. | Tam 10 sütun bulunur ve sırası birebir eşleşir: `sevkiyat_id`, `tarih`, `cikis_sehri`, `varis_sehri`, `tasima_modu`, `agirlik_kg`, `mesafe_km`, `ucret_tl`, `teslim_suresi_saat`, `durum`. | |
| **4** | **Kimlik Formatı ve Benzersizlik** | 1. Tüm `sevkiyat_id` değerlerini topla.<br>2. `SVK-G2-\d{4,}` regex formatını denetle.<br>3. Tekrarlanan ID olup olmadığını kontrol et. | Tüm 900 kimlik benzersizdir ve `SVK-G2-0001` formatına tam uyar. | |
| **5** | **Tarih Formatı ve Simülasyon Periyodu** | 1. `tarih` alanının ISO `YYYY-MM-DD` formatında olduğunu doğrula.<br>2. Minimum ve maksimum tarih aralığını kontrol et. | Tüm tarihler ISO formatındadır; `2026-01-01` ile `2026-03-01` arasındaki 60 günlük periyodu kapsar. | |
| **6** | **8 Lojistik Merkez ve Farklı Şehir Kuralı** | 1. `cikis_sehri` ve `varis_sehri` alanlarındaki değerleri 8 izinli merkezle (`Istanbul`, `Ankara`, `Izmir`, `Bursa`, `Antalya`, `Adana`, `Trabzon`, `Gaziantep`) karşılaştır.<br>2. Her satırda `cikis_sehri != varis_sehri` olduğunu denetle. | Tüm şehirler 8 merkez listesindedir; hiçbir satırda çıkış ve varış şehri aynı değildir. | |
| **7** | **4 Taşıma Modu Temsili** | 1. `tasima_modu` alanının benzersiz değerlerini çıkar.<br>2. 4 modun (`kara`, `deniz`, `hava`, `demiryolu`) tamamının temsil edildiğini doğrula. | Yalnızca izinli 4 mod bulunur ve dördü de veri kümesinde yer alır. | |
| **8** | **Sayısal Aralıklar ve Tipler** | 1. `agirlik_kg` (50–10000 kg tam sayı) aralığını kontrol et.<br>2. `mesafe_km` (100–1800 km tam sayı) aralığını kontrol et.<br>3. `ucret_tl` (> 0 ve tam 2 ondalık basamak) kontrolünü yap. | Tüm sayısal değerler pozitif, belirtilen aralıklarda ve beklenen veri tiplerindedir. | |
| **9** | **Durum Kategorileri ve İptal Kuralı (Kritik)** | 1. `durum` alanının yalnızca `zamaninda`, `gecikmeli`, `iptal` değerlerini içerdiğini doğrula.<br>2. `durum == 'iptal'` olan satırlarda `teslim_suresi_saat` hücresinin boş (None/NaN) olduğunu doğrula.<br>3. Aktif sevkiyatlarda teslim süresinin pozitif ve 1 ondalıklı olduğunu denetle. | Durum değerleri geçerlidir. İptal edilen tüm satırlarda teslim süresi boştur; aktif sevkiyatlarda süre pozitiftir. | |
| **10** | **Tohum 42 ile Deterministik Tekrarlanabilirlik** | 1. `python src/simulasyon.py --tohum 42` komutunu çalıştır.<br>2. Üretilen geçici çıktıyı depodaki nihai `data/lojistik_sevkiyat_g2.csv` ile hash/satır bazında karşılaştır. | İki üretim arasında %100 birebir eşleşme sağlanır; veri deterministiktir. | |
