import firebase_admin
from firebase_admin import credentials, firestore
import csv

# Firebase ayarlarını yükle
cred = credentials.Certificate('/Users/murathankarasu/PycharmProjects/SystemFinder/Main/Api/4_GFM_Firebase_Ath.json')
firebase_admin.initialize_app(cred)

# Firestore veritabanına bağlan
db = firestore.client()

# Belirli bir dokümandan veri çek
koleksiyon_adi = 'csv_files'
dokuman_adi = 'games'
doc_ref = db.collection(koleksiyon_adi).document(dokuman_adi)
doc = doc_ref.get()

if doc.exists:
    data = doc.to_dict()

    # CSV olarak kaydet
    with open('gamessdata.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Sütun başlıklarını yaz
        headers = ["Property", "Value"]
        writer.writerow(headers)

        # Verileri yaz
        for key, value in data.items():
            writer.writerow([key, value])

    print(f"{dokuman_adi} dokümanı 'gpu_data.csv' olarak kaydedildi.")
else:
    print(f"{dokuman_adi} dokümanı bulunamadı.")
