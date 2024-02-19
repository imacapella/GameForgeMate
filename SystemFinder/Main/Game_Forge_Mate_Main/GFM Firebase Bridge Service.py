from flask import Flask, request, jsonify
from google.cloud import firestore
from google.oauth2 import service_account
import pandas as pd
from io import StringIO

# Firebase Admin Ath
credentials = service_account.Credentials.from_service_account_file(
    "SystemFinder/Main/Game_Forge_Mate_Main/4_GFM_Firebase_Ath.json",
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

# Firestore Connect
fdb = firestore.Client(credentials=credentials)
app = Flask(__name__)

# Flask Route
@app.route('/<category>')
def csv(category):

    datacol = fdb.collection('csv_files')
    document = datacol.document(category)

    if not document.get().exists:
        return jsonify({"error": f"({category}) kayıp. Bulmak için /content"})


    content = document.get().to_dict()['content']

   #Pandas
    try:

        frame = pd.read_csv(StringIO(content))

        # Rank Filter
        rank = request.args.get('rank')
        if rank:
            filter = int(rank)
            frame = frame[frame['Rank'] == filter]

        # JSON
        result = frame.to_dict(orient='records')

        return jsonify(result)
    except pd.errors.EmptyDataError:
        return jsonify({"error": "CSV dosyası boş."})
    except pd.errors.ParserError:
        return jsonify({"error": "CSV dosyası geçerli bir format değil."})

if __name__ == '__main__':
    app.run(debug=True)


