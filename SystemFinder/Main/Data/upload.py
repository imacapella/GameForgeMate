from google.cloud import firestore
from google.oauth2 import service_account
import os

# Firebase Admin Auth
credentials = service_account.Credentials.from_service_account_file(
    "/Main/4_GFM_Firebase_Ath.json",
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

# Firestore Connection
fdb = firestore.Client(credentials=credentials)

# CSV File
def csv_to_firestore(file_name, content):
    csv_doc = fdb.collection('csv_files').document(file_name)
    csv_doc.set({'content': content})
    print(f"{file_name} Firestore'a yüklendi.")

csv_filename = ['games']

for file_name in csv_filename:
    try:
        path = f'/Users/murathankarasu/PycharmProjects/SystemFinder/Main/CSV/{file_name}.csv'
        size = os.path.getsize(path)

        with open(path, 'r') as file:
            content = file.read()
            current_size = 0

            while True:
                bar = file.read(4096)
                if not bar:
                    break
                current_size += len(bar)
                progress = (current_size / size) * 100
                print(f"Yükleniyor: {progress:.2f}% tamamlandı", end='\r')

            print(f"Yükleniyor: yükleme tamamlandı")

            csv_to_firestore(file_name, content)

    except Exception as e:
        print(f"{file_name} bir hata oluştu: {e}")
