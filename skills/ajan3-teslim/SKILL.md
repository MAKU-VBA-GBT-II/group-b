---
name: ajan3-teslim
description: Riskli sevkiyatlar için resmi duyuru bağlantılı şeffaf müşteri mesajları üretir ve ACP uyumlu teslim paketi hazırlar.
---

# ajan3-teslim — Ajan 3 Müşteri Mesajı ve Nihai Teslim Skill'i

## Amaç
Denetimden geçen kritik riskli sevkiyatlar için müşteriye iletilecek şeffaf, resmi Karayolları (KGM) veya Meteoroloji (MGM) dayanak bağlantılarını içeren bilgilendirme metinlerini oluşturur. Nihai sonuçları `docs/oneri.md` §6 ve `docs/veri-sozlugu.md` v3.0 standartlarında ACP JSON paketi (`data/ajan3_mesaj.json`) ve yönetim denetim raporu (`data/ajan3_denetim_raporu.md`) olarak teslim eder.

## Girdiler
- Onaylanan yüksek riskli sevkiyatlar listesi
- Ajan 2 kaynak nesneleri

## Çıktılar
- **`data/ajan3_mesaj.json`**: Çekirdek ve Arayüz modülünün beklediği nihai ACP mesaj paketi.
- **`data/ajan3_denetim_raporu.md`**: Yönetim ve PM incelemesi için Markdown formatında denetim raporu.

## Müşteri Mesajı Standartları
1. Sevkiyat takip numarası (`sevkiyat_id`), güzergah ve tahmini ek gecikme süresi net belirtilir.
2. Gecikmenin dayandığı resmi KGM veya MGM duyurusu **tıklanabilir web bağlantısı** olarak mesaja eklenir.
3. Şirketin kurumsal ve profesyonel dil standardı korunur.

## Nasıl Çalıştırılır
```bash
python src/ajan3_denetim.py --cikti-json data/ajan3_mesaj.json --cikti-md data/ajan3_denetim_raporu.md
```
