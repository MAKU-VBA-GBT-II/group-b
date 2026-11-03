---
name: fe-gorsel
description: Grup B'nin Görev 2 lojistik sevkiyat verisinden (data/lojistik_sevkiyat_g2.csv) 3 grafik üretir: haftalık zaman serisi, taşıma modu kırılımı ve teslimat süresi histogramı. Görev 2 grafikleri veya bu grafiklerin yeniden üretilmesi istendiğinde kullan.
---

# fe-gorsel — Lojistik grafik üretimi (Görev 2)

## Amaç
Görev 2 veri dosyasından (`data/lojistik_sevkiyat_g2.csv`) yönetim ve DQ tarafından okunabilir 3 PNG grafik üretmek. Grafikler yalnızca veri dosyasındaki değerlerden çizilir; hiçbir değer uydurulmaz.

## Girdiler
- Veri: `data/lojistik_sevkiyat_g2.csv` (900 satır, şema `docs/veri-sozlugu.md` v2.0). Gerekli sütunlar: `tarih`, `tasima_modu`, `durum`, `teslim_suresi_saat`, `ucret_tl`.
- Kod: `src/gorsel_g2.py`
- Doğrulama: `docs/analiz-g2.md` (DQ analiz raporu, Issue #49)

## Çıktılar
1. `visuals/zaman_serisi_haftalik.png`: İki panel. Üstte haftalık sevkiyat sayısı (adet), altta haftalık navlun geliri (TL). X ekseni ISO haftası.
2. `visuals/mod_gecikme_kirilimi.png`: İki çubuk grafik. Solda sevkiyat sayısı (adet, iptaller dahil), sağda gecikme oranı (%, iptaller hariç).
3. `visuals/teslimat_suresi_dagilimi.png`: Histogram. İptal dışı sevkiyatların teslim süresi (saat), ortalama çizgisiyle.

## Kararlar (DQ onayı, Issue #48)
- **Hafta:** Pazartesi başlangıçlı ISO haftası (`YYYY-Www`). Eksik hafta ayrı blok yapılmaz. 4 günlük 2026-W01 yıldızla işaretlenir ve altına not yazılır.
- **Sevkiyat sayısı ve ciro:** İptaller dahil.
- **Gecikme oranı:** `gecikmeli / (zamaninda + gecikmeli) * 100`. İptaller paydada yok.
- **Teslim süresi:** Yalnızca `durum != iptal`. `teslim_suresi_saat` boş olan satır çizilmez.

## Görsel kurallar
- Her grafikte başlık, eksen etiketi ve birim olmalı (adet, TL, %, saat).
- Türkçe karakterler (ş, ğ, ı, İ) doğru görünmeli. Para tutarları binlik ayraçla yazılmalı (ör. 3.351.304,20).
- Kaydetme: 150 dpi PNG, `tight_layout`.
- Renkler: mavi `#378ADD` (adet, ciro, histogram), turuncu `#EF9F27` (oran, ortalama çizgisi).
- Veri dosyası yoksa grafiklere "ÖRNEK VERİ" damgası konur. Gerçek veriyle üretilen grafikte bu damga olmaz.

## Adımlar
1. Veri dosyasının varlığını kontrol et. Yoksa BE'nin veri commit'ini `main`'e merge etmesini bekle ve Issue'ya yaz. Uydurma veriyle yeniden üretme.
2. `python src/gorsel_g2.py` çalıştır.
3. Terminalde "gerçek veri, 900 satır" yazmalı. "ÖRNEK veri" yazıyorsa dur ve veri dosyasını kontrol et.
4. Terminaldeki sayıları `docs/analiz-g2.md` ile karşılaştır: toplam sevkiyat, toplam ciro, mod bazlı gecikme oranları, ortalama teslim süresi, haftalık değerler. Fark varsa grafikleri yayınlama, DQ'ya sor.
5. PNG'leri aç. "ÖRNEK VERİ" yazısı olmamalı, yazılar çerçeveye taşmamalı.
6. Commit mesajı: `FE: <ne değişti> (#48)`. `Fixes` kullanma; Issue PR merge edilince kapanır.

## Kontrol listesi (commit öncesi)
- [ ] Terminalde "gerçek veri" yazıyor
- [ ] Toplam 900 sevkiyat, haftalık toplamlar 900 ediyor
- [ ] Mod sayıları 900 ediyor (iptaller dahil)
- [ ] Gecikme oranları `analiz-g2.md` ile aynı
- [ ] Teslim süresi ortalaması `analiz-g2.md` ile aynı (yuvarlama farkı tolere edilir)
- [ ] 3 PNG üretildi; başlık, eksen etiketi ve birim var
- [ ] Hiçbir PNG'de "ÖRNEK VERİ" yazmıyor

## Örnek giriş ve çıkış
**Giriş (prompt):** "fe-gorsel skill'ini kullanarak Görev 2 grafiklerini gerçek veriyle yeniden üret."

**Çıkış (özet):**
```
3 grafik yazıldı (gerçek veri, 900 satır): visuals/
Grafik 1: 2026-W01 4 gün (60 sevkiyat), W02–W09 7 gün (105'er sevkiyat)
Grafik 2: kara %17,5 · demiryolu %17,3 · hava %12,6 · deniz %10,7
Grafik 3: 851 başarılı sevkiyat, ortalama 20,9 saat
```
Ardından `analiz-g2.md` ile karşılaştırma sonucu yazılır ve commit önerilir.

## Reddetme durumları
- **Gerçek kişisel veri talebi** (ad-soyad, telefon, adres, TC kimlik no, gerçek müşteri kaydı): Grafik üretmez, veri eklemez. Nedenini kısaca söyler, sentetik bir karşılık önerir (ör. `musteri_id` gibi sentetik kimlik).
- **Sayı uydurma veya veriyi değiştirme** (ör. "ciroyu biraz yükselt", "eksik haftayı doldur"): Reddeder. Eksik hafta gösterilir.
- **"ÖRNEK VERİ" damgasını gerçek veriymiş gibi gizleme** talebi: Reddeder.
- **Şemayı tek taraflı değiştirme** (kolon ekleme, aralık değiştirme): DQ'ya sorulmadan yapılmaz. Önce `docs/veri-sozlugu.md` güncellenir.

## Üretim kaydı
Bu skill ve `src/gorsel_g2.py`, Claude (Anthropic) yardımıyla hazırlanmıştır. Bu skill ile yapılan her teslimin PR açıklamasına şu satır eklenir:
`Üretim: skill'i ile, Claude — prompt özeti: <kısa özet>`

## Kullanılan dosyalar
- **Okur:** `data/lojistik_sevkiyat_g2.csv`, `docs/veri-sozlugu.md`, `docs/analiz-g2.md`
- **Çalıştırır:** `src/gorsel_g2.py`
- **Yazar:** `visuals/zaman_serisi_haftalik.png`, `visuals/mod_gecikme_kirilimi.png`, `visuals/teslimat_suresi_dagilimi.png`

## Bağımlılıklar
`pip install matplotlib pandas numpy`

## Nasıl çalıştırılır
- Ajana: "fe-gorsel skill'ini kullanarak Görev 2 grafiklerini gerçek veriyle yeniden üret."
- Elle: `python src/gorsel_g2.py`