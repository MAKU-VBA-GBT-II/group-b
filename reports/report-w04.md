# Sprint Raporu — Hafta 04 (22.10–27.10.2026)

**Şirket:** Grup B — Logistics Intelligence Network (LIN) / Sevkiyatlar · **PM:** Sude Çukurtaş  
**Tarih:** 27.10.2026  
**Görev:** Görev 1 Kapanışı (Hafta 4: Test, Düzeltme, Sürüm) + Yan Görev 3: Çapraz Skill İncelemesi  

---

## Planlanan

| Issue | Başlık | Atanan | Son tarih | Kabul kriteri |
|---|---|---|---|---|
| #24 | [DQ] Hafta 4: Test Koşumu, Hata Tespiti ve Veri Doğrulama | @Aykuutt (DQ) | 27.10.2026 23:59 | `tests/test-cases.md` senaryolarının gerçek veri üzerinde koşulup `tests/test-log.md`'ye işlenmesi; en az 2 bug/enhancement kaydı açılması |
| #25 | [BE] Hafta 4: Hata Düzeltmeleri ve Nihai Veri Hattı Kapanışı | @sema788 (BE) | 27.10.2026 23:59 | Tespit edilen hataların/iyileştirmelerin `Fixes #no` commit mesajıyla düzeltilmesi |
| #26 | [FE] Hafta 4: Görselleştirme Düzeltmeleri ve Çıktı Güncelleme | @ece-naz (FE) | 27.10.2026 23:59 | Grafik hatalarının ve skill eksiklerinin giderilmesi, nihai çıktıların güncellenmesi |
| #27 | [Junior] Hafta 4: Test Senaryosu Koşma ve Hata Doğrulama | @ipek0-0 (Junior) | 27.10.2026 23:59 | Test senaryolarının koşumuna ve hata doğrulama adımlarına katılım |
| #28 | [Tüm Ekip] Yan Görev 3: Grup A Çapraz Skill İncelemesi | @sudecukurtas, @Aykuutt, @sema788, @ece-naz, @ipek0-0 | 27.10.2026 23:59 | Partner şirket olan Grup A'nın reposunda her rolün kendi skill'ini inceleyip enhancement Issue'su açması |

---

## Yapılan

