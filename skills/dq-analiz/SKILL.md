---
name: dq-analiz
description: Görev 2 parametreli lojistik sevkiyat verisini veri sözlüğüne göre analiz eder, 5 metrik, 3 somut gözlem ve 1 eylem önerisi çıkarır.
---

# DQ Analiz Skill'i — G2-ANALİZ

## Amaç
Bu skill, Görev 2 kapsamında üretilen `data/lojistik_sevkiyat_g2.csv` dosyasını `docs/veri-sozlugu.md` (v2.0) kurallarına göre analiz ederek 5 temel analitik metriği hesaplar, elde edilen bulguları (3 gözlem + 1 eylem önerisi) `docs/analiz-g2.md` dosyasında raporlar ve görselleştirme için FE'ye devir notu hazırlar.

## Girdiler
1. GitHub Issue #49 `G2-analiz` kabul kriterleri.
2. BE veri teslim ve merge commit'i ([`869dd1b`](https://github.com/MAKU-VBA-GBT-II/group-b/commit/869dd1b)).
3. Veri Sözlüğü: `docs/veri-sozlugu.md` (v2.0).
4. Nihai Veri Kümesi: `data/lojistik_sevkiyat_g2.csv` (900 satır).
5. Görselleştirme gereksinimleri için GitHub Issue #48 `G2-gorsel`.

## İş Akışı ve Adımlar
1. Veri dosyasını (`data/lojistik_sevkiyat_g2.csv`) ve kullanılan merge commit hash'ini doğrula.
2. Depo kökünden analiz betiğini çalıştır: `python src/analiz_g2.py`
3. Betiğin hesapladığı metrikleri (toplam hacim/ciro, ortalama süre, ISO haftalık zaman serisi, mod bazlı gecikme oranları, top-5 rota) `docs/analiz-g2.md` raporuna aktar.
4. Her bir temel metriğin yanına 1–2 cümlelik, veriye dayalı analitik yorum ekle.
5. Veri kümesinden türetilen en az 3 somut operasyonel gözlem ve bunlara dayalı 1 uygulanabilir eylem önerisi yaz.
6. FE (Sema - Issue #48) için doğrulanmış grafik metriklerini içeren devir teslim bölümünü rapora ekle.
7. `feature/analiz-g2` dalından PR aç, merge et ve Issue #48'e devir yorumu bırak.

## 5 Metrik Tanımı ve Hesaplama Kuralları
- **Toplam Hacim ve Ciro (Metrik 1):** Tüm 900 satırın toplamı. İptal edilen kayıtların navlun ücretleri de operasyonel hacme dahildir.
- **Net Ortalama Teslim Süresi (Metrik 2):** `durum == 'iptal'` kayıtları **kesinlikle dışarıda bırakılır**; yalnızca tamamlanan (zamanında ve gecikmeli) kayıtların `teslim_suresi_saat` ortalaması alınır.
- **Haftalık Zaman Serisi (Metrik 3):** Pazartesi başlangıçlı ISO haftası (`YYYY-Www`) standardı kullanılır. 1–4 Ocak (W01) doğal takvim haftası olarak ayrı bir blok yapılmadan gösterilir.
- **Taşıma Modu Gecikme Oranı (Metrik 4):** `(Gecikmeli / (Zamanında + Gecikmeli)) * 100` formülü uygulanır; paydada iptaller yer almaz.
- **Top-5 Rota (Metrik 5):** `cikis_sehri -> varis_sehri` çiftine göre sevkiyat adedi azalan sırada ilk 5 rota listelenir.

## Çalıştırma
```bash
python src/analiz_g2.py
```
*(Farklı bir dosya için: `python src/analiz_g2.py --csv-yolu data/ozel_veri.csv`)*

## Örnek Girdi ve Çıktı
### Girdi:
> "Görev 2 nihai verisi üzerinde metrikleri hesapla ve FE devir notlarıyla raporla."
### Çıktı Parçası:
```markdown
- Toplam Ciro: 3.351.304,20 TL
- Ortalama Süre (İptaller Hariç): 20,86 saat
- Kara Yolu Gecikme Oranı: %17,5 (74 gecikmeli / 423 tamamlanan)
```

## Reddetme Durumları
1. **İptal Kayıtlarının Süre Ortalamasına Katılması:** İptal edilen sevkiyatlarda fiili teslim süresi oluşmadığından, bu kayıtları süre ortalamasına veya gecikme paydasına katan analiz talepleri doğrudan reddedilir.
2. **Gerçek Kişi / Firma Verisi:** Sentetik olmayan veya kişisel veri içeren analiz talepleri reddedilir.
3. **Uydurma Veri ve Nedensellik:** CSV verisinde bulunmayan varsayımsal sayılar veya sentetik veriden mutlak gerçek dünya nedenselliği çıkarma talepleri reddedilir.
