# Sprint Raporu — Hafta 05 (28.10–03.11.2026)

**Şirket:** Grup B — Logistics Intelligence Network (LIN) / Sevkiyatlar · **PM:** Sude Çukurtaş  
**Tarih:** 03.11.2026  
**Görev:** Görev 2 — Parametreli Lojistik Simülasyonu, 5 Temel Metrik Analizi, Görselleştirme ve Test Hattı (1. Hafta)  

---

## Planlanan

| Issue / PR | Başlık | Atanan | Son tarih | Kabul kriteri |
|---|---|---|---|---|
| #46 / PR #52 | [DQ] Görev 2 Veri Sözlüğü, Simülasyon Parametreleri ve Analiz Planı | Ece Naz Aktürk (DQ) | 01.11.2026 23:59 | `docs/veri-sozlugu.md` (v2.0, 10 sütun, 900 satır hedefi, parametreler), `skills/dq-sozluk/SKILL.md` ve güncel `AGENTS.md` |
| #47 / PR #53 | [BE] Görev 2 Parametreli Lojistik Sevkiyat Simülasyonu | Aykut Çakıcı (BE) | 02.11.2026 23:59 | `src/simulasyon.py` (CLI argümanları, tohum 42, `dogrula()` fonksiyonu), `data/lojistik_sevkiyat_g2.csv` (tam 900 satır), `skills/be-simulasyon/SKILL.md` |
| #49 / PR #54 | [DQ] Görev 2 Analiz Raporu, 5 Metrik Hesabı ve Gereksinim Dokümanı | Ece Naz Aktürk (DQ) | 02.11.2026 23:59 | `docs/analiz-g2.md` (5 analitik metrik, ISO hafta kırılımı, 3 gözlem, 1 eylem önerisi, FE devir teslim notu), `docs/requirements.md`, `src/analiz_g2.py` |
| #50 / PR #55 | [DQ] Görev 2 Veri Kalite Test Senaryoları ve Koşum Günlüğü | Ece Naz Aktürk (DQ) | 02.11.2026 23:59 | `tests/test-cases.md` (10 senaryo), `tests/test-log.md` (3. koşum kaydı), `src/test_calistir.py` (otomatik test motoru), `skills/dq-test/SKILL.md` |
| #48 / PR #56 | [FE] Görev 2 Grafikleri ve fe-gorsel Skill'i | Sema Coşkun (FE) | 03.11.2026 23:59 | `src/gorsel_g2.py`, 3 adet grafik (`visuals/zaman_serisi_haftalik.png`, `visuals/mod_gecikme_kirilimi.png`, `visuals/teslimat_suresi_dagilimi.png`), `skills/fe-gorsel/SKILL.md` |
| - | [PM] Hafta 5 Koordinasyonu, PR İncelemeleri ve Sprint Raporu | Sude Çukurtaş (PM) | 03.11.2026 23:59 | PR süreçlerinin yönetimi, devir teslim zinciri takibi, `reports/report-w05.md` hazırlanması |

---

## Yapılan

| Issue / PR | Kanıt (commit / dosya / PR) | Durum |
|---|---|---|
| #46 / PR #52 | `docs/veri-sozlugu.md` (v2.0), `skills/dq-sozluk/SKILL.md`, `AGENTS.md` — commit `518bb1e`, PR #52 merge `2e9f9aa` | ✅ Kapandı |
| #47 / PR #53 | `src/simulasyon.py`, `data/lojistik_sevkiyat_g2.csv` (900 satır, tohum 42), `skills/be-simulasyon/SKILL.md` — commit `63691cd`, PR #53 merge `869dd1b` | ✅ Kapandı |
| #49 / PR #54 | `docs/analiz-g2.md`, `docs/requirements.md` (v2.0), `src/analiz_g2.py`, `skills/dq-analiz/SKILL.md` — commit `c9c2785`, PR #54 merge `dffe2ea` | ✅ Kapandı |
| #50 / PR #55 | `tests/test-cases.md` (10 senaryo), `tests/test-log.md` (3. koşum: 10/10 geçti), `src/test_calistir.py`, `skills/dq-test/SKILL.md` — commit `c749dfc`, PR #55 merge `b777350` | ✅ Kapandı |
| #48 / PR #56 | `src/gorsel_g2.py`, 3 adet PNG görsel, `skills/fe-gorsel/SKILL.md` — commit `1add6b1`, `b650a1a`, `a253a75`, PR #56 merge `844f3b7` | ✅ Kapandı |
| PM | Hafta 5 PR akışı denetimi, devir teslim kontrolleri, `reports/report-w05.md` | ✅ Tamamlandı |

