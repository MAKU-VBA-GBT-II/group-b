# Dönem Raporu 1 — PM'den Öğretim Elemanına

**Şirket:** Grup B — Logistics Intelligence Network (LIN) / Sevkiyatlar  
**PM:** Sude Çukurtaş  
**Tarih:** 04.11.2026  
**Dönem Kapsamı:** Hafta 01 – Hafta 05 (Görev 1 ve Görev 2 Kapanışı)  
**Hedef Kitle:** Öğretim Elemanı (@eofdred)  

---

## 1. Yönetici Özeti

Grup B (Logistics Intelligence Network - LIN), dönemin ilk yarısında Görev 1 (temel veri üretim ve analiz hattı) ve Görev 2 (parametreli lojistik sevkiyat simülasyonu, 5 analitik metrik, 3 grafik ve 10/10 veri kalite test hattı) teslimatlarını başarıyla mühürlemiştir. Takım, dönem planında öngörülen rol rotasyonunu (DQ: Aykut Çakıcı, BE: Sema Coşkun, FE: Ece Naz Aktürk, Junior: İpek Özarslan, PM: Sude Çukurtaş) başarıyla işletmiş; `main` dalına yalnızca PR ve DQ onayıyla giriş disiplinine eksiksiz uymuştur. 60 günlük simülasyonda 900 sentetik sevkiyat ve 3,35M TL navlun hacmi sıfır veri ihlaliyle modellenmiş olup, şirketimiz 5 Kasım bitiş hattına açık gecikmiş iş bırakmadan girmiştir.

---

## 2. Teslim Edilenler

Görev 1'in kapanışından (`gorev1-final` sürümü) bugüne kadar tamamlanan ve `main` dalına entegre edilen başlıca işler:

| Rol | Teslim Edilen Çıktı / Dosya | İlgili Issue / PR | Kanıt Commit / Hash |
|---|---|---|---|
| **DQ** | `docs/veri-sozlugu.md` (v2.0, 10 sütun şeması, 900 satır hedefi) ve `skills/dq-sozluk/SKILL.md` | Issue #46 / PR #52 | `518bb1e`, PR merge `2e9f9aa` |
| **BE** | `src/simulasyon.py` (CLI argümanları, tohum 42, `dogrula()`), `data/lojistik_sevkiyat_g2.csv` (900 satır) ve `skills/be-simulasyon/SKILL.md` | Issue #47 / PR #53 | `63691cd`, PR merge `869dd1b` |
| **DQ** | `docs/analiz-g2.md` (5 analitik metrik, ISO hafta kırılımı), `docs/requirements.md`, `src/analiz_g2.py` ve `skills/dq-analiz/SKILL.md` | Issue #49 / PR #54 | `c9c2785`, PR merge `dffe2ea` |
| **DQ** | `tests/test-cases.md` (10 senaryo), `tests/test-log.md` (10/10 koşum), `src/test_calistir.py` ve `skills/dq-test/SKILL.md` | Issue #50 / PR #55 | `c749dfc`, PR merge `b777350` |
| **FE** | `src/gorsel_g2.py`, 3 adet analitik grafik (`visuals/zaman_serisi_haftalik.png`, `visuals/mod_gecikme_kirilimi.png`, `visuals/teslimat_suresi_dagilimi.png`), `skills/fe-gorsel/SKILL.md` | Issue #48 / PR #56 | `1add6b1`, `b650a1a`, `a253a75`, PR merge `844f3b7` |
| **Junior** | Test senaryolarının yerel ortamda bağımsız doğrulanması, veri sözlüğü kontrolleri | Issue #51 | Issue #51 kanıt yorumu |
| **PM** | `reports/report-w04.md`, `reports/report-w05.md`, `AGENTS.md` skill envanteri yönetimi, Görev 2 Milestone kapanışı | PM Koordinasyon | `ec74266`, `127e58c`, `ad2cbd4` |

---

## 3. Sayılarla Dönem (Süreç KPI'ları)

Tüm veriler GitHub API ve `git log` kayıtları üzerinden nesnel olarak derlenmiştir:

| Süreç KPI Metriği | Ölçülen Değer | Açıklama |
|---|---|---|
| **Toplam Açılan Issue Sayısı** | **49** | PR'lar hariç açılan iş kartı sayısı |
| **Kapatılan Issue Sayısı** | **48** | Kanıt veya gerekçeli kapatılan Issue sayısı |
| **Merge Edilmiş PR Sayısı** | **10** | Bağımsız özellik dallarından `main`'e merge edilen PR sayısı |
| **PR Başına Ort. İlk İnceleme Süresi** | **~11,0 saat** (658,5 dk) | PR açılışı ile ilk yetkili inceleme/yorum arasındaki süre |
| **Son Tarihi Geçen (Geciken) İş Sayısı** | **0** | Görev 2 kapsamındaki tüm işler takviminde teslim edildi |

