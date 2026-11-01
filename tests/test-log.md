# Lojistik Sevkiyat Veri Kalitesi Test Sonuç Günlüğü (test-log.md)

**Şirket:** Grup B — Logistics Intelligence Network (LIN)  
**Mevcut Aşama:** Görev 2 (Parametreli Sevkiyat Simülasyonu)  
**Test Eden (G2):** Ece Naz Aktürk (DQ — @ece-naz)  
**Test Edilen Nihai Dosya:** `data/lojistik_sevkiyat_g2.csv`  
**Test Edilen Veri Commit'i:** [`869dd1b`](https://github.com/MAKU-VBA-GBT-II/group-b/commit/869dd1b)  
**Referans Dokümanlar:** [`tests/test-cases.md`](test-cases.md), [`docs/veri-sozlugu.md`](../docs/veri-sozlugu.md) (v2.0)  
**Test Yöntemi:** `src/test_calistir.py` betiği ile 10 senaryonun CSV ve Python simülasyonu üzerinde otomatik koşumu.  

---

## 3. Koşum: Görev 2 Nihai Veri Kalite Test Koşumu (2026-11-02)

| No | Senaryo Adı | Test Tarihi | Test Eden | Gerçekleşen Sonuç | Durum | İlgili Kural / Not |
|---:|---|---|---|---|---|---|
| **1** | Dosya Varlığı ve UTF-8 Okuma | 2026-11-02 | Ece Naz Aktürk (DQ) | `data/lojistik_sevkiyat_g2.csv` UTF-8 olarak okundu; 900 veri satırı mevcut | **GEÇTİ** | Başlık + 900 satır |
| **2** | Hedef Satır Sayısı Doğrulaması | 2026-11-02 | Ece Naz Aktürk (DQ) | Tam 900 veri satırı mevcut (60 gün × 15 sevkiyat/gün hedefi %100 sağlandı) | **GEÇTİ** | Hedef: 900 |
| **3** | Sütun Sayısı, İsimleri ve Sırası | 2026-11-02 | Ece Naz Aktürk (DQ) | 10 sütun adı ve sırası `docs/veri-sozlugu.md` v2.0 ile birebir eşleşiyor | **GEÇTİ** | 10 sütun tam uyum |
| **4** | Kimlik Formatı ve Benzersizlik | 2026-11-02 | Ece Naz Aktürk (DQ) | 900 kimliğin tamamı benzersiz; `SVK-G2-0001`...`SVK-G2-0900` formatında | **GEÇTİ** | 0 tekrarlanan ID |
| **5** | Tarih Formatı ve 60 Günlük Periyot | 2026-11-02 | Ece Naz Aktürk (DQ) | Tüm tarihler ISO `YYYY-MM-DD`; `2026-01-01` ile `2026-03-01` arasında tam 60 gün | **GEÇTİ** | Periyot eksiksiz |
| **6** | 8 Lojistik Merkez ve Farklı Şehir | 2026-11-02 | Ece Naz Aktürk (DQ) | 8 izinli merkez kullanıldı; hiçbir satırda `cikis_sehri == varis_sehri` yok | **GEÇTİ** | 0 hatalı rota |
| **7** | 4 Taşıma Modu Temsili | 2026-11-02 | Ece Naz Aktürk (DQ) | `kara` (451), `demiryolu` (186), `hava` (135), `deniz` (128) modlarının tümü mevcut | **GEÇTİ** | 4 mod aktif |
| **8** | Sayısal Aralıklar ve Tipler | 2026-11-02 | Ece Naz Aktürk (DQ) | Ağırlık 50–10000 kg, mesafe 100–1800 km, ücret pozitif ve tam 2 ondalık basamaklı | **GEÇTİ** | 0 kural ihlali |
| **9** | Durum ve İptal Boşluk Kuralı | 2026-11-02 | Ece Naz Aktürk (DQ) | 49 iptal kaydında teslim süresi tam boş; 851 aktif kayıtta süre pozitif ve 1 ondalıklı | **GEÇTİ** | İptal kuralı tam |
| **10**| Tohum 42 ile Deterministik Tekrarlanabilirlik | 2026-11-02 | Ece Naz Aktürk (DQ) | `src/simulasyon.py --tohum 42` komutu ile üretilen veri mevcut CSV ile %100 eşleşti | **GEÇTİ** | Deterministik üretim |

**Özet (3. Koşum):** 10 senaryo, 10 geçti, 0 kaldı. Veri kalitesi skoru: **%100 (Kusursuz)**.

---

## Tarihsel Koşum Arşivi (Görev 1)

### 2. Koşum: Görev 1 Otomatik Koşum (2026-10-27)
- **Koşucu:** `src/test_calistir.py` (G1)
- **Sonuç:** 8 senaryo, 8 geçti, 0 kaldı (Hedef 300 satırlık `data/lojistik-sevkiyat.csv`).

### 1. Koşum: Görev 1 Manuel Doğrulama (2026-10-22)
- **Test Eden:** Aykut Çakıcı (DQ)
- **Sonuç:** 8 senaryo, 8 geçti, 0 kaldı.

---

## Görev 2 Test Sonuç Değerlendirmesi
1. **Şema ve Veri Tutarlılığı:** Backend simülasyon betiği `src/simulasyon.py`, veri sözlüğü v2.0 kurallarını eksiksiz uygulamıştır.
2. **Kritik İptal Alanı:** 49 iptal kaydının tamamında teslim süresinin boş bırakıldığı doğrulanmış, analiz ve görselleştirme metriklerinin bozulması engellenmiştir.
3. **Tekrarlanabilirlik:** Sabit tohum (seed=42) kuralı tam olarak sağlanmış, projenin tekrarlanabilirlik ilkesi korunmuştur.
