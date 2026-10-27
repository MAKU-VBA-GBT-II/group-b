# G1 Sevkiyat Veri Kalitesi Test Sonuç Günlüğü (test-log.md)

**Şirket:** Grup B — Logistics Intelligence Network (LIN)  
**Test Edilen Dosya:** `data/lojistik-sevkiyat.csv`  
**Referans:** `tests/test-cases.md`, `docs/veri-sozlugu-g1.md` v1.1  
**Test edilen upstream kaynak:** `main` @ `8962c03ba82cb214b28405cfd27295d1cea8246b` (CSV dosyası bu commit'te)  
**Test yöntemi:** `tests/test-cases.md` senaryoları CSV üzerinde tek tek doğrulandı. Depoda `src/dq_test.py` bulunmadığından testler mevcut betikle koşturulamadı.  
**Test Eden:** Aykut Çakıcı (DQ)

---

## Test Koşum Kayıtları

| No | Senaryo | Test Tarihi | Test Eden | Gerçekleşen Sonuç | Durum (Geçti / Kaldı) | İlgili Issue / Not |
|---:|---|---|---|---|---|---|
| 1 | Sevkiyat dosyası mevcut ve okunabilir | 2026-10-22 | Aykut Çakıcı (DQ) | UTF-8 CSV okundu; 10 sütun ve 300 veri satırı | Geçti | — |
| 2 | Asgari satır sayısı sağlanıyor | 2026-10-22 | Aykut Çakıcı (DQ) | 300 veri satırı (hedef 300; alt sınır 100) | Geçti | — |
| 3 | Sütun sayısı ve adları şemayla eşleşiyor | 2026-10-22 | Aykut Çakıcı (DQ) | 10 sütun; adlar ve sıra veri sözlüğü v1.1 ile birebir aynı | Geçti | — |
| 4 | Sevkiyat kimlikleri benzersiz ve biçime uygun | 2026-10-22 | Aykut Çakıcı (DQ) | 300 benzersiz ID; SVK-0001–SVK-0300 aralığında | Geçti | — |
| 5 | Tarih, tür ve sayısal aralıklar geçerli | 2026-10-22 | Aykut Çakıcı (DQ) | Tarihler 2026-01-01–2026-03-31; ağırlık 10–5000, mesafe 50–2500, ücret > 0; ihlal 0 | Geçti | — |
| 6 | Kategoriler ve şehir değerleri geçerli | 2026-10-22 | Aykut Çakıcı (DQ) | Şehir/durum/mod değerlerinde şema dışı kayıt 0; dört mod da mevcut | Geçti | — |
| 7 | İptal sevkiyatlarda teslim süresi boş | 2026-10-22 | Aykut Çakıcı (DQ) | 12 iptal satırının teslim süresi boş; iptal olmayan 288 satırda süre sayısal | Geçti | İptaller ortalamadan hariç |
| 8 | Bonus: çıkış ve varış şehirleri farklı | 2026-10-22 | Aykut Çakıcı (DQ) | Aynı şehirli rota 0 | Geçti | — |

**Özet (1. Koşum):** 8 senaryo, 8 geçti, 0 kaldı. Hata bulunmadı.

### 2. Koşum (2026-10-27 — `src/test_calistir.py` ile Otomatik Koşum)

| No | Senaryo | Test Tarihi | Test Eden | Gerçekleşen Sonuç | Durum (Geçti / Kaldı) | İlgili Issue / Not |
|---:|---|---|---|---|---|---|
| 1 | Sevkiyat dosyası mevcut ve okunabilir | 2026-10-27 | DQ Test Runner (`test_calistir.py`) | UTF-8 olarak başarıyla okundu; başlık ve 300 veri satırı mevcut | Geçti | Otomatik koşum |
| 2 | Asgari satır sayısı sağlanıyor | 2026-10-27 | DQ Test Runner (`test_calistir.py`) | 300 veri satırı mevcut (alt sınır 100, hedef 300 sağlandı) | Geçti | Otomatik koşum |
| 3 | Sütun sayısı ve adları şemayla eşleşiyor | 2026-10-27 | DQ Test Runner (`test_calistir.py`) | Tam 10 sütun; adlar ve sıra veri sözlüğü v1.1 ile birebir eşleşiyor | Geçti | Otomatik koşum |
| 4 | Sevkiyat kimlikleri benzersiz ve biçime uygun | 2026-10-27 | DQ Test Runner (`test_calistir.py`) | 300 kimliğin tamamı benzersiz ve 'SVK-XXXX' biçiminde | Geçti | Otomatik koşum |
| 5 | Tarih, tür ve sayısal aralıklar geçerli | 2026-10-27 | DQ Test Runner (`test_calistir.py`) | Tarihler 2026-01-01..2026-03-31; ağırlık 10..5000; mesafe 50..2500; ücret > 0 | Geçti | Otomatik koşum |
| 6 | Kategoriler ve şehir değerleri geçerli | 2026-10-27 | DQ Test Runner (`test_calistir.py`) | Tüm şehir, durum ve modlar izinli listede; 4 taşıma modu da temsil ediliyor | Geçti | Otomatik koşum |
| 7 | İptal sevkiyatlarda teslim süresi boş | 2026-10-27 | DQ Test Runner (`test_calistir.py`) | 12 adet iptal satırının teslim süresi boş; aktif satırlar sayısal | Geçti | Otomatik koşum |
| 8 | Bonus: çıkış ve varış şehirleri farklı | 2026-10-27 | DQ Test Runner (`test_calistir.py`) | Hiçbir satırda çıkış ve varış şehri aynı değil (0 hata) | Geçti | Otomatik koşum |

**Özet (2. Koşum):** 8 senaryo, 8 geçti, 0 kaldı. `src/test_calistir.py` betiği ile tüm senaryolar başarıyla doğrulandı.

---

## Test Edilen Nihai Veri

- 300 satır, 10 beklenen alan; dosya UTF-8 ve virgülle ayrılmış.
- 300 benzersiz ve biçime uygun sevkiyat kimliği.
- Tarih, ağırlık, mesafe ve ücret kurallarında ihlal yok.
- İzinli şehir, durum ve taşıma modları dışında değer yok; dört modun tamamı mevcut.
- 12 iptal kaydında teslim süresi boş; iptal olmayan 288 kayıtta sayısal.
- Çıkış ve varış şehirleri aynı olan kayıt yok.

---

## İyileştirme Önerileri

1. `tests/test-cases.md` senaryolarını tekrarlanabilir biçimde çalıştıran `src/test_calistir.py` eklenmesi. *(Tamamlandı — 2026-10-27)*
2. `src/uret_sevkiyat.py` içinde CSV yazılmadan önce tüm veri sözlüğü kurallarının doğrulanması. *(Tamamlandı — v1.2 dogrula() fonksiyonu eklendi)*

## Tespit Edilen Hatalar ve Açılan Kayıtlar

- Veri hatası tespit edilmedi; test sonucu 8/8 geçti.
- İki somut iyileştirme önerisi Duyuru 5 kapsamında başarıyla hayata geçirildi.