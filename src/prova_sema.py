import csv
import os
import random

# data klasörünün yolu (src klasörünün bir üstündeki data)
klasor = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
os.makedirs(klasor, exist_ok=True)

# 1-100 arası 10 rastgele sayı
sayilar = [random.randint(1, 100) for _ in range(10)]

with open(os.path.join(klasor, "prova-sema.csv"), "w", newline="", encoding="utf-8") as f:
    yazici = csv.writer(f)
    yazici.writerow(["deger"])
    for sayi in sayilar:
        yazici.writerow([sayi])