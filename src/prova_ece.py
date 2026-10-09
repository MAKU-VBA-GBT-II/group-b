import random
import os

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

with open('data/prova-ece.csv', 'w', encoding='utf-8') as f:
    f.write("deger\n")
    for _ in range(10):
        f.write(f"{random.randint(1, 100)}\n")

print("Dosya oluşturuldu: data/prova-ece.csv")
