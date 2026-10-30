---
name: dq-sozluk
description: Görev 2 mini ürünü için lojistik sevkiyat veri şemasını, simülasyon parametrelerini ve analiz planını tanımlar.
---

# dq-sozluk — Lojistik Sevkiyat Veri Şeması ve Analiz Planı Tasarımı

## Amaç
Bu skill, Görev 2 kapsamındaki parametreli sentetik lojistik sevkiyat simülasyonu için alan kurallarını, veri tiplerini, parametreleri ve analiz/görselleştirme metriklerini tanımlayan standart `docs/veri-sozlugu.md` belgesini tasarlar ve doğrular.

## Girdiler
- Proje gereksinimleri ve ilgili GitHub Issue (#46 `G2-sem`).
- BE parametreli simülasyon gereksinimleri (#47 `G2-veri`).
- FE 3 grafik seti gereksinimleri (#48 `G2-gorsel`).
- Sabit tohum ve sentetik veri kuralları (AGENTS.md).

## Çıktı Formatı Kuralları
1. **Şema Tablosu:** Her alan için `Alan Adı`, `Veri Tipi`, `Zorunlu/Boşluk Durumu`, `Geçerli Aralık / Kural` ve `Örnek Değer` sütunlarını içeren Markdown formatında tablo olmalıdır.
2. **Parametre Listesi:** Simülasyon betiğinin alacağı en az iki parametre (örn: `tohum`, `gun_sayisi`, `gunluk_sevkiyat`, `gecikme_olasiligi`), tipleri ve varsayılan değerleri açıkça listelenmelidir.
3. **Analiz Metrikleri:** En az 5 metrik tanımlanmalıdır:
   - 1 Toplam metrik (toplam sevkiyat, toplam ciro)
   - 1 Ortalama metrik (ortalama teslim süresi; iptaller hariç)
   - 2 Kırılım metriği (biri zaman serisi: haftalık hacim/gelir, biri kategorik: mod bazlı gecikme oranı)
   - 1 Top-N metrik (en yoğun 5 rota)
4. **FE Uyum Bölümü:** FE'nin hazırlayacağı 3 grafik (zaman serisi, kategorik kırılım, dağılım histogramı) ile şema alanları arasındaki ilişki netleştirilmelidir.

## Örnek Girdi ve Çıktı

### Örnek Girdi:
> "Görev 2 için 60 günlük, mod bazlı gecikme olasılığı içeren ve FE'nin haftalık grafik çıkarabileceği bir sevkiyat şeması hazırla."

### Örnek Çıktı Parçası:
```markdown
| Alan Adı | Veri Tipi | Kural / Aralık | Örnek |
|---|---|---|---|
| sevkiyat_id | Metin | SVK-G2-0001 ... SVK-G2-XXXX, benzersiz | SVK-G2-0001 |
| teslim_suresi_saat | Ondalık | Pozitif float, 1 basamak; durum='iptal' ise boş | 14.5 |

**Parametreler:**
- `--gun-sayisi`: 60 (varsayılan)
- `--tohum`: 42 (varsayılan)
```

## Reddetme Durumları
Aşağıdaki talepler veya durumlar bu skill tarafından kesin olarak REDDEDİLİR:
1. **Gerçek Kişisel Veri / Şirket Verisi:** Gerçek şahıs isimleri, TC kimlik no, gerçek adres, telefon veya gerçek şirket finansal verisi içeren alan talepleri KVKK ve veri güvenliği kuralları gereği doğrudan reddedilir; yalnızca sentetik ve anonim alanlar kullanılır.
2. **Parametresiz / Sabit Kodlanmış Üretim:** Simülasyon parametresi tanımlanmayan veya tohumu bulunmayan şema tasarımları reddedilir.
3. **Tutarsız İptal Mantığı:** İptal edilen sevkiyatlarda teslim süresi hesaplanmasını öngören veya paydasında iptalleri gecikme oranına katan tasarımlar reddedilir (iptal edilen sevkiyatın teslim süresi olamaz).
