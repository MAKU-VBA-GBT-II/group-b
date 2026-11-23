# Veri Sözlüğü — Çok Ajanlı Şirket Programı (Görev 3)

**Sürüm:** v3.0 (Görev 3 — Çok Ajanlı Lojistik Karar Destek Sistemi Uyumlu)  
**Rol ve Sorumlu:** DQ / Ajan 3 — Ece Naz Aktürk (@ece-naz) & BE / Ajan 2 — Aykut Çakıcı (@Aykuutt)  
**Şirket:** Grup B — Logistics Intelligence Network (LIN)  
**Tarih:** 2026-11-24  
**İlgili Duyuru:** [Duyuru 10](https://github.com/MAKU-VBA-GBT-II/ders/blob/main/Duyuru-10_2026-11-20.md)  

---

## 1. Genel Bakış ve Amaç
Bu veri sözlüğü, Görev 3 kapsamında geliştirilen **Çok Ajanlı Şirket Programı** için veri modellerini, parametrik simülasyon kurallarını ve dış web kaynakları (MGM, KGM, Akaryakıt) ile şirket içi sentetik sevkiyat verilerinin eşleştirme standartlarını belirler.

Sistemde:
- **İç Veri (Sentetik):** Şirketin aktif sevkiyat operasyonları, rotalar, ağırlıklar, taşıma modları ve baz maliyetler.
- **Dış Veri (Gerçek & Kamusal):** Meteoroloji Genel Müdürlüğü (MGM) meteorolojik uyarı haritası, Karayolları Genel Müdürlüğü (KGM) yol durumu bülteni ve serbest akaryakıt pompa fiyatları.
- **Kişisel Veri:** Sistemde gerçek kişi, şoför, müşteri kimliği veya kişisel profil verisi kesinlikle barındırılmaz ve toplanmaz.

---

## 2. Veri Kümesi Özellikleri
- **Örnek Veri Dosyası:** `data/lojistik_sevkiyat_g3_ornek.csv`
- **Hedef Satır Sayısı:** 140 satır (7 gün × 20 sevkiyat/gün)
- **Karakter Kodlaması:** UTF-8
- **Ayraç:** Virgül (`,`)
- **Tohum (Seed):** 42 (Tekrarlanabilir)

---

## 3. Dinamik Simülasyon Parametreleri (Duyuru 10 Kural 3)
`src/simulasyon.py` betiği, web kaynaklarından gelen uyarılara göre dışarıdan dinamik liste ve aralık parametreleri alabilir:

| Parametre | Tip | Varsayılan | Açıklama |
|---|---|---|---|
| `--tohum` (`seed`) | Tam sayı | `42` | Rastgelelik tohumu |
| `--gun-sayisi` (`days`) | Tam sayı | `7` | Simüle edilecek gün sayısı (analiz haftası) |
| `--gunluk-sevkiyat` | Tam sayı | `20` | Gün başına üretilecek sevkiyat sayısı |
| `--baslangic-tarihi` | Metin | `2026-11-20` | `YYYY-MM-DD` ISO başlangıç tarihi |
| `--sehirler` | Metin | `None` (Tüm 8 merkez) | Web uyarısı alan illere odaklanmak için virgülle ayrılmış şehir listesi (örn: `"Istanbul,Ankara,Trabzon"`) |
| `--fiyat-carpani` | Ondalık | `1.0` | Dış piyasadan çekilen akaryakıt fiyatına göre dinamik navlun çarpanı |
| `--gecikme-olasiligi`| Ondalık | `0.15` | Baz operasyonel gecikme olasılığı |
| `--iptal-olasiligi`  | Ondalık | `0.05` | Baz iptal olasılığı |

---

## 4. Alan Tanımları ve Veri Şeması

| Alan Adı | Veri Tipi | Zorunlu | Format / Kural | Örnek |
|---|---|:---:|---|---|
| `sevkiyat_id` | String | Evet | Benzersiz format: `SVK-G3-XXXX` | `SVK-G3-0012` |
| `tarih` | String (ISO) | Evet | `YYYY-MM-DD` ISO tarih formatı | `2026-11-20` |
| `cikis_sehri` | String | Evet | Web kaynaklarıyla eşleşen 8 merkez il | `Antalya` |
| `varis_sehri` | String | Evet | 8 merkez il (`varis_sehri != cikis_sehri`) | `Istanbul` |
| `tasima_modu` | String | Evet | `kara`, `deniz`, `hava`, `demiryolu` | `kara` |
| `agirlik_kg` | Integer | Evet | `50` - `10000` kg arası tam sayı | `4538` |
| `mesafe_km` | Integer | Evet | Karayolu ve mod katsayılı mesafe (`100` - `1800` km) | `700` |
| `ucret_tl` | Float | Evet | `(agirlik * 0.50) + (mesafe * mod_çarpanı * 1.6) * fiyat_carpani` (2 ondalık) | `3389.00` |
| `teslim_suresi_saat` | Float | Koşullu | 1 ondalık basamak. **Kural:** `durum == 'iptal'` ise **BOŞ** kalmalıdır. | `24.0` |
| `durum` | String | Evet | `zamaninda`, `gecikmeli`, `iptal` | `gecikmeli` |

---

## 5. Web Kaynakları Eşleme Şeması (Ajanlar Arası Veri Bağı)

| Dış Web Kaynağı | Web Veri Alanı | İç Veri Eşleşmesi (`data/`) | Ajan 2 İşleme Kuralı |
|---|---|---|---|
| **MGM Uyarı Haritası** | Uyarı Alan İl (`il_adi`), Uyarı Türü (`tur: kar/firtina`), Uyarı Seviyesi (`seviye: sari/turuncu/kirmizi`) | `cikis_sehri` ve `varis_sehri` | Rota güzergahında sarı uyarı varsa risk puanı +25, turuncu uyarıda +50 puan eklenir. |
| **KGM Yol Bülteni** | Güzergah (`guzergah`), Durum (`kapali/tek_serit`), Neden (`kar/heyelan`) | `cikis_sehri` - `varis_sehri` mesafesi | Kapalı yolda tahmini gecikme süresine +12 saat eklenir, teslim süresi güncellenir. |
| **Akaryakıt Fiyatı** | İl bazlı motorin pompa fiyatı (`fiyat_tl`) | `ucret_tl` | Simülasyonun `--fiyat-carpani` katsayısını belirler. |

---

## 6. Ajanlar Arası Mesajlaşma Formatı (JSON Standardı)

Ajan 1'den Ajan 2'ye ve Ajan 2'den Ajan 3'e aktarılan mesaj paketlerinde bulunması zorunlu alanlar:
```json
{
  "mesaj_id": "MSG-G3-20261124-001",
  "uretim_zamani": "2026-11-24T10:00:00Z",
  "kaynak_ajan": "Ajan_1_WebToplayici",
  "hedef_ajan": "Ajan_2_RiskAnaliz",
  "veri": {
    "mgm_uyarilari": [
      {
        "il": "Trabzon",
        "seviye": "turuncu",
        "tur": "yogun_kar",
        "kaynak_url": "https://www.mgm.gov.tr/tahmin/meteorolojik-uyari-ve-degerlendirmeler.aspx"
      }
    ],
    "kgm_yol_durumu": [
      {
        "guzergah": "Trabzon-Gaziantep",
        "durum": "tek_serit",
        "kaynak_url": "https://www.kgm.gov.tr"
      }
    ]
  }
}
```

---

## 7. Kabul ve Doğrulama Kriterleri
- [ ] `src/simulasyon.py` betiği `--sehirler` argümanıyla sadece seçilen iller arasında sevkiyat üretebilmelidir.
- [ ] Dış web kaynaklarındaki il isimleri ile simülasyondaki `cikis_sehri` ve `varis_sehri` birebir uyumlu olmalıdır.
- [ ] `durum == 'iptal'` kayıtlarında `teslim_suresi_saat` alanı kesinlikle boş bırakılmalıdır.
- [ ] Üretilen tüm sayılar kaynak URL ve zaman damgasıyla taşınmalıdır.