### Üye Bazında Katkı Dağılımı:
| Üye | Rol | Commit Sayısı | Kapatılan Issue Sayısı | Birincil Sorumluluk Alanı |
|---|---|---|---|---|
| **Sude Çukurtaş** | PM | 83 | 4 (+ Genel Koordinasyon) | Sprint planlaması, sürüm yönetimi, raporlama ve pano denetimi |
| **Aykut Çakıcı** | DQ | 24 | 8 | Veri sözlüğü, şema doğrulama, analiz betikleri ve hata denetimi |
| **Sema Coşkun** | BE | 16 | 9 | Parametreli veri simülasyonu, CSV üretimi ve şema filtreleme |
| **Ece Naz Aktürk** | FE | 11 | 9 | Analitik grafik üretimi, görselleştirme motoru ve skill dokümantasyonu |
| **İpek Özarslan** | Junior | 4 | 4 | Test senaryo koşumları, ortam doğrulama ve kullanıcı desteği |

---

## 4. Tıkananlar ve Çözümleri

1. **Sıfır Payda Hata Riski (ZeroDivisionError):**
   - *Problem:* Görev 1 analiz betiğinde iptal veya teslimatsız kırılımlarda gecikme oranı hesaplanırken sıfıra bölünme hatası tespit edildi (#40).
   - *Çözüm:* DQ tarafından hesaplama fonksiyonlarına koşullu payda kontrolü eklendi; PR #40 açılarak `main`'e merge edildi.
2. **BE / FE Bağımlılık Blokajı (Paralel İş Akışı):**
   - *Problem:* FE görselleştirme geliştirmesinin BE veri simülasyonunu beklemesi, sprint teslimini riske atıyordu.
   - *Çözüm:* DQ'nun `docs/veri-sozlugu.md` şeması referans alınarak FE tarafında örnek veriyle çalışan iskelet grafik motoru kodlandı (`1add6b1`). Gerçek veri `main`'e girdiğinde sadece merge yapılarak dakikalar içinde nihai grafikler tamamlandı.
3. **İptal Edilen Sevkiyatların Ortalama Süreyi Bozma Riski:**
   - *Problem:* 49 iptal sevkiyatta teslim süresine yapay 0 atanması, teslimat süresi ortalamalarını saptırıyordu.
   - *Çözüm:* Veri sözlüğüne "iptal sevkiyatlarda teslim süresi boş (NaN) bırakılır" kuralı kondu ve test senaryosu 9 ile kod düzeyinde denetlendi.

---

## 5. Kim Ne Yaptı (Olgusal Bildirim Tablosu)

Duyuru 7 gereği [Issue #57](https://github.com/MAKU-VBA-GBT-II/group-b/issues/57) üzerinden toplanan üye yanıtları:

| Üye / Rol | Ne Teslim Etti? (Kanıtlı) | Neye Takıldı ve Nasıl Aştı? | Gelecek Dönem Hedefi / Önerisi |
|---|---|---|---|
| **Aykut Çakıcı** (DQ) | G1 veri sözlüğü ve analiz hattı (`docs/veri-sozlugu-g1.md`), PR #35 (test koşumu), PR #37 (G1 analiz betiği), PR #40 (sıfır payda düzeltmesi), G2 şema ve test incelemeleri (`5cea41b`, `cc68482`, `8e0e977`, `71f5d34`). | Gecikme oranı hesaplamasında sıfır payda hatası oluştu; formüle koşullu kontrol ekleyerek çözdü. | Veri doğrulama testlerini CI/CD hattına entegre etmek ve B2B partner şemasını karşılayacak otomatik validatör geliştirmek. |
| **Sema Coşkun** (BE) | G1 sentetik veri üretim betiği (`src/veri_uret.py`), CSV şema doğrulama yaması (Fixes #39, commit `b488b95`), `skills/be-simulasyon/SKILL.md` ve G2 parametreli simülasyonu ile 900 satırlık veri seti (`data/lojistik_sevkiyat_g2.csv`, PR #53, commit `63691cd`). | İptal sevkiyatlarda teslim süresinin NaN bırakılması kuralında filtreleme zorluğu yaşandı; sözlük şemasına özel filtreleme fonksiyonuyla çözüldü. | Simülasyon betiğine CLI argüman doğrulama ve `try/except` hata yakalama blokları ekleyerek CLI esnekliğini artırmak. |
| **Ece Naz Aktürk** (FE) | G2 görselleştirme motoru (`src/gorsel_g2.py`), 3 adet analitik grafik (`visuals/zaman_serisi_haftalik.png`, `visuals/mod_gecikme_kirilimi.png`, `visuals/teslimat_suresi_dagilimi.png`), `skills/fe-gorsel/SKILL.md` (PR #56, commit `1add6b1`, `b650a1a`, `a253a75`). | BE verisi gelmeden görsel kodlamanın tıkanması riski; şema bazlı taslak kod yazılarak veri gelince anında merge ile aşıldı. | Statik PNG grafiklerin yanı sıra web ve pano uyumlu etkileşimli dashboard bileşenleri tasarlamak. |
| **İpek Özarslan** (Junior) | G1 ve G2 test senaryolarının (`tests/test-cases.md`) bağımsız yerel koşumu, `tests/test-log.md` 10/10 denetimi ve şema doğrulaması (#51). | Farklı Python sürümlerinde karakter kodlama (UTF-8) ve paket uyumsuzluğu; `requirements.md` ve sanal ortam yönergeleriyle aşıldı. | `docs/user-manual.md` kullanıcı kılavuzunu hazırlamak ve sistemin sıfırdan kurulum testlerini uçtan uca yürütmek. |
| **Sude Çukurtaş** (PM) | Sprint planlaması (W01–W05), PR devir teslim takibi, `reports/report-w04.md`, `reports/report-w05.md`, G1 kapanışı (`gorev1-final` release), kök `AGENTS.md` ve proje panosu koordinasyonu, G2 Milestone kapanışı. | Rol rotasyonunda yetki karmaşası ve dal disiplini riski; "main'e yalnızca PR ve DQ onayıyla girilir" kuralı tavizsiz işletilerek sıfır çakışmayla aşıldı. | Görev 3'te partnerimiz Grup A ile B2B veri değişimi şema protokolünü sprint başında sabitlemek ve entegrasyonu gecikmesiz tamamlamak. |

---

## 6. Dersler (Retrospektif)

1. **Sözleşme Öncelikli Geliştirme (Contract-First):** Veri sözlüğünün kod yazılmadan önce kesinleştirilmesi, BE ve FE'nin birbirini beklemeden paralel çalışabilmesini sağladı. Görev 3'te de bu yöntem partner şirketle uygulanacaktır.
2. **Otomatik Test Koşumunun Gücü:** 10 test senaryosunun tek bir betikle (`src/test_calistir.py`) otomatik koşulması, manuel gözden kaçabilecek şema sapmalarını tamamen engelledi.
3. **PR ve Dal Hijyeni:** Doğrudan `main` dalına commit atılmaması, ekip içinde kod sahiplenmesini ve karşılıklı denetimi en üst düzeye çıkardı.

---

## 7. Görev 3 Hazırlığı (Partner Şirket: Grup A Veri Değişimi Planı)

Duyuru 5 eşleşme tablosu uyarınca Grup B'nin partner şirketi **Grup A**'dır. B2B veri değişimi için planlanan yol haritası:

1. **Şema ve Alan Eşleme (Schema Mapping):**
   - Grup A'nın veri sözlüğü ile LIN (Grup B) sevkiyat şeması (`docs/veri-sozlugu.md`) karşılaştırılacak; ortak anahtarlar (müşteri ID, tedarikçi kodu, ürün grubu, sipariş tarihi) belirlenecektir.
2. **Veri Değişim Formatı Protokolü:**
   - İki şirket arasında veri transferinin UTF-8 kodlamalı JSON veya standartlaştırılmış CSV üzerinden gerçekleştirilmesi kararlaştırılacaktır.
3. **Çapraz Doğrulama Hattı:**
   - Grup A'dan temin edilecek girdi verileri için `src/b2b_dogrula.py` doğrulama modülü yazılarak şema uyumsuzlukları giriş anında engellenecektir.

---

## 8. Araç ve Model Kaydı (Prompt Özeti)

Bu rapor, `pm-rapor` skill'i yönergeleri doğrultusunda, GitHub deposundaki (`MAKU-VBA-GBT-II/group-b`) Issue'lar, PR'lar, `git log` geçmişi ve [Issue #57](https://github.com/MAKU-VBA-GBT-II/group-b/issues/57) altındaki olgusal takım verileri taranarak **Google Antigravity asistanında çalışan Gemini 2.5 Pro** modeli tarafından üretilmiştir.
