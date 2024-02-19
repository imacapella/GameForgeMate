import pandas as pd

# CSV dosyasını oku
df = pd.read_csv('/Users/murathankarasu/PycharmProjects/SystemFinder/Main/CSV_Edit/games1000row.csv')

# Sütun isimlerindeki boşlukları sil
df.columns = df.columns.str.strip()

# "Graphics Card" sütununda " or " varsa, sonrasını sil ve değerlerdeki boşlukları sil
df['Graphics Card:'] = df['Graphics Card:'].str.split(' or ').str[0].str.strip()

# String tipindeki tüm sütunlardaki değerlerdeki boşlukları sil
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].str.strip()

# Sonuçları yeni bir CSV dosyasına kaydet
df.to_csv('/Users/murathankarasu/PycharmProjects/SystemFinder/Main/CSV_Edit/games.csv', index=False)
