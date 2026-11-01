---
name: dq-test
description: Görev 2 lojistik sevkiyat verisi için 10 veri kalite test senaryosunu tanımlar, src/test_calistir.py ile otomatik çalıştırır ve test-log.md'ye kaydeder.
---

# DQ Test Skill'i — G2-TEST

## Amaç
Bu skill, Görev 2 kapsamında üretilen `data/lojistik_sevkiyat_g2.csv` dosyasının ve `src/simulasyon.py` betiğinin `docs/veri-sozlugu.md` (v2.0) kurallarına tam uyumunu denetleyen 10 test senaryosunu (`tests/test-cases.md`) yönetir, testleri otomatik koşarak sonuçları `tests/test-log.md` dosyasına işler.

## Girdiler
1. GitHub Issue #50 `G2-test` kabul kriterleri.
2. Nihai veri kümesi: `data/lojistik_sevkiyat_g2.csv` (commit [`869dd1b`](https://github.com/MAKU-VBA-GBT-II/group-b/commit/869dd1b)).
3. Referans Veri Sözlüğü: `docs/veri-sozlugu.md` (v2.0).
4. Simülasyon betiği: `src/simulasyon.py`.

## İş Akışı ve Adımlar
1. Eski Görev 1 test senaryolarını `tests/test-cases-g1.md` dosyasına arşivle.
2. `tests/test-cases.md` dosyasına 10 ana senaryoyu tanımla (dosya varlığı, 900 satır, 10 sütun, benzersiz ID, 60 günlük periyot, 8 merkez & rota, 4 mod, sayısal aralıklar, iptalde boş süre kuralı, tohum=42 tekrarlanabilirlik).
3. `src/test_calistir.py` test koşucu betiğini çalıştır:
   ```bash
   python src/test_calistir.py
   ```
4. Koşum sonuçlarını (tüm testlerin geçtiğini) `tests/test-log.md` dosyasına tarihli olarak kaydet.
5. `feature/test-g2` dalından PR aç, merge et ve Issue #50'yi kapat.

## Örnek Girdi ve Çıktı
### Girdi:
> "Görev 2 nihai verisini test senaryolarına göre çalıştır ve günlüğe kaydet."
### Çıktı Parçası:
```markdown
No   Senaryo Adı                                   Durum      Açıklama
1    Dosya Varlığı ve UTF-8 Okuma                  GEÇTİ      UTF-8 okundu; 900 veri satırı mevcut
9    Durum Kategorileri ve İptalde Teslim Süresi   GEÇTİ      49 iptal kaydında teslim süresi tam boş
SONUÇ: 10/10 TEST BAŞARIYLA GEÇTİ.
```

## Reddetme Durumları
1. **İptal Kayıtlarında Süre Kabulü:** İptal durumundaki satırlarda teslim süresi içeren veya bu kuralı esneten test talepleri doğrudan reddedilir.
2. **Gerçek Kişi / Firma Verisi:** Sentetik olmayan veya kişisel veri içeren alan testleri reddedilir.
3. **Manuel Sonuç Uydurma:** Testleri çalıştırmadan başarı varsayımı yapmak reddedilir; testler `src/test_calistir.py` ile fiilen doğrulanmalıdır.
