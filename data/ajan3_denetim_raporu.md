# Ajan 3 Denetim, Kalite Kontrol ve Müşteri Teslim Raporu

**Rapor Tarihi / Üretim Zamanı:** `2026-11-28T13:31:36Z`  
**Mesaj ID:** `MSG-G3-20261128-A3-001`  
**Referans Mesaj (Ajan 2):** `MSG-G3-20261128-A2-001`  
**Sorumlu:** DQ / Ajan 3 — Ece Naz Aktürk (`@ece-naz`)  
**Şirket:** Grup B — Logistics Intelligence Network (LIN)  

---

## 1. Genel Denetim ve Kalite Kontrol Özeti

| Metrik | Değer | Açıklama |
|---|---|---|
| **Genel Denetim Kararı** | **`ONAYLANDI`** | Ajan 2 çıktı paketi şema, tazelik ve tutarlılık onayından geçti |
| Toplam İncelenen Sevkiyat | 140 | G3 örnek sevkiyat evreni |
| Aktif Sevkiyat | 134 | Rota riski ve yakıt katsayısı uygulanan aktif operasyonlar |
| İptal Sevkiyat | 6 | Operasyonel teslim süresi boş bırakılan iptal kayıtları |
| Ortalama Risk Puanı | 13.13 / 100 | Şirket genel ortalama gecikme riski |
| Kritik Eşik Değeri | **65 Puan** | Eşik üstü sevkiyatlar için müşteri bildirimi zorunludur |
| Kritik Riskli Sevkiyat Sayısı | **1 Adet** | KGM kapalı yol bülteniyle eşleşen rota |

---

## 2. Onaylanan Kritik Riskli Sevkiyat ve Müşteri Mesajı

### 🚨 Sevkiyat: `SVK-G3-0093` (Trabzon -> Adana)
- **Tahmini Ek Gecikme:** `+16.0 saat` (Toplam Teslimat: ~`57.1` saat)
- **Resmi Dayanak Bağlantıları:**
  - **AKARYAKIT**: Trabzon motorin 86.5 TL/LT — [https://www.petrolofisi.com.tr/akaryakit-fiyatlari](https://www.petrolofisi.com.tr/akaryakit-fiyatlari)
  - **KGM**: Ilgar Geçidi (kapali) — [https://www.kgm.gov.tr/Sayfalar/KGM/SiteTr/YolDanisma/GunlukYolDurumuBulteni.aspx](https://www.kgm.gov.tr/Sayfalar/KGM/SiteTr/YolDanisma/GunlukYolDurumuBulteni.aspx)
  - **KGM**: Pozantı Kavşağı (Ankara-Niğde Otoyolu) (tek_serit) — [https://www.kgm.gov.tr/Sayfalar/KGM/SiteTr/YolDanisma/GunlukYolDurumuBulteni.aspx](https://www.kgm.gov.tr/Sayfalar/KGM/SiteTr/YolDanisma/GunlukYolDurumuBulteni.aspx)

**Üretilen Müşteri Bilgilendirme Metni:**
> Sayın Müşterimiz,
> 
> **SVK-G3-0093** takip numaralı **Trabzon -> Adana** güzergahındaki sevkiyatınız, planlanan operasyon takvimine göre tahmini **+16.0 saat** operasyonel gecikme riski altındadır (Tahmini toplam teslimat süresi: ~57.1 saat).
> 
> **Gecikme Gerekçesi:**
> Güzergah üzerindeki resmi karayolları bültenlerinde bildirilen çalışma ve hava şartları:
> - **AKARYAKIT**: Trabzon motorin 86.5 TL/LT ([Resmi Duyuru Bağlantısı](https://www.petrolofisi.com.tr/akaryakit-fiyatlari))
> - **KGM**: Ilgar Geçidi (kapali) ([Resmi Duyuru Bağlantısı](https://www.kgm.gov.tr/Sayfalar/KGM/SiteTr/YolDanisma/GunlukYolDurumuBulteni.aspx))
> - **KGM**: Pozantı Kavşağı (Ankara-Niğde Otoyolu) (tek_serit) ([Resmi Duyuru Bağlantısı](https://www.kgm.gov.tr/Sayfalar/KGM/SiteTr/YolDanisma/GunlukYolDurumuBulteni.aspx))
> 
> Logistics Intelligence Network (LIN) operasyon merkezimiz güzergah güvenliğini anlık izlemekte olup akaryakıt ve rota optimizasyonuyla teslimatınızı en güvenli sürede tamamlamak için çalışmaktadır.
> 
> Detaylı bilgi ve canlı takip için müşteri destek hattımızla iletişime geçebilirsiniz.
> Saygılarımızla,
> **Logistics Intelligence Network (LIN) — Operasyonel İletişim Merkezi**

---
## 3. Ajan 3 Skill Doğrulama ve ACP Zincir Uyumu
- **Alma Skill'i (`skills/ajan3-alma`):** Ajan 2 JSON paketi eksik alan, aralık aşımı ve mantıksal tutarsızlık filtrelerinden geçirildi.
- **İşleme Skill'i (`skills/ajan3-isleme`):** Risk puanı eşiği (65) filtresi çalıştı; KGM kapalı yol bülteniyle rota tutarlılığı teyit edildi.
- **Teslim Skill'i (`skills/ajan3-teslim`):** Resmi duyuru linki içeren müşteri mesajı üretilerek `data/ajan3_mesaj.json` oluşturuldu.

*Bu rapor Logistics Intelligence Network (LIN) Ajan 3 denetim motoru tarafından üretilmiştir.*