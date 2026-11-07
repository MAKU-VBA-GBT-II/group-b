# Dönem Raporu 1 — PM'den Öğretim Elemanına

**Şirket:** Grup B — Logistics Intelligence Network (LIN) / Sevkiyatlar  
**PM:** Sude Çukurtaş (`@sudecukurtas`)  
**Tarih:** 07.11.2026  
**Dönem Kapsamı:** Hafta 01 – Hafta 05 (Görev 1 Kapanışı ve Görev 2 Mini Ürün Teslimi)  
**Hedef Kitle:** Öğretim Elemanı (@eofdred)  
**Dayanak:** Kapatılan Issue [#64](https://github.com/MAKU-VBA-GBT-II/group-b/issues/64) (*DÖNEM RAPORU 1*), [Duyuru 7](https://github.com/MAKU-VBA-GBT-II/ders/blob/main/Duyuru-7_2026-11-01.md), [Duyuru 5](https://github.com/MAKU-VBA-GBT-II/ders/blob/main/Duyuru-5_2026-10-22.md) ve [`AGENTS.md`](https://github.com/MAKU-VBA-GBT-II/group-b/blob/main/AGENTS.md)

---

## 1. Yönetici Özeti

Grup B (Logistics Intelligence Network - LIN), 2026-2027 Güz dönemi ilk yarısında planlanan **Görev 1** (lojistik veri sözlüğü, sentetik veri üretim motoru, 5 temel analitik metrik ve görselleştirme) ve **Görev 2** (parametreli lojistik sevkiyat simülasyonu, 60 günlük sentetik zaman serisi, 10 senaryolu otomatik veri kalite hattı ve 3 modlu analitik grafik seti) teslimatlarını eksiksiz tamamlamıştır. Takımımız, dönem başında belirlenen rol rotasyonunu (Görev 1'de DQ: Aykut, BE: Sema, FE: Ece; Görev 2'de BE: Aykut, FE: Sema, DQ: Ece; tüm süreçte PM: Sude, Junior: İpek) başarıyla işletmiş; `main` dalına yalnızca Pull Request ve DQ onayıyla giriş disiplinini tavizsiz uygulamıştır. Duyuru 7'de belirlenen 5 Kasım 23:59 eşiğine repoda **hiçbir açık/gecikmiş iş bırakılmadan (51 kapalı, 0 açık Issue)** girilmiş olup, 900 satırlık deterministik lojistik veri hattı sıfır hata ile mühürlenmiştir.

---

## 2. Teslim Edilenler

Görev 1'in kapanışından (`gorev1-final` sürümü) bugüne kadar Görev 2 kapsamında tamamlanan, test edilen ve `main` dalına entegre edilen başlıca işler kanıt linkleriyle aşağıda listelenmiştir:

| Rol | Teslim Edilen Çıktı / Dosya | İlgili Issue / PR | Kanıt Commit / Hash | Durum |
|---|---|---|---|---|
| **DQ** (Ece Naz Aktürk) | `docs/veri-sozlugu.md` (v2.0, 10 sütun, 5 parametre, 900 satır kuralı), `skills/dq-sozluk/SKILL.md`, `AGENTS.md` | Issue [#46](https://github.com/MAKU-VBA-GBT-II/group-b/issues/46) / PR [#52](https://github.com/MAKU-VBA-GBT-II/group-b/pull/52) | Commit [`518bb1e`](https://github.com/MAKU-VBA-GBT-II/group-b/commit/518bb1e), PR merge [`2e9f9aa`](https://github.com/MAKU-VBA-GBT-II/group-b/commit/2e9f9aa) | ✅ Merge Edildi |
| **BE** (Aykut Çakıcı) | `src/simulasyon.py` (CLI argümanlı deterministik motor, tohum 42, `dogrula()`), `data/lojistik_sevkiyat_g2.csv` (900 satır), `skills/be-simulasyon/SKILL.md` | Issue [#47](https://github.com/MAKU-VBA-GBT-II/group-b/issues/47) / PR [#53](https://github.com/MAKU-VBA-GBT-II/group-b/pull/53) | Commit [`63691cd`](https://github.com/MAKU-VBA-GBT-II/group-b/commit/63691cd), PR merge [`869dd1b`](https://github.com/MAKU-VBA-GBT-II/group-b/commit/869dd1b) | ✅ Merge Edildi |
| **DQ** (Ece Naz Aktürk) | `docs/analiz-g2.md` (5 metrik, ISO hafta kırılımı, 3 gözlem, 1 eylem önerisi), `docs/requirements.md`, `src/analiz_g2.py`, `skills/dq-analiz/SKILL.md` | Issue [#49](https://github.com/MAKU-VBA-GBT-II/group-b/issues/49) / PR [#54](https://github.com/MAKU-VBA-GBT-II/group-b/pull/54) | Commit [`c9c2785`](https://github.com/MAKU-VBA-GBT-II/group-b/commit/c9c2785), PR merge [`dffe2ea`](https://github.com/MAKU-VBA-GBT-II/group-b/commit/dffe2ea) | ✅ Merge Edildi |
| **DQ** (Ece Naz Aktürk) | `tests/test-cases.md` (10 senaryo), `src/test_calistir.py` (otomatik test motoru), `tests/test-log.md` (10/10 koşum), `skills/dq-test/SKILL.md` | Issue [#50](https://github.com/MAKU-VBA-GBT-II/group-b/issues/50) / PR [#55](https://github.com/MAKU-VBA-GBT-II/group-b/pull/55) | Commit [`c749dfc`](https://github.com/MAKU-VBA-GBT-II/group-b/commit/c749dfc), PR merge [`b777350`](https://github.com/MAKU-VBA-GBT-II/group-b/commit/b777350) | ✅ Merge Edildi |
| **FE** (Sema Coşkun) | `src/gorsel_g2.py`, 3 nihai PNG görsel (`visuals/zaman_serisi_haftalik.png`, `visuals/mod_gecikme_kirilimi.png`, `visuals/teslimat_suresi_dagilimi.png`), `skills/fe-gorsel/SKILL.md` | Issue [#48](https://github.com/MAKU-VBA-GBT-II/group-b/issues/48) / PR [#56](https://github.com/MAKU-VBA-GBT-II/group-b/pull/56) | Commit [`1add6b1`](https://github.com/MAKU-VBA-GBT-II/group-b/commit/1add6b1), [`b650a1a`](https://github.com/MAKU-VBA-GBT-II/group-b/commit/b650a1a), [`a253a75`](https://github.com/MAKU-VBA-GBT-II/group-b/commit/a253a75), PR merge [`844f3b7`](https://github.com/MAKU-VBA-GBT-II/group-b/commit/844f3b7) | ✅ Merge Edildi |
| **Junior** (İpek Özarslan) | G2 bağımsız parametre testi (8 kombinasyon tohum/gün/hacim analizi, sınır değer tespiti), veri sözlüğü şema incelemesi | Issue [#51](https://github.com/MAKU-VBA-GBT-II/group-b/issues/51) | Issue #51 doğrulama kütüğü | ✅ Kapandı |
| **PM** (Sude Çukurtaş) | Hafta 5 sprint koordinasyonu, PR devir teslim zinciri denetimi, pano hijyeni, `reports/report-w05.md` | Issue [#64](https://github.com/MAKU-VBA-GBT-II/group-b/issues/64) | Commit [`127e58c`](https://github.com/MAKU-VBA-GBT-II/group-b/commit/127e58c), [`ad2cbd4`](https://github.com/MAKU-VBA-GBT-II/group-b/commit/ad2cbd4), [`b50cf2a`](https://github.com/MAKU-VBA-GBT-II/group-b/commit/b50cf2a) | ✅ Tamamlandı |

---

## 3. Sayılarla Dönem (Süreç KPI'ları)

Tüm metrikler GitHub REST API ve deponun Git geçmişinden doğrudan çekilmiş, PM tarafından doğrulanmıştır:

| Metrik | Değer | Açıklama |
|---|:---:|---|
| **Açılan Saf Issue Sayısı** | **51** | G1, G2, Yan Görevler ve koordinasyon kartlarının toplamı |
| **Kapatılan Saf Issue Sayısı** | **51** | Duyuru 7 gereği tüm kartlar kanıt yorumuyla kapatılmıştır |
| **Açıkta Kalan Issue Sayısı** | **0** | %100 kapanış oranı (Sıfır sahipsiz/açık iş) |
| **Merge Edilen PR Sayısı** | **10** | Tüm PR'lar onay mekanizması işletilerek merge edilmiştir |
| **PR Başına İlk İnceleme Süresi** | **10,98 saat** | PR açılışı ile ilk inceleme/onay yorumu arasındaki ortalama süre |
| **Son Tarihi Geçen (Geciken) İş Sayısı** | **0** | Hem G1 hem de G2 sprint son tarihlerine tam uyum sağlanmıştır |

### Üye Bazında Commit ve Kapatılan Issue Dağılımı

| Üye | GitHub Kullanıcı Adı | Dönem Rolleri (G1 → G2) | Commit Sayısı | Kapatılan / Katkı Verilen Issue |
|---|---|---|:---:|:---:|
| **Sude Çukurtaş** | `@sudecukurtas` | PM → PM | 86 | 6 |
| **Aykut Çakıcı** | `@Aykuutt` | DQ → BE | 26 | 9 |
| **Sema Coşkun** | `@sema788` | BE → FE | 16 | 10 |
| **Ece Naz Aktürk** | `@ece-naz` | FE → DQ | 11 | 10 |
| **İpek Özarslan** | `@ipek0-0` | Junior → Junior | 4 | 5 |
| *Ders Altyapısı / Bot* | `@eofdred`, `@maku-vba` | Hoca / Şablon Altyapısı | 4 | 20 (Genel/Ortak) |
| **Toplam** | | | **147** | **51** (Net) |

---

## 4. Tıkananlar ve Çözümleri

Dönem boyunca yaşanan başlıca teknik ve süreç tıkanıklıkları, Issue [#64](https://github.com/MAKU-VBA-GBT-II/group-b/issues/64) altındaki resmi üye beyanlarıyla şu şekilde çözülmüştür:

1. **Sıfır Payda (`ZeroDivisionError`) Hesaplama Riski (DQ/BE):**
   - *Problem:* Görev 1 analizlerinde bazı filtreleme ve mod kırılımlarında hiç iptal veya teslimat bulunmadığında gecikme oranı hesaplanırken sıfıra bölünme hatası oluştu.
   - *Çözüm:* Aykut Çakıcı formüllere dinamik payda kontrolü ekleyerek PR [#40](https://github.com/MAKU-VBA-GBT-II/group-b/pull/40) (commit `5cea41b`) ile hatayı giderdi.
2. **İptal Kayıtlarının İstatistiksel Sapma ve Payda Bozulması Riski (DQ/BE/FE):**
   - *Problem:* Görev 2 simülasyonunda 49 iptal sevkiyatında teslim süresinin 0 yazılması durumunda ortalama teslim süresi (20,86 saat) aşağı çekilecek ve analiz çarpıtılacaktı.
   - *Çözüm:* Ece Naz Aktürk veri sözlüğünde `durum == 'iptal'` kayıtlarında `teslim_suresi_saat` alanının NaN (boş) bırakılması ve paydadan hariç tutulması kuralını getirdi. Aykut Çakıcı `dogrula()` fonksiyonuyla bunu teyit etti; test senaryosu 9 ile tam doğrulandı.
3. **Takvim Haftası Uyumsuzluğu — ISO W01 Standardı (DQ/FE):**
   - *Problem:* 1 Ocak 2026 Perşembe gününe denk geldiği için yılın ilk takvim haftasının (W01) 4 gün çekmesi (60 sevkiyat), haftalık 105 sevkiyatlık düzenli seride grafik ve rapor arasında tutarsızlık algısı yaratıyordu.
   - *Çözüm:* Analiz ve görselleştirme ekipleri Pazartesi başlangıçlı ISO takvim haftasını ortak standart kabul etti; analiz raporunda ve grafikte W01 kırılımı şeffafça belgelendi.
4. **FE Blokajının Önlenmesi & Dal Senkronizasyonu (FE/BE):**
   - *Problem:* BE simülasyon verisini üretirken FE'nin beklemesi riski doğdu; ayrıca `feature/gorsel` dalına `main` verileri çekilirken ağ bağlantısı kesintisi yaşandı.
   - *Çözüm:* Sema Coşkun şemayı baz alarak önce örnek veriyle grafik iskelet kodunu (`1add6b1`) oluşturdu; veri `main`'e girdikten sonra dalını `main` ile güncelleyip gerçek sayılarla grafikleri dakikalar içinde nihai hale getirdi.
5. **Windows Yerel Ortamında Karakter Kodlama (`UnicodeDecodeError`) (Junior):**
   - *Problem:* Windows terminalinde CP1254 kodlaması nedeniyle Türkçe karakterli test çıktılarında kırılma yaşandı.
   - *Çözüm:* İpek Özarslan test betiklerinde `errors="replace"` ve `utf-8` reconfigure pratiklerini uygulayarak ortam uyumluluğunu sağladı.

---

## 5. Kim Ne Yaptı (Olgusal Üye Katkı Tablosu)

Takım üyelerinin kapatılan Issue [#64](https://github.com/MAKU-VBA-GBT-II/group-b/issues/64) altına bıraktığı resmi yanıtlar doğrultusunda hazırlanan olgusal özet tablosudur:

| Üye ve Rol | 1. Ne Teslim Etti? (Kanıt Linkleri) | 2. Neye Takıldı ve Nasıl Aştı? | 3. Gelecek Dönem Hedefi / Önerisi |
|---|---|---|---|
| **Aykut Çakıcı**<br>*(G1: DQ → G2: BE)* | - G1 veri sözlüğü, analiz betiği ([`src/analiz_g1.py`](https://github.com/MAKU-VBA-GBT-II/group-b/blob/main/src/analiz_g1.py), PR [#37](https://github.com/MAKU-VBA-GBT-II/group-b/pull/37)), 8/8 test log kaydı ([`tests/test-log.md`](https://github.com/MAKU-VBA-GBT-II/group-b/blob/main/tests/test-log.md)), PR [#40](https://github.com/MAKU-VBA-GBT-II/group-b/pull/40) sıfır payda onarımı.<br>- Yan Görev 3: Grup A DQ skill incelemesi ([Grup A #53](https://github.com/MAKU-VBA-GBT-II/group-a/issues/53)).<br>- G2 parametreli simülasyon motoru ([`src/simulasyon.py`](https://github.com/MAKU-VBA-GBT-II/group-b/blob/main/src/simulasyon.py), tohum 42, `dogrula()`), 900 satırlık sevkiyat veri seti ([`data/lojistik_sevkiyat_g2.csv`](https://github.com/MAKU-VBA-GBT-II/group-b/blob/main/data/lojistik_sevkiyat_g2.csv)), `skills/be-simulasyon`, PR [#53](https://github.com/MAKU-VBA-GBT-II/group-b/pull/53) (Issue [#47](https://github.com/MAKU-VBA-GBT-II/group-b/issues/47)). | G1'de gecikme oranı sıfıra bölünme hatasını formüle dinamik koşul ekleyerek çözdü. G2'de iptallerde teslim süresinin NaN kalması ve farklı şehir kuralını `dogrula()` ile kontrol altına aldı. | Görev 3 B2B veri değişimi için partner şirketimiz Grup A'nın veri şemasıyla ortak anahtarları eşleyecek otomatik validatör/dönüştürücü modül (`src/b2b_dogrula.py`) geliştirmek. |
| **Sema Coşkun**<br>*(G1: BE → G2: FE)* | - G1 sentetik veri üretim betiği ([`data/lojistik-sevkiyat.csv`](https://github.com/MAKU-VBA-GBT-II/group-b/blob/main/data/lojistik-sevkiyat.csv), 300 satır, commit `a0e58a2`, Issue [#14](https://github.com/MAKU-VBA-GBT-II/group-b/issues/14)). Hafta 4 düzeltmeleri: #31, #45, #39.<br>- Yan Görev 3: Grup A be-veri skill incelemesi ([Grup A #56](https://github.com/MAKU-VBA-GBT-II/group-a/issues/56)).<br>- G2'de 3 adet analitik grafik (`b650a1a`), `skills/fe-gorsel` (`a253a75`), PR [#56](https://github.com/MAKU-VBA-GBT-II/group-b/pull/56) (Issue [#48](https://github.com/MAKU-VBA-GBT-II/group-b/issues/48)). | `feature/gorsel` dalına `main` verisini çekerken yaşanan senkronizasyon ve ağ kesintisini dal güncelleme ile aştı; sayıları analiz dokümanıyla birebir karşılaştırdı. | Her teslimde commit mesajını ve PR açıklamasını baştan kanıt linkleriyle yazarak dönem sonunda link arama yükünü sıfıra indirmek. |
| **Ece Naz Aktürk**<br>*(G1: FE → G2: DQ)* | - Yan Görev 1 keved raporu (`c505062`, Issue [#41](https://github.com/MAKU-VBA-GBT-II/group-b/issues/41)).<br>- G1 grafik seti ([`src/grafik_uret.py`](https://github.com/MAKU-VBA-GBT-II/group-b/blob/main/src/grafik_uret.py), 2 görsel, `skills/fe-gorsel`, Issue [#16](https://github.com/MAKU-VBA-GBT-II/group-b/issues/16), commit `c41926d`, `5db99ce`).<br>- Yan Görev 3: [Grup A Issue #54](https://github.com/MAKU-VBA-GBT-II/group-a/issues/54).<br>- G2 veri sözlüğü v2.0 & analiz planı (PR [#52](https://github.com/MAKU-VBA-GBT-II/group-b/pull/52)), BE simülasyon PR onayı (PR [#53](https://github.com/MAKU-VBA-GBT-II/group-b/pull/53)), analiz raporu & gereksinim dokümanı ([`src/analiz_g2.py`](https://github.com/MAKU-VBA-GBT-II/group-b/blob/main/src/analiz_g2.py), [`docs/analiz-g2.md`](https://github.com/MAKU-VBA-GBT-II/group-b/blob/main/docs/analiz-g2.md), PR [#54](https://github.com/MAKU-VBA-GBT-II/group-b/pull/54)), 10 senaryolu otomatik test hattı ([`src/test_calistir.py`](https://github.com/MAKU-VBA-GBT-II/group-b/blob/main/src/test_calistir.py), [`tests/test-log.md`](https://github.com/MAKU-VBA-GBT-II/group-b/blob/main/tests/test-log.md), PR [#55](https://github.com/MAKU-VBA-GBT-II/group-b/pull/55)) ve FE nihai grafik onayı (PR [#56](https://github.com/MAKU-VBA-GBT-II/group-b/pull/56)). | G1'de planlanan 6 ay yerine verinin 3 ay çıkmasını başlığı güncelleyerek aştı. G2'de iptal kayıtlarında teslim süresi payda sapmasını NaN kuralı ve Senaryo 9 ile çözdü; W01 haftası için ISO standardı uyguladı. | Veri kalite testlerini GitHub Actions CI/CD hattına entegre ederek her PR açılışında otomatik koşulmasını sağlamak ve `docs/user-manual.md` kılavuzunu hazırlamak. |
| **İpek Özarslan**<br>*(Junior)* | - Isınma & Keşif: `prova-ipek.csv`, `src/prova_ipek.py`, Yan Görev 1 keşif raporu (`c1a9f88`).<br>- G1 test koşumu doğrulaması ve `tests/test-log.md` 2. koşum kaydı (`e42c3f8`).<br>- G2 ön test ve bağımsız doğrulama: `src/simulasyon.py` betiğini 8 farklı parametre kombinasyonuyla bağımsız test ederek hash eşleşmesi ve gözlem raporu teslimi (Issue [#51](https://github.com/MAKU-VBA-GBT-II/group-b/issues/51)).<br>- Yan Görev 3: Grup A reposunda çapraz inceleme ([Grup A #53](https://github.com/MAKU-VBA-GBT-II/group-a/issues/53)). | Windows terminalinde Türkçe karakterlerin yarattığı `UnicodeDecodeError` hatasını `errors="replace"` ve UTF-8 reconfigure ile aştı. `dogrula()` içindeki en az 100 satır şartını sınır testlerinde belgeledi. | `docs/user-manual.md` kullanıcı kurulum ve çalıştırma kılavuzunun yazımını üstlenmek; yeni başlayan geliştiriciler için uçtan uca kurulum senaryolarını test edip belgelemek. |
| **Sude Çukurtaş**<br>*(PM)* | - Hafta 1-5 sprint planlaması, koordinasyon ve pano yönetimi.<br>- `reports/report-w03.md`, `reports/report-w04.md` (`ec74266`), `reports/report-w05.md` (`127e58c`, `b50cf2a`).<br>- `gorev1-final` release'i ve sürüm notları yayını.<br>- PR devir teslim zincirinin denetlenmesi, `AGENTS.md` ve `skills/pm-rapor` güncelliği.<br>- Duyuru 7 kapsamındaki 51 Issue'nun eksiksiz neticelendirilmesi ve Dönem Raporu 1 veri toplama koordinasyonu ([Issue #64](https://github.com/MAKU-VBA-GBT-II/group-b/issues/64)). | Rol rotasyonunda görev yetki karmaşası riskini `AGENTS.md` devir teslim zincirini ve rol onay zorunluluğunu işleterek önledi. 5 Kasım temizliğinde tüm takımdan kanıtlı verileri Issue #64 ile toplayarak sıfır açık iş hedefini sağladı. | Partner şirketimiz Grup A ile Görev 3 veri değişimi için API ve sözleşme protokolünü koordine etmek, ortak veri takvimini yönetmek ve takımın teslim disiplinini korumak. |

---

## 6. Dersler (Retrospektif)

Dönemin ilk yarısında edinilen ve sonraki görevlerde uygulanacak 3 temel kurumsal ders:

1. **Sözleşme-Öncelikli (Contract-First) Geliştirmenin Gücü:** Görev 2 başında veri sözlüğünün (`docs/veri-sozlugu.md` v2.0) tüm parametre, tip ve sınır değerleriyle eksiksiz tanımlanması; Backend (veri simülasyonu) ve Frontend (grafik taslağı) ekiplerinin birbirini beklemeden paralel çalışmasını sağlamış, devir teslim süresini yarıya indirmiştir.
2. **Otomatik Test Hattı ve Erken Hata Yakalama:** Manuel testler yerine `src/test_calistir.py` motoru ile 10 senaryonun tek komutla koşulabilmesi; iptal kayıtlarında teslim süresinin NaN bırakılması gibi kritik mantıksal hataların PR aşamasında (main'e girmeden) yakalanmasını sağlamıştır.
3. **Kanıt Odaklı PR ve İletişim Disiplini:** Issue ve PR'ların içerisine commit hash'i, dosya yolu ve doğrulama ekran çıktılarının baştan eklenmesi; dönem raporu derlenirken hiçbir verinin kaybolmamasını ve takım içi güven ortamını güçlendirmiştir.

---

## 7. Görev 3 Hazırlığı (B2B Veri Değişimi Planı)

Duyuru 5'te ilan edilen eşleşme tablosuna göre **Şirket B (Lojistik)** olarak partnerimiz **Şirket A (Tedarikçi / Bilişim Entegrasyonu)** şirketidir. Görev 3 kapsamındaki veri alışverişi için hazırlık planımız şu şekildedir:

1. **Veri Değişimi Kapsamı:** Şirket B lojistik sevkiyat verilerini (`lojistik_sevkiyat_g2.csv`) Şirket A'ya sağlarken; Şirket A'dan sipariş, tedarikçi ve depo stok kayıtlarını alarak sevkiyat hareketleriyle konsolide edecektir.
2. **Ortak Anahtar ve Şema Mutabakatı:** İki şirketin veri modellerini birleştirmek üzere `siparis_id` ve `tedarikci_id` alanları ortak anahtar (foreign key) olarak belirlenecektir. BE sorumlumuz Aykut Çakıcı, partner şemasını karşılayan `src/b2b_dogrula.py` doğrulama modülünü geliştirecektir.
3. **Skill ve Dokümantasyon:** Yan Görev 3 kapsamında Şirket A'nın repolarında açtığımız inceleme Issue'ları ([Grup A #53](https://github.com/MAKU-VBA-GBT-II/group-a/issues/53), [#54](https://github.com/MAKU-VBA-GBT-II/group-a/issues/54), [#56](https://github.com/MAKU-VBA-GBT-II/group-a/issues/56)) temel alınarak B2B veri sözlüğü ortak bir PR ile iki takımın depolarına eşzamanlı işlenecektir.

---

## 8. Prompt ve Model Özeti

Bu dönem raporu, Grup B'nin `skills/pm-rapor/SKILL.md` kuralları doğrultusunda **Antigravity (Google DeepMind)** ortamında çalışan **Gemini 3.8 Flash** modeli kullanılarak hazırlanmıştır. Raporun tüm verileri kapatılan GitHub Issue [#64](https://github.com/MAKU-VBA-GBT-II/group-b/issues/64), commit geçmişi (`git shortlog`), GitHub PR API'si ve depodaki gerçek teslimat dosyaları taranarak olgusal olarak derlenmiştir.

---
*Raporu Hazırlayan ve Onaylayan:*  
**Sude Çukurtaş** — Proje Yöneticisi (PM), Grup B (LIN)  
*İmza Tarihi:* 07.11.2026
