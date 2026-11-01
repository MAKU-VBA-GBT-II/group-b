# Ürün Gereksinim Dokümanı — Lojistik Zeka Ağı (LIN Görev 2)

**Ürün Adı:** LIN Parametreli Lojistik Simülasyon ve Analitik Hattı  
**Depo:** `MAKU-VBA-GBT-II/group-b`  
**Sürüm:** v2.0  
**Hazırlayan:** DQ — Ece Naz Aktürk (@ece-naz)  
**Tarih:** 2026-11-02  
**İlgili Issue:** [#49](https://github.com/MAKU-VBA-GBT-II/group-b/issues/49)

---

## 1. Ürünün Amacı
Bu mini ürünün amacı; çok modlu (kara, deniz, hava, demiryolu) yurt içi lojistik sevkiyat operasyonlarını gerçekçi parametrelerle simüle eden, veri kalitesi kurallarını üretim aşamasında denetleyen ve operasyonel performansı (ciro, teslimat süreleri, gecikme ve iptal oranları) ölçülebilir 5 temel metrik üzerinden raporlayıp görselleştiren uçtan uca tekrarlanabilir bir sentetik veri hattı sunmaktır.

---

## 2. Ürünün Yaptıkları (Kapsam İçi)
Ürün aşağıdaki işlevleri eksiksiz olarak yerine getirir:

1. **Parametrik Simülasyon Yönetimi:** Komut satırından (`argparse`) ayarlanabilir tohum (`--tohum`), simülasyon gün sayısı (`--gun-sayisi`), günlük sevkiyat hacmi (`--gunluk-sevkiyat`), gecikme olasılığı (`--gecikme-olasiligi`) ve iptal olasılığı (`--iptal-olasiligi`) parametreleriyle dinamik veri üretimi sağlar.
2. **Deterministik Tekrarlanabilirlik:** Varsayılan tohum (`seed=42`) ve parametreler ile çalıştırıldığında her seferinde birebir aynı 900 satırlık veri kümesini üretir.
3. **Çok Modlu Sevkiyat Modellemesi:** 8 ana lojistik merkez (İstanbul, Ankara, İzmir, Bursa, Antalya, Adana, Trabzon, Gaziantep) arasında 4 farklı taşıma modunu (kara, deniz, hava, demiryolu) mesafe ve ağırlık katsayılarıyla simüle eder.
4. **Entegre Şema Doğrulaması:** Dosya diske yazılmadan önce `dogrula()` fonksiyonu ile ID formatı (`SVK-G2-XXXX`), değer aralıkları, pozitiflik ve mantıksal kuralları denetler.
5. **İptal Mantığı Tutarlılığı:** İptal edilen sevkiyatlarda teslim süresi alanını boş (NaN) bırakarak analitik hesaplamaların bozulmasını engeller.
6. **Otomatik Metrik Hesabı:** `src/analiz_g2.py` betiği ile toplam hacim/ciro, net ortalama süre, ISO haftalık zaman serisi, mod gecikme oranları ve en yoğun top-5 rotayı otomatik olarak hesaplar.
7. **Standart Veri Çıktısı:** Veriyi UTF-8 kodlamasında, virgül ayracıyla `data/lojistik_sevkiyat_g2.csv` olarak üretir ve görselleştirme için hazır hale getirir.

---

## 3. Ürünün Yapmadıkları (Kapsam Dışı)
Ürün aşağıdaki konuları bilinçli olarak kapsam dışında tutar:

1. **Gerçek Kişi / Firma Verisi Kullanımı:** Sistem hiçbir aşamasında gerçek kişi adları, TC kimlik numaraları, gerçek adresler veya ticari müşteri sırları içermez; tüm veriler sentetik ve anonimdir.
2. **Canlı GPS ve Canlı Harita Takibi:** Sevkiyat rotaları anlık GPS koordinatları veya gerçek zamanlı telemetri cihazları üzerinden değil, statik şehir mesafe matrisi üzerinden hesaplanır.
3. **Canlı Hava Durumu ve Trafik API Entegrasyonu:** Hava muhalefeti veya yol durumu gecikmeleri harici web servislerinden çekilmez; olasılıksal simülasyon değişkenleri üzerinden modellenir.
4. **Veritabanı (RDBMS / NoSQL) Kalıcılığı:** Veriler ilişkisel veritabanı (PostgreSQL vb.) yerine doğrudan dosya sistemi tabanlı CSV ve Markdown formatında saklanır.
5. **Web Tabanlı Kullanıcı Arayüzü:** Ürün bir web frontend'i sunmaz; etkileşim CLI betikleri, statik PNG grafikleri ve Markdown raporları ile sınırlıdır.
