import random
import csv
import os

# data klasörü yoksa otomatik oluştur
os.makedirs("data", exist_ok=True)

# 1 ile 100 arasında rastgele 10 sayı üret
sayilar = [random.randint(1, 100) for _ in range(10)]

# CSV dosyasına yaz
dosya_yolu = os.path.join("data", "prova-aykut.csv")
with open(dosya_yolu, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["deger"])  # Başlık satırı
    for sayi in sayilar:
        writer.writerow([sayi])

print("data/prova-aykut.csv başarıyla oluşturuldu!")