| Issue | Kanıt (commit / dosya / link) | Durum |
|---|---|---|
| #24 | `tests/test-log.md` (1. ve 2. koşum; 8/8 senaryo geçti), `src/test_calistir.py` (commit `e42c3f8`), Issue #38 & #39 açıldı | ✅ Kapandı |
| #25 | `src/uret_sevkiyat.py` şema doğrulayıcı `dogrula()` (commit `b488b95` - `Fixes #39`), `ucret_tl` 2 ondalık yuvarlama (commit `57f2187`) | ✅ Kapandı |
| #26 | `skills/fe-gorsel/SKILL.md` bağımlılık ve ön kontrol güncellemeleri (commit `5db99ce` - `#44`), grafik taslak standardı (Issue #33) | ✅ Kapandı |
| #27 | Junior üye Hafta 4 test doğrulama ve inceleme sürecine katıldı | ✅ Kapandı |
| #28 | Grup A reposunda 5 rol inceleme Issue'su açıldı (Grup A #39, #53, #54, #56, #58) | ✅ Kapandı |
| G-İnceleme | Grup G'den gelen inceleme Issue'ları (#29, #34, #36, #44, #45) yanıtlandı ve düzeltme commit'leriyle kapatıldı | ✅ Kapandı |
| PM | `AGENTS.md` ve `skills/pm-rapor/SKILL.md` güncellemeleri (`7a56fea`, `6a77516`), `reports/report-w04.md` | ✅ Tamamlandı |

**Test ve Kalite Özeti:**  
`tests/test-log.md`'ye göre 8 senaryonun 8'i de başarıyla geçmiştir (0 hata, 0 ihlal). 300 satırlık nihai sentetik lojistik sevkiyat verisi (`data/lojistik-sevkiyat.csv`), veri sözlüğü v1.1 ve v1.2 kurallarına tam uyumludur. Veri hatası bulunmadığından Duyuru 5 doğrultusunda 2 somut iyileştirme önerisi (#38 ve #39) açılarak başarıyla uygulanmıştır.

---

## Devir Teslim Zinciri

- **DQ → BE (Kalite ve Geliştirme):** Test senaryolarında veri hatası çıkmadı; ancak hattı daha sağlam kılmak adına CSV yazılmadan önce tam sözlük doğrulamasını zorunlu kılan iyileştirme Issue'su açıldı (#39). BE Sema Coşkun `src/uret_sevkiyat.py` içine `dogrula()` fonksiyonunu entegre ederek commit `b488b95` ile kapattı.
- **DQ → Test Otomasyonu:** DQ Aykut Çakıcı, manuel test adımlarını otomatik olarak çalıştıran `src/test_calistir.py` betiğini yazdı ve 27.10.2026 tarihli 2. test koşumunu otomatikleştirerek depoya kazandırdı (commit `e42c3f8`).
- **Grup G → Ekip (Geri Bildirim Döngüsü):** Grup G'den gelen çapraz incelemeler (PM için #29 & #34, DQ için #36, FE için #44, BE için #45) ilgili rol sahipleri tarafından değerlendirildi; skill'ler ve betikler somut commit'lerle zenginleştirildi.
- **Ekip → Grup A (Çapraz İnceleme Teslimi):** Tüm ekip partner şirket Grup A reposunda kendi rolüne ait skill'leri derinlemesine inceleyerek 1 güçlü yan, 1 eksik ve 1 somut öneri içeren Issue'larını açtı.
- **PM → Sürüm Kapanışı:** Tüm görevlerin kanıt yorumlarıyla kapandığı teyit edildi, sprint raporu (`report-w04.md`) mühürlendi ve `gorev1-final` sürümü için hat kapatıldı.

---

## Tıkanan / Yönetilen Riskler

1. **Sıfır Hata Durumunda Duyuru 5 Prosedürü:** Test koşumunda veride kritik hata çıkmaması üzerine, Duyuru 5 kuralı işletilerek boş geçilmedi; veri üretim hattına ön doğrulama (`dogrula()`) ve otomatik test koşucu (`test_calistir.py`) olmak üzere 2 somut enhancement açılarak hat güçlendirildi.
2. **Çapraz İnceleme Eşleşmesi ve İletişim:** Yan Görev 3 kapsamında eşleştiğimiz Grup A'ya incelemeler eksiksiz iletildi; aynı zamanda repomuza Grup G'den gelen tüm geri bildirimler 24 saat içinde yanıtlanarak aksiyon alındı.
3. **Pano / Issue Senkronizasyonu:** PM rapor skill'ine (#34 kapsamında) proje panosuna doğrudan erişilememesi durumunda doğrudan GitHub Issue ve `git log` kayıtlarının esas alınacağı açık talimatı eklenerek süreç riski ortadan kaldırıldı.

---

## Kim Ne Yaptı

| Üye | Rol | Başlıca Commit'ler / Katkı | Kapattığı Issue |
|---|---|---|---|
| Sude Çukurtaş | PM | Sprint koordinasyonu (#24-#28), `AGENTS.md` ve `pm-rapor` revizyonları (`Fixes #29`, `Fixes #34`), Grup A PM incelemesi (Grup A #39), `report-w04.md`, `gorev1-final` release hazırlığı | #28, #29, #30, #34 |
| Sema Coşkun | BE | `src/uret_sevkiyat.py` şema doğrulayıcı `dogrula()` (`b488b95` - `Fixes #39`), `ucret_tl` ve float hassasiyet revizyonu (`57f2187`), `be-veri` skill onarımı (`1fd917a` - `Fixes #31`), Grup A BE incelemesi (Grup A #56) | #25, #31, #39, #45 |
| Aykut Çakıcı | DQ | `tests/test-log.md` 1. ve 2. test koşumu, `src/test_calistir.py` otomatik test betiği (`e42c3f8`), `src/analiz_g1.py` analizi (`71f5d34` - `Fixes #32`), Grup A DQ incelemesi (Grup A #53) | #24, #32, #36, #38 |
| Ece Naz Aktürk | FE | `skills/fe-gorsel/SKILL.md` bağımlılık ve dosya kontrol adımı eklenmesi (`5db99ce`), grafik taslak standardı (#33), Grup A FE incelemesi (Grup A #54) | #26, #33, #44 |
| İpek Özarslan | Junior | Hafta 4 doğrulama kartı, `test-log.md` ve test senaryosu kontrolleri, Grup A incelemesi (Grup A #58) | #27 |

---

## Gelecek Hafta (Görev 2)

- Görev 1 final sürümü (`gorev1-final`) ile veri üretim ve kalite hattı resmen kapatılmıştır.
- Görev 2 kapsamında B2B veri değişimi, format dönüşümleri ve partner şirketimiz (Grup A) ile veri entegrasyonu çalışmalarına başlanacaktır.

---

*Bu rapor `pm-rapor` skill'i kullanılarak Antigravity / Gemini 3.8 Flash modeli ile depodaki gerçek izler (Issue'lar, commit'ler ve test logları) doğrulanarak üretilmiştir.*