### Analitik ve Operasyonel Çıktı Özeti (`docs/analiz-g2.md`)
- **Toplam Sevkiyat & Ciro:** 60 günlük simülasyonda günlük ortalama 15 sevkiyat hedefiyle tam 900 sevkiyat gerçekleştirilmiş ve 3.351.304,20 TL navlun cirosu elde edilmiştir.
- **Başarı ve İptal Dağılımı:** 851 sevkiyat (%94,6) başarıyla teslim edilirken, 49 sevkiyat (%5,4) operasyonel nedenlerle iptal edilmiştir (Hedeflenen %5 parametresiyle tam uyumlu).
- **Ortalama Teslim Süresi:** İptaller hariç net ortalama teslim süresi **20,86 saat**; ortalama sevkiyat ağırlığı **4.969,93 kg** olarak gerçekleşmiştir.
- **Taşıma Modları Dağılımı & Gecikme:**
  - **Kara:** 451 sevkiyat (%50,1 pay, 1,59M TL), gecikme oranı **%17,5** (en yüksek hacim ve en yüksek gecikme).
  - **Demiryolu:** 186 sevkiyat (%20,7 pay, 652K TL), gecikme oranı **%17,3**.
  - **Hava:** 135 sevkiyat (%15,0 pay, 702K TL), gecikme oranı **%12,6** (sevkiyat başı 5.205,93 TL ile en yüksek birim getiri).
  - **Deniz:** 128 sevkiyat (%14,2 pay, 406K TL), gecikme oranı **%10,7** (en güvenilir mod).
- **Zaman Serisi İstikrarı:** W01 (4 günlük başlangıç: 60 sevkiyat) haricinde, W02–W09 arasındaki 8 tam haftanın her birinde haftalık tam 105 sevkiyat ve 368K–408K TL aralığında dengeli ciro üretilmiştir.

### Test ve Kalite Özeti (`tests/test-log.md`)
- `src/test_calistir.py` motoru üzerinden 10 senaryonun tamamı otomatik olarak koşulmuştur.
- **Sonuç:** 10 senaryo koşuldu, 10'u başarıyla geçti (0 hata, 0 ihlal). Veri kalitesi skoru: **%100 (Kusursuz)**.
- Dosya varlığı, UTF-8 kodlama, 900 satır hedefi, 10 sütun şema uyumu, benzersiz ID formatı (`SVK-G2-0001`...`SVK-G2-0900`), 60 günlük ISO tarih aralığı, 8 merkezli rota mantığı, pozitif değerler ve 49 iptal kaydında teslim süresinin boş bırakılması kuralı teyit edilmiştir.

---

## Devir Teslim Zinciri (Görev 2)

Hafta 5 boyunca `AGENTS.md`'de tanımlanan Görev 2 devir teslim zinciri adım adım işletilmiştir:

1. **DQ → BE (ve Paralel FE Taslak):** DQ Ece Naz Aktürk veri sözlüğünü (`docs/veri-sozlugu.md` v2.0), simülasyon parametrelerini ve analiz planını tanımlayarak PR #52 ile sisteme kazandırdı. BE Aykut Çakıcı simülasyon kodlamasına başlarken; FE Sema Coşkun paralel hatta şemayı referans alarak grafik iskelet kodunu (`src/gorsel_g2.py`) ve taslakları oluşturdu (`1add6b1`).
2. **BE → DQ (Veri Doğrulama ve PR Onayı):** BE Aykut Çakıcı `src/simulasyon.py` betiğini ve tohum 42 ile üretilen 900 satırlık `data/lojistik_sevkiyat_g2.csv` dosyasını `feature/veri` dalında tamamlayıp PR #53'ü açtı. DQ Ece Naz Aktürk şema ve veri sözlüğü uyumunu doğrulayarak PR'ı onayladı ve `main`'e merge etti (`869dd1b`).
3. **DQ → FE (Analiz Metrikleri ve Gereksinim Devri):** DQ Ece Naz Aktürk, `src/analiz_g2.py` betiği ile 5 temel metriği hesapladı; `docs/analiz-g2.md` raporunu ve `docs/requirements.md` ürün gereksinim dokümanını hazırlayarak PR #54 ile sundu. Raporun 4. bölümünde FE'ye grafik üretiminde kullanılacak doğrulanmış sayılar eksiksiz devredildi.
4. **DQ → Kalite ve Test Hattı:** DQ Ece Naz Aktürk 10 test senaryosunu içeren `tests/test-cases.md` ve otomatik test koşucu `src/test_calistir.py` betiğini hazırladı. 3. test koşumunu tamamlayıp `tests/test-log.md` kütüğüne işleyerek PR #55 ile sisteme kazandırdı.
5. **FE → DQ / PM (Nihai Grafikler ve Görselleştirme Onayı):** FE Sema Coşkun, `feature/gorsel` dalında `main`'den son analiz verilerini alarak (`c1bfe15`), analiz raporundaki doğrulanmış sayılarla birebir uyumlu 3 nihai grafiği üretti (`b650a1a`), `skills/fe-gorsel/SKILL.md`'yi güncelledi (`a253a75`) ve PR #56'yı açtı. DQ onayı sonrasında PR `main`'e merge edildi (`844f3b7`).
6. **PM → Sprint Mühürleme:** PM Sude Çukurtaş tüm Issue ve PR'ların kanıt yorumlarıyla kapandığını, dalların entegrasyonunu ve `main` dalının temizliğini teyit ederek sprint raporunu (`reports/report-w05.md`) tamamladı.

