# AGENTS.md GRUP-B Logistics Intelligence Network(LIN) SKİLL Envanteri

Bu repo, Şirket B (Lojistik) için parametreli sentetik sevkiyat veri hattı içerir.
Ajan, görev aldığında ilgili `SKILL.md` dosyasını okuyup talimatları izlemelidir.

| Skill | Konum | Sahibi | Ne işe yarar | Nasıl kullanılır |
|---|---|---|---|---|
| dq-sozluk | `skills/dq-sozluk/SKILL.md` | DQ — Ece Naz Aktürk | G2 veri şeması, parametreleri ve analiz planını tanımlar | Görev #46 için bu skill'i oku; `docs/veri-sozlugu.md` hazırla |
| be-simulasyon | `skills/be-simulasyon/SKILL.md` | BE — Aykut Çakıcı | Parametreli lojistik sevkiyat simülasyon verisi üretir | `python src/simulasyon.py` |
| fe-gorsel | `skills/fe-gorsel/SKILL.md` | FE — Sema Coşkun | G2 simülasyon verisinden 3 grafik üretir (zaman serisi, kırılım, dağılım) | `python src/grafik_uret.py` (taslak Issue'ya eklendikten sonra) |
| dq-analiz | `skills/dq-analiz/SKILL.md` | DQ — Ece Naz Aktürk | Sevkiyat verisinden 5 metrik, gözlem ve eylem önerisi çıkarır | Görev #49 için bu skill'i oku; `docs/analiz-g2.md` hazırla |
| dq-test | `skills/dq-test/SKILL.md` | DQ — Ece Naz Aktürk | G2 test senaryolarını tanımlar ve PR doğrulamasını yürütür | Görev #50 için bu skill'i oku; `tests/test-cases.md` hazırla |
| pm-rapor | `skills/pm-rapor/SKILL.md` | PM — Sude Çukurtaş | Haftalık raporu commit/Issue geçmişinden hazırlar | Ajana: "pm-rapor skill'ini oku" |

## Devir teslim zinciri (Görev 2)
DQ şema/sözlük → BE veri simülasyonu (ve paralel FE taslak) → DQ BE PR inceleme/onay → DQ analiz & FE nihai görseller → DQ test & PM rapor.
Her adım ilgili Issue'ya commit hash'li yorumla biter.
> Kural: Roller görevden göreve döner (plan §1.3); skill'ler rolle birlikte el değiştirir. Yeni sahibi skill'i günceller ve bu tablodaki "Sahibi" sütununu değiştirir.

## Kurallar
- Veri sentetiktir; gerçek kişi veya firma verisi asla depoya girmez.
- Veri üretimi sabit tohumla tekrarlanabilir olmalıdır.
- Yeni skill eklendikçe bu dosya güncellenir.
- "GitHub'da yoksa, yapılmamıştır": her iş bir Issue'ya bağlıdır; bitince Issue'ya kanıt yorumu (commit hash + dosya) yazılır.
- Gerçek kişi verisi asla depoya girmez; tüm veriler simülasyon ürünüdür.
- Veri üretimi sabit tohumla tekrarlanabilir olmalıdır.
- Hafta 5'ten itibaren `main`'e yalnızca PR ile girilir; kod/veri PR'ları DQ onayı olmadan merge edilmez.
