# Görev 3 Önerisi: Çok Ajanlı Şirket Programı (Lojistik Gecikme Riski)

**Şirket:** Grup B — Logistics Intelligence Network (LIN)  
**Tarih:** 24 Kasım 2026  
**Dönem / Hafta:** Görev 3 — 1. Hafta (Hazırlık, Öneri ve Roller)  
**İlgili Duyuru:** [Duyuru 10](https://github.com/MAKU-VBA-GBT-II/ders/blob/main/Duyuru-10_2026-11-20.md)  
**Son Teslim Tarihi:** 26 Kasım 2026 Perşembe 13:00  

---

## 1. Senaryo Özeti

**Senaryo Başlığı:** *Meteoroloji ve Yol Olaylarına Dayalı Önümüzdeki Haftanın Sevkiyat Gecikme Riski Analizi*

Logistics Intelligence Network (LIN) olarak şirketimiz, aktif sevkiyat operasyonlarında hava koşulları ve yol durumu nedeniyle oluşabilecek gecikmeleri önceden tahmin eden çok ajanlı bir karar destek sistemi geliştirmektedir. Sistem; dış piyasa/kamu verilerini web'den toplayıp şirket içi sevkiyat kayıtlarıyla birleştirerek rota bazlı risk puanı üretmekte, denetimden geçen riskli sevkiyatlar için müşterilere otomatik ve kanıtlı uyarı mesajları hazırlamaktadır.

---

## 2. Üç Ajanın Tanımı

Sistem sırayla çalışan ve birbirini besleyen 3 bağımsız yapay zekâ ajanından oluşur:

1. **Ajan 1 (Web Veri Toplayıcı):** Meteoroloji Genel Müdürlüğü (MGM) dinamik uyarı haritasını (tarayıcı kullanarak), Karayolları Genel Müdürlüğü (KGM) yol bültenini ve güncel akaryakıt fiyatlarını toplayıp ortak JSON formatında doğrulanmış girdi paketi haline getirir.
2. **Ajan 2 (Sevkiyat & Rota Risk Motoru):** Ajan 1'den gelen hava/yol uyarılarını şirketimizin sentetik sevkiyat veri setindeki aktif rotalarla eşleştirir; her rota ve sevkiyat için Python tabanlı risk puanı (0–100) ve tahmini gecikme süresi hesaplar.
3. **Ajan 3 (Denetim, Kalite Kontrol & Müşteri İletişimi):** Üretilen risk puanlarını ve veri tutarlılığını denetler (şüpheli veya eksik veri varsa gerekçesiyle Ajan 1 veya Ajan 2'ye geri gönderir), eşiği aşan yüksek riskli sevkiyatlar için dayandığı resmi uyarı bağlantılarını içeren şeffaf müşteri bilgilendirme mesajları üretir.

---

## 3. Web Kaynakları Listesi

Sistemde toplanacak tüm veriler kamuya açık olup hiçbir kişisel veri (isim, profil, kullanıcı yorumu vb.) içermez. En az bir kaynak tarayıcı otomasyonu (Playwright / Camoufox / Headless Chrome) gerektirecek şekilde seçilmiştir:

| # | Kaynak Adı | Web Adresi (URL) | Sağladığı Veri | Tarayıcı Gereksinimi | robots.txt & Kullanım Şartları (ToS) Kontrolü |
|:---:|---|---|---|:---:|---|
| **1** | **MGM Meteorolojik Uyarılar** | `https://www.mgm.gov.tr/tahmin/meteorolojik-uyari-ve-degerlendirmeler.aspx` | İl bazlı sarı/turuncu/kırmızı fırtına, kar, yoğun yağış uyarıları | **Evet (Zorunlu)** | Kamu bilgilendirme haritasıdır. Dinamik Leaflet/SVG harita render edildiğinden tarayıcı şarttır. robots.txt engeli yoktur; istekler arası 3 saniye bekleme uygulanır. |
| **2** | **KGM Günlük Yol Durumu** | `https://www.kgm.gov.tr/Sayfalar/KGM/SiteTr/YolDanisma/GunlukYolDurumuBulteni.aspx` | Güzergah bazlı kapalı yollar, heyelan/kar çalışmaları ve tek şerit uygulamaları | **Hayır (Basit HTTP / Tablo)** | Kamuya açık günlük bültendir. Tablo formatında HTML çıktısı verir. robots.txt taramaya açıktır; kişisel veri içermez. |
| **3** | **Açık Akaryakıt Fiyat Tarifesi** | `https://www.petrolofisi.com.tr/akaryakit-fiyatlari` | İl bazlı güncel motorin/benzin pompa fiyatları (navlun maliyet çarpanı) | **Opsiyonel (Dinamik Form/Select)** | Kamuya açık serbest tarife listesidir. Form seçimi ile il bazlı liste çekilir. robots.txt engeli yoktur. |

---

## 4. Takım Rolleri Dağılımı

Duyuru 10 kapsamında tanımlanan 4 rol ve üstlenen takım üyeleri:

| Rol | Üstlenen Üye | Görev ve Sorumluluk Alanı |
|---|---|---|
| **Çekirdek ve Arayüz** | **Sude Çukurtaş** (PM)<br>*(Destek: İpek Özarslan - Junior)* | ACP (Agent Client Protocol) bağlantısının kurulması, Claude Code / Vibe CLI süreçlerinin başlatılması ve yönetimi, ajanlar arası mesaj protokolü, kullanıcı onay/izin ekranı ve oturum loglarının tutulması. |
| **Ajan 1** | **Sema Coşkun** (Geliştirici) | Zincirin ilk ajanı: Web veri toplama, tarayıcı otomasyonu (Playwright/Headless), `robots.txt` uyumu, girdi doğrulama ve veriyi ortak JSON mesaj formatına getirme. |
| **Ajan 2** | **Aykut Çakıcı** (Geliştirici) | Zincirin ikinci ajanı: Ajan 1 çıktısını şirketin güncel sevkiyat simülasyonu ile eşleme, Python analiz motoru, rota risk puanlama ve gecikme tahmini algoritması. |
| **Ajan 3** | **Ece Naz Aktürk** (Geliştirici) | Zincirin üçüncü ajanı: Çıktı denetimi, eşik kontrolleri, tutarsızlık durumunda işi gerekçeli geri gönderme ve kaynak bağlantılı müşteri uyarı mesajlarını hazırlama. |

---

## 5. Abonelikler ve Geliştirme Ortamı

Programın içinde hiçbir sabit API anahtarı barındırılmayacaktır. Program, öğretim elemanının ve kullanıcıların kendi ortamlarındaki ACP destekli araçları üzerinden çalışacaktır.

| Üye Adı Soyadı | GitHub Kullanıcı Adı | Tanımlı Rol | Kullanılan Araç / Abonelik |
|---|---|---|---|
| **Sude Çukurtaş** | `@sudecukurtas` | PM / Çekirdek ve Arayüz | Claude Code & Antigravity |
| **Aykut Çakıcı** | `@Aykuutt` | Ajan 2 (İşleme & Risk Analizi) | Claude Code & Antigravity |
| **Sema Coşkun** | `@sema788` | Ajan 1 (Web & Tarayıcı Veri Toplama) | Claude Code |
| **Ece Naz Aktürk** | `@ece-naz` | Ajan 3 (Denetim & Teslim Raporu) | Claude Code & Antigravity |
| **İpek Özarslan** | `@ipek0-0` | Junior (Arayüz & Entegrasyon Destek) | Claude Code |

> **Not:** Takım genelinde ortak standart olarak ACP uyumlu **Claude Code** aracı ve **Antigravity** geliştirme ortamı benimsenmiştir. Sistem ayrıca öğretim elemanının bilgisayarında varsayılan olan **Mistral Vibe** ile de tam uyumlu çalışacak şekilde konfigüre edilecektir.