---

## Tıkanan / Yönetilen Riskler

1. **Rol Rotasyonu Adaptasyonu:** Görev 1'den Görev 2'ye geçişte proje planı gereği roller döndürülmüştür (DQ: Aykut → Ece, BE: Sema → Aykut, FE: Ece → Sema). `AGENTS.md` ve tüm rol skill dokümanları hızla senkronize edilerek görev yetki karmaşası önlenmiştir.
2. **Main Dalı Koruma ve PR Zorunluluğu Disiplini:** Hafta 5 kuralı ("`main`'e yalnızca PR ile girilir; kod/veri PR'ları DQ onayı olmadan merge edilmez") eksiksiz uygulanmıştır. Tüm çalışmalar (`feature/sozluk-g2`, `feature/veri`, `feature/analiz-g2`, `feature/test-g2`, `feature/gorsel`) bağımsız dallarda yürütülmüş, her PR DQ onayı ve kanıt doğrulaması ile merge edilmiştir.
3. **FE Blokajının Önlenmesi (Paralel İş Akışı):** BE veri simülasyonunu kodlarken FE'nin veri beklemesini önlemek adına, veri sözlüğündeki şema baz alınarak FE tarafında örnek veriyle çalışan iskelet kod hazırlanmış; veri `main`'e girdikten sonra `git merge main` yapılarak gerçek sayılarla grafikler dakikalar içinde nihai hale getirilmiştir.
4. **İptal Kayıtlarının İstatistiksel Sapma Riski:** 49 iptal edilen sevkiyatta teslim süresinin analitik ortalamayı aşağı çekmemesi veya yapay sıfır değeri üretmemesi için sözlükte NaN (boş) bırakılması zorunlu kılınmış, test senaryosu 9 ile doğrulanmıştır.

---

## Kim Ne Yaptı

| Üye | Rol | Başlıca Katkı / Commit'ler | Kapattığı Issue / PR |
|---|---|---|---|
| **Sude Çukurtaş** | PM | Sprint planlama, PR süreçleri ve devir teslim takibi, `reports/report-w05.md`, pano koordinasyonu | PM Koordinasyon, Hafta 5 Sprint Raporu |
| **Ece Naz Aktürk** | DQ | `docs/veri-sozlugu.md` (v2.0), `skills/dq-sozluk`, `docs/analiz-g2.md`, `docs/requirements.md`, `src/analiz_g2.py`, `skills/dq-analiz`, `tests/test-cases.md`, `tests/test-log.md` (10/10), `src/test_calistir.py`, `skills/dq-test`, PR inceleme ve onayları (`518bb1e`, `c9c2785`, `c749dfc`) | #46 (PR #52), #49 (PR #54), #50 (PR #55), PR #56 İnceleme & Onay |
| **Aykut Çakıcı** | BE | `src/simulasyon.py` (CLI argümanları, tohum 42, `dogrula()`), `data/lojistik_sevkiyat_g2.csv` (900 satır), `skills/be-simulasyon/SKILL.md` (`63691cd`) | #47 (PR #53) |
| **Sema Coşkun** | FE | `src/gorsel_g2.py`, 3 adet grafik üretimi (`visuals/zaman_serisi_haftalik.png`, `visuals/mod_gecikme_kirilimi.png`, `visuals/teslimat_suresi_dagilimi.png`), `skills/fe-gorsel/SKILL.md` (`1add6b1`, `b650a1a`, `a253a75`) | #48 (PR #56) |
| **İpek Özarslan** | Junior | Test koşumlarının takibi, simülasyon ve veri doğrulama senaryolarının incelenmesi | Junior Destek / Doğrulama |

---

## Gelecek Hafta Planı (Hafta 6 — Görev 2 Kapanışı, Test ve Sürüm)

1. **Uçtan Uca Entegrasyon ve Sınır Testleri:** Simülasyon veri hattının farklı tohum ve uç parametrelerdeki davranışı test edilecek.
2. **İyileştirme ve Hata Kayıtları:** Ekip üyeleri veri ve görselleştirme hattında en az 2 enhancement/bug kaydı açıp `Fixes #no` formatıyla çözecek.
3. **Görev 2 Final Sürümü:** Tüm G2 gereksinimlerinin karşılandığı doğrulanıp `gorev2-final` release etiketi oluşturulacak.
4. **Görev 3 Hazırlığı (B2B Veri Değişimi):** Partner şirketimiz Grup A ile ortak veri formatları ve entegrasyon arayüzleri planlanacak.

---

*Bu rapor `pm-rapor` skill'i kullanılarak Antigravity / Gemini 3.8 Flash modeli ile depodaki gerçek izler (PR'lar, Issue'lar, commit'ler, test logları ve analiz dokümanları) doğrulanarak üretilmiştir.*
