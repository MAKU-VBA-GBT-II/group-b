# Lojistik Sevkiyat Analiz Raporu — Görev 2

**Analiz Edilen Veri Commit'i:** [`869dd1b`](https://github.com/MAKU-VBA-GBT-II/group-b/commit/869dd1b)  
**Veri Dosyası:** [`data/lojistik_sevkiyat_g2.csv`](https://github.com/MAKU-VBA-GBT-II/group-b/blob/main/data/lojistik_sevkiyat_g2.csv)  
**Veri Sözlüğü Sürümü:** [`docs/veri-sozlugu.md`](https://github.com/MAKU-VBA-GBT-II/group-b/blob/main/docs/veri-sozlugu.md) (v2.0)  
**Hazırlayan:** DQ — Ece Naz Aktürk (@ece-naz)  
**Tarih:** 2026-11-02  
**İlgili Issue:** [#49](https://github.com/MAKU-VBA-GBT-II/group-b/issues/49)

---

## 1. Yönetici Özeti ve Genel Metrikler

Görev 2 kapsamında üretilen 60 günlük parametreli lojistik sevkiyat simülasyon veri kümesi, veri kalitesi ve analitik metrikler açısından incelenmiştir. Toplam 900 operasyonel sevkiyat kaydı üzerinden elde edilen temel göstergeler şunlardır:

| Metrik | Değer | Açıklama |
|---|---|---|
| **Toplam Sevkiyat Adedi** | 900 adet | Simülasyon periyodundaki tüm operasyonel kayıtlar (İptaller dahil). |
| **Toplam Ciro (Navlun Geliri)** | 3.351.304,20 TL | Tahakkuk eden tüm navlun gelirleri toplamı. |
| **Tamamlanan Sevkiyat** | 851 adet (%94,6) | Zamanında veya gecikmeli olarak alıcısına ulaşan yükler. |
| **İptal Edilen Sevkiyat** | 49 adet (%5,4) | Operasyonel nedenlerle iptal edilen yükler (Hedeflenen %5 parametresiyle uyumlu). |
| **Ortalama Teslim Süresi** | 20,86 saat | **İptaller hariç** fiili teslimat süresi ortalaması. |
| **Ortalama Sevkiyat Ağırlığı**| 4.969,93 kg | 50 kg ile 10.000 kg bandında dengeli dağılan yük ortalaması. |

---

## 2. 5 Temel Analitik Metrik

### Metrik 1: Toplam Sevkiyat Hacmi ve Toplam Ciro
* **Toplam Sevkiyat:** 900  
* **Toplam Ciro:** 3.351.304,20 TL  
* **Yorum:** 60 günlük simülasyon boyunca günlük ortalama 15 sevkiyat hedefine tam ulaşılmış olup, 3,35 milyon TL'lik dengeli ve sürdürülebilir bir operasyonel iş hacmi yönetilmiştir.

### Metrik 2: Ortalama Teslimat Süresi ve Ortalama Ağırlık
* **Ortalama Teslim Süresi:** 20,86 saat (Yalnızca tamamlanan 851 sevkiyat üzerinden hesaplanmıştır; iptal olan 49 kayıt süreye dahil edilmemiştir).
* **Ortalama Ağırlık:** 4.969,93 kg  
* **Yorum:** Yüklerin ortalama teslimat süresi 21 saatin altında kalarak ülke içi lojistikte hızlı teslimat standardını karşılamaktadır; ortalama ağırlık ise endüstriyel parsiyel ve komple taşımacılık dengesini yansıtmaktadır.

### Metrik 3: Haftalık Sevkiyat Hacmi ve Gelir Trendi (Zaman Serisi Kırılımı)
Analiz standardı olarak Pazartesi başlangıçlı ISO haftası (`YYYY-Www`) esas alınmıştır:

| Hafta | Tarih Aralığı | Gün Sayısı | Sevkiyat Adedi | Haftalık Ciro (TL) | Ortalama Navlun / Sevkiyat |
|---|---|---|---|---|---|
| **2026-W01** | 2026-01-01 – 2026-01-04 | 4 gün | 60 | 220.732,20 TL | 3.678,87 TL |
| **2026-W02** | 2026-01-05 – 2026-01-11 | 7 gün | 105 | 408.413,50 TL | 3.889,65 TL |
| **2026-W03** | 2026-01-12 – 2026-01-18 | 7 gün | 105 | 377.873,30 TL | 3.598,79 TL |
| **2026-W04** | 2026-01-19 – 2026-01-25 | 7 gün | 105 | 405.814,40 TL | 3.864,90 TL |
| **2026-W05** | 2026-01-26 – 2026-02-01 | 7 gün | 105 | 403.997,60 TL | 3.847,60 TL |
| **2026-W06** | 2026-02-02 – 2026-02-08 | 7 gün | 105 | 368.535,70 TL | 3.509,86 TL |
| **2026-W07** | 2026-02-09 – 2026-02-15 | 7 gün | 105 | 377.817,80 TL | 3.598,26 TL |
| **2026-W08** | 2026-02-16 – 2026-02-22 | 7 gün | 105 | 388.795,50 TL | 3.702,81 TL |
| **2026-W09** | 2026-02-23 – 2026-03-01 | 7 gün | 105 | 399.324,20 TL | 3.803,09 TL |

* **Yorum:** Simülasyonun Perşembe gününe denk gelen ilk 4 günü (W01) doğal takvim kısıtı nedeniyle 60 sevkiyatta kalmış; W02'den itibaren tüm haftalarda haftalık 105 sevkiyatlık mükemmel bir istikrar sağlanmıştır. Haftalık cirolar düzenli olarak 370.000 TL – 408.000 TL aralığında gerçekleşmiştir.

### Metrik 4: Taşıma Moduna Göre Sevkiyat Sayısı ve Gecikme Oranı (Kategorik Kırılım)
Gecikme oranı formülü: `Gecikme Oranı (%) = (Gecikmeli / (Zamanında + Gecikmeli)) * 100` (Paydada iptaller yer almaz).

| Taşıma Modu | Toplam Sevkiyat | Zamanında | Gecikmeli | İptal | Gecikme Oranı (%) | Toplam Gelir (TL) | Gelir Payı (%) |
|---|---|---|---|---|---|---|---|
| **Kara** | 451 | 349 | 74 | 28 | **%17,5** | 1.589.147,00 TL | %47,4 |
| **Demiryolu**| 186 | 148 | 31 | 7 | **%17,3** | 652.578,00 TL | %19,5 |
| **Hava** | 135 | 111 | 16 | 8 | **%12,6** | 702.800,50 TL | %21,0 |
| **Deniz** | 128 | 109 | 13 | 6 | **%10,7** | 406.778,70 TL | %12,1 |

* **Yorum:** Kara yolu %47,4'lük gelir ve 451 sevkiyatla operasyonun omurgasını oluştururken, %17,5 ile en yüksek gecikme oranına sahiptir. Deniz yolu ise %10,7 ile en güvenilir ve zamanında teslimat oranı en yüksek mod olarak öne çıkmaktadır.

### Metrik 5: En Yoğun Top-5 Sevkiyat Rotası (Top-N Metrik)

| Sıra | Rota (`Çıkış -> Varış`) | Sevkiyat Adedi | Toplam Hacim Payı (%) | Toplam Ciro (TL) |
|---|---|---|---|---|
| **1** | Trabzon -> Bursa | 25 | %2,8 | 113.292,00 TL |
| **2** | Adana -> Gaziantep | 24 | %2,7 | 74.231,90 TL |
| **3** | Izmir -> Trabzon | 23 | %2,6 | 105.240,70 TL |
| **4** | Ankara -> Antalya | 22 | %2,4 | 82.153,90 TL |
| **5** | Ankara -> Bursa | 22 | %2,4 | 73.866,80 TL |

* **Yorum:** 8 lojistik merkez arasındaki 56 olası rotanın içinde en yoğun 5 rota, toplam iş hacminin yaklaşık %13'ünü oluşturmaktadır. Karadeniz-Marmara koridoru (Trabzon -> Bursa) hem adet hem de ciro bakımından lider rotadır.

---

## 3. Bulgular (3 Somut Gözlem + 1 Eylem Önerisi)

### Somut Gözlem 1: Taşıma Modlarında Değer/Hacim Asimetrisi
Kara yolu taşımacılığı 451 sevkiyat ile hacmin %50,1'ini ve 1,59 milyon TL ile cironun %47,4'ünü oluşturarak hacim lideridir. Buna karşılık, **hava yolu taşımacılığı** sadece 135 sevkiyatla (%15,0 hacim) 702.800,50 TL ciro (%21,0 pay) üretmiş ve sevkiyat başına **5.205,93 TL** ortalama gelir ile kara yoluna (3.523,61 TL) kıyasla %47 daha yüksek birim katma değer sağlamıştır.

### Somut Gözlem 2: Mod Bazında Güvenilirlik ve İptal Riski
Kara yolu (%17,5) ve demiryolu (%17,3) gecikme oranları simülasyon temel hedefi olan %15'in üzerinde kalmıştır. Ayrıca toplam 49 iptalin 28'i (%57,1'i) kara yolu modunda gerçekleşmiştir. Buna karşılık **deniz yolu (%10,7)** ve **hava yolu (%12,6)**, hava ve liman operasyonlarındaki planlama disiplini sayesinde belirgin şekilde daha yüksek teslimat güvenilirliği sunmaktadır.

### Somut Gözlem 3: Zaman Serisinde Kararlı Akış
W01 periyodundaki 4 günlük başlangıç (60 sevkiyat) sonrasında, W02'den W09'a kadar olan 8 tam haftanın her birinde tam 105 sevkiyat gerçekleştirilmiş ve haftalık ciro 368 bin TL ile 408 bin TL arasında çok dar bir varyansla seyretmiştir. Bu durum operasyonel kapasitenin ve talebin tam doygunlukta çalıştığını göstermektedir.

### Eylem Önerisi (Optimizasyon & Rota Güçlendirme)
* **Kombine Taşımacılık ve Mod Kaydırma:** Kara yolundaki yüksek gecikme (%17,5) ve iptal yoğunluğunu (28 adet) azaltmak amacıyla; özellikle Marmara–Karadeniz (Trabzon–Bursa) ve İç Anadolu bağlantılarında yüklerin bir kısmı kara yolundan demiryoluna ve deniz yoluna kaydırılmalıdır.
* **Yüksek Katma Değerli Ekspres Hat:** Zaman hassasiyeti kritik olan sanayi ve e-ticaret yükleri için en düşük gecikme oranına sahip deniz (%10,7) ve hava (%12,6) modları teşvik edilerek ciro marjı artırılmalıdır.

---

## 4. Frontend (Görselleştirme) Devir Teslim Notları
Frontend rolü (@sema788 - [Issue #48](https://github.com/MAKU-VBA-GBT-II/group-b/issues/48)), grafik üretim kodunda (`src/gorsel_g2.py`) aşağıdaki doğrulanmış metrikleri kullanacaktır:
1. **`visuals/zaman_serisi_haftalik.png`:** Yukarıdaki Metrik 3 tablosundaki 9 ISO haftası değerleri (W01: 60 ... W09: 105) ve ciro çizgisi kullanılacaktır.
2. **`visuals/mod_gecikme_kirilimi.png`:** Metrik 4 tablosundaki 4 mod (Kara: 451/%17,5, Demiryolu: 186/%17,3, Hava: 135/%12,6, Deniz: 128/%10,7) kullanılacaktır.
3. **`visuals/teslimat_suresi_dagilimi.png`:** İptal edilen 49 kayıt dışlanarak 851 başarılı kaydın teslim süresi histogramı çizilecektir.
