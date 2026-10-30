# Veri Sözlüğü — Lojistik Sevkiyat Simülasyonu (Görev 2)

**Sürüm:** v2.0  
**Rol ve Sorumlu:** DQ — Ece Naz Aktürk (@ece-naz)  
**Hedef Kitle:** BE (Aykut Çakıcı), FE (Sema Coşkun), Junior (İpek), PM (Sude Çukurtaş)  
**Tarih:** 2026-10-31  
**İlgili Issue:** [#46](https://github.com/MAKU-VBA-GBT-II/group-b/issues/46)

---

## 1. Genel Bakış ve Amaç
Bu veri sözlüğü, Görev 2 mini ürünü olan **Parametreli Lojistik Sevkiyat Simülasyonu** veri hattının, analiz planının ve görselleştirme gereksinimlerinin temel standardını belirler.

Tüm veri sentetik olup sabit tohumla tekrarlanabilir niteliktedir. **Gerçek kişi, müşteri veya firma verisi kesinlikle depoya dahil edilmez.**

---

## 2. Veri Kümesi Özellikleri
- **Hedef Dosya:** `data/lojistik_sevkiyat_g2.csv`
- **Hedef Satır Sayısı:** 900 satır (60 gün × ortalama 15 sevkiyat/gün)
- **Karakter Kodlaması:** UTF-8
- **Ayraç:** Virgül (`,`)
- **Tohum (Seed):** 42 (varsayılan)

---

## 3. Simülasyon Parametreleri (BE İçin)
Backend simülasyon betiği (`src/simulasyon.py`), komut satırı argümanları (`argparse`) veya yapılandırma değişkenleri ile en az aşağıdaki ayarlanabilir parametreleri desteklemelidir:

| Parametre Adı | Tip | Varsayılan | Açıklama |
|---|---|---|---|
| `--tohum` (`seed`) | Tam sayı | `42` | Simülasyonun tekrarlanabilirliğini sağlayan rastgelelik tohumu. |
| `--gun-sayisi` (`days`) | Tam sayı | `60` | Simüle edilecek toplam gün sayısı (Başlangıç: `2026-01-01`). |
| `--gunluk-sevkiyat` (`daily_shipments`) | Tam sayı | `15` | Gün başına ortalama üretilecek sevkiyat sayısı. |
| `--gecikme-olasiligi` (`delay_prob`) | Ondalık | `0.15` | Bir sevkiyatın operasyonel gecikmeye uğrama olasılığı (%15). |
| `--iptal-olasiligi` (`cancel_prob`) | Ondalık | `0.05` | Bir sevkiyatın iptal edilme olasılığı (%5). |

---

## 4. Alan Tanımları ve Kuralları

| Alan Adı | Veri Tipi | Zorunlu / Boşluk | Geçerli Aralık / Kural | Örnek Değer |
|---|---|---|---|---|
| `sevkiyat_id` | Metin (String) | Zorunlu | Benzersiz format: `SVK-G2-0001` ... `SVK-G2-XXXX` | `SVK-G2-0142` |
| `tarih` | Tarih (String) | Zorunlu | `YYYY-MM-DD` ISO formatı; `2026-01-01` ile başlayan `gun_sayisi` aralığı | `2026-01-18` |
| `cikis_sehri` | Metin (String) | Zorunlu | 8 Lojistik Merkez: `Istanbul`, `Ankara`, `Izmir`, `Bursa`, `Antalya`, `Adana`, `Trabzon`, `Gaziantep` | `Istanbul` |
| `varis_sehri` | Metin (String) | Zorunlu | Çıkış şehirleri listesiyle aynı, ancak `varis_sehri != cikis_sehri` | `Izmir` |
| `tasima_modu` | Metin (String) | Zorunlu | 4 Mod: `kara`, `deniz`, `hava`, `demiryolu` | `kara` |
| `agirlik_kg` | Tam sayı (Integer) | Zorunlu | `50` ile `10000` arası pozitif tam sayı | `1850` |
| `mesafe_km` | Tam sayı (Integer) | Zorunlu | Şehirler arası karayolu mesafesi baz alınır (`100` - `1800` km). Hava modu için düz hat katsayısı (%80-%85) uygulanabilir. | `480` |
| `ucret_tl` | Ondalık (Float) | Zorunlu | Pozitif ondalık sayı, tam 2 basamak. Formül: `(agirlik_kg * 0.50) + (mesafe_km * mod_çarpanı * 1.6)`. İptal edilenlerde de tahakkuk eden navlun yansıtılır. | `3450.50` |
| `teslim_suresi_saat` | Ondalık (Float) | Koşullu | 1 ondalık basamak. Ortalama hız ve bekleme süresine dayalıdır. **Kural:** `durum == 'iptal'` ise bu alan kesinlikle **BOŞ** (None / NaN / boş string) olmalıdır! | `18.5` |
| `durum` | Metin (String) | Zorunlu | 3 Durum: `zamaninda`, `gecikmeli`, `iptal` | `zamaninda` |

---

## 5. Analiz Planı ve 5 Temel Metrik (DQ & FE İçin)

Mini ürün analiz raporunda (`docs/analiz-g2.md`) ve görselleştirmelerde (`visuals/`) kullanılacak zorunlu 5 metrik şunlardır:

### Metrik 1: Toplam Sevkiyat Hacmi ve Toplam Ciro (Toplam Metrik)
* **Adı:** Toplam Sevkiyat Adedi ve Toplam Navlun Geliri (`toplam_ciro_tl`)
* **Ölçtüğü:** Simülasyon dönemindeki tüm sevkiyat hacmini ve parasal büyüklüğü.
* **Formül:** `Toplam Adet = COUNT(sevkiyat_id)`, `Toplam Ciro = SUM(ucret_tl)` (İptaller dahil operasyonel hacim).

### Metrik 2: Ortalama Teslimat Süresi ve Ortalama Ağırlık (Ortalama Metrik)
* **Adı:** Net Ortalama Teslimat Süresi (`ortalama_teslim_suresi_saat`)
* **Ölçtüğü:** Başarıyla sonuçlanan (zamanında + gecikmeli) sevkiyatların ortalama teslimat hızını.
* **Formül:** `AVG(teslim_suresi_saat)` WHERE `durum != 'iptal'`.
* **Kritik Kural:** İptal edilen kayıtlar süre ortalamasına kesinlikle dahil edilmez.

### Metrik 3: Haftalık Sevkiyat Hacmi ve Gelir Trendi (Zaman Serisi Kırılımı)
* **Adı:** Hafta Bazında Sevkiyat Sayısı ve Ciro
* **Ölçtüğü:** Dönem içindeki operasyonel yoğunluğun haftalık dağılımını.
* **Formül:** `GROUP BY Hafta(tarih)` -> `COUNT(sevkiyat_id)`, `SUM(ucret_tl)`.
* **FE Kullanımı:** 1. Grafik (Zaman Serisi trend grafiği).

### Metrik 4: Taşıma Moduna Göre Sevkiyat Sayısı ve Gecikme Oranı (Kategorik Kırılım)
* **Adı:** Mod Bazlı Gecikme Performansı
* **Ölçtüğü:** Farklı taşıma modlarının (kara, deniz, hava, demiryolu) güvenilirlik ve gecikme riskini.
* **Formül:** Mod bazında `Gecikme Oranı (%) = (Geciken Sevkiyat Sayısı / (Zamanında + Geciken Sevkiyat Sayısı)) * 100`. (Paydada iptaller yer almaz).
* **FE Kullanımı:** 2. Grafik (Kategorik kırılım çubuk grafiği).

### Metrik 5: En Yoğun Top-5 Sevkiyat Rotası (Top-N Metrik)
* **Adı:** En Yüksek Hacimli İlk 5 Rota
* **Ölçtüğü:** En çok sevkiyat yapılan şehir çiftlerini (`cikis_sehri` -> `varis_sehri`).
* **Formül:** `GROUP BY cikis_sehri, varis_sehri` -> `ORDER BY COUNT(*) DESC LIMIT 5`.

---

## 6. FE (Görselleştirme) İçin 3 Grafik Seti Gereksinimleri
Issue #48 gereğince FE rolünün üreteceği 3 grafik doğrudan bu sözlükteki verileri kullanır:
1. **Zaman Serisi Grafiği:** Haftalık sevkiyat hacmi ve toplam ciro trendi (`visuals/zaman_serisi_haftalik.png`).
2. **Kategorik Kırılım Grafiği:** Taşıma modlarına göre toplam sevkiyat adedi ve gecikme oranı (`visuals/mod_gecikme_kirilimi.png`).
3. **Dağılım Grafiği:** Başarılı sevkiyatların teslimat süresi dağılımı histogramı (`visuals/teslimat_suresi_dagilimi.png`).

---

## 7. Kabul ve Doğrulama Kriterleri
- [ ] Üretim betiği veriyi yazmadan önce şemayı doğrulamalıdır (`dogrula()` fonksiyonu).
- [ ] `sevkiyat_id` değerleri benzersiz olmalıdır.
- [ ] İptal durumundaki satırlarda `teslim_suresi_saat` boş (NaN) bırakılmalıdır.
- [ ] Sabit tohum (seed=42) ile çalıştırıldığında her seferinde birebir aynı veri kümesi elde edilmelidir.
