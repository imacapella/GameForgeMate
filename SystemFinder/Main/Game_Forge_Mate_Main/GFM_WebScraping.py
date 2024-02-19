import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote
from GFM_HardwareCheck import GameHardwareChecker
import time
import re
import csv

time.sleep(1)


def read_games_from_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row['GameName'] for row in reader]


file_path = 'SystemFinder/Main/Game_Forge_Mate_Main/1_games_list.csv'  # Update with the path to your CSV file
game_names = read_games_from_csv(file_path)


checker = GameHardwareChecker()


highest_cpu, highest_cpu_rank, highest_gpu, highest_gpu_rank = checker.find_highest_ranked_hardware(game_names)

# En iyi CPU ve GPU bilgilerini al
gpu_name = highest_gpu['Model'] if highest_gpu else "Default GPU Model"
cpu_name = highest_cpu['Model'] if highest_cpu else "Default CPU Model"


header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0"
}


def format_gpu_name(name):
    # GPU adındaki "NVIDIA Geforce" veya "AMD" kısmını temizle (büyük küçük harf duyarsız)
    cleaned_name = re.sub(r"(geforce|nvidia geforce|nvidia geforce rtx|amd)", "", name, flags=re.IGNORECASE).strip()
    return cleaned_name

def format_cpu_name(name):
    # CPU adındaki "Intel Core" veya "AMD" kısmını temizle (büyük küçük harf duyarsız)
    cleaned_name = re.sub(r"(intel core|amd)", "", name, flags=re.IGNORECASE).strip()
    return cleaned_name

# GPU adını temizle
formatted_gpu_name = format_gpu_name(gpu_name)

# CPU adını temizle
formatted_cpu_name = format_cpu_name(cpu_name)

# formatted_gpu_name ve formatted_cpu_name'yi URL'ye çevirme
encoded_gpu_name = quote(formatted_gpu_name)
encoded_cpu_name = quote(formatted_cpu_name)
encoded_gpu_name1 = quote(gpu_name)
encoded_cpu_name1 = quote(cpu_name)
print(" ")
print("-------Encoded and Formatted Test-------")
#BU ALAN TEST İÇİN YAZILDI
print("Formatted GPU Name:", formatted_gpu_name)
print("Formatted CPU Name:", formatted_cpu_name)
print("Encoded GPU Name:", encoded_gpu_name)
print("Encoded CPU Name:", encoded_cpu_name)
print("-------Best GPU and CPU-------")
print(" ")
print("GPU Name:", gpu_name)
print("CPU Name:", cpu_name)
#BU ALAN TEST İÇİN YAZILDI

#####################################################SİSTEM ÖNERİSİ İÇİN YAZILDI######################################################################
print(" ")
print("---------------------------------------")
print("Aramanızla İlgili Sonuçlar:")
print("---------------------------------------")
print(" ")

# GAMEGARAJ.COM İÇİN ARAMA YAPTIM
url1 = f"https://www.gamegaraj.com/?s={encoded_cpu_name}+{encoded_gpu_name}"
get1 = requests.get(url1, headers=header)
content1 = get1.content
soup1 = BeautifulSoup(content1, "html.parser")

# VATANBİLGİSAYAR.COM İÇİN ARAMA YAPTIM
url2 = f"https://www.vatanbilgisayar.com/oem-hazir-sistemler/?qText={encoded_cpu_name}+{encoded_gpu_name}"
get2 = requests.get(url2, headers=header)
content2 = get2.content
soup2 = BeautifulSoup(content2, "html.parser")

# GAMİNG.COM.TR İÇİN ARAMA YAPTIM AYRICA BU SİTEDEN OYUN FPSLERİNE GÖRE SİSTEM GETİREBİLİRİZ
url3 = f"https://www.gaming.gen.tr/?s={encoded_cpu_name}+{encoded_gpu_name}&post_type=product&dgwt_wcas=1"
get3 = requests.get(url3, headers=header)
content3 = get3.content
soup3 = BeautifulSoup(content3, "html.parser")

# AKAKCE.COM İÇİN ARAMA YAPTIM. Burda sistem filtreleme işimiz daha kolay gibi geldi
url5 = f"https://www.akakce.com/arama/?q={encoded_cpu_name}+{encoded_gpu_name}&c=1002"
get5 = requests.get(url5, headers=header)
content5 = get5.content
soup5 = BeautifulSoup(content5, "html.parser")
#HEPSİBURADA.COM İÇİN ARAMA YAPTIM.BURDA 11 DEN BAŞLAYACAK KAFA KARIŞMASIN
url11 = f"https://www.hepsiburada.com/ara?q={encoded_cpu_name}+{encoded_gpu_name}&filtreler=MainCategory.Id:46&kategori=2147483646_8_46"
get11 = requests.get(url11, headers=header)
content11 = get11.content
soup11 = BeautifulSoup(content11, "html.parser")
##########################################################################sistem önerisi ürün bulma işlemi############################################################################################################
# GAMEGARAJ.COM ÜRÜN BULMA İŞLEMİ
products1 = soup1.find_all("div", {"class": "edgtf-search-page-holder"})

first_product_link1 = None

if products1:
    first_product_link1_elem = products1[0].find("a")
    if first_product_link1_elem:
        first_product_link1 = urljoin("https://www.gamegaraj.com", first_product_link1_elem["href"])
        print(first_product_link1)
    else:
        print("İlgili sonuç GameGaraj stoktlarında bulunamamıştır.")

time.sleep(0.5)

first_product_link2 = None

# VATANBİLGİSAYAR.COM sistemi bulma işlemi
products2 = soup2.find_all("div", {"class": "wrapper-product wrapper-product--list-page clearfix"})
if products2:
    first_product_link2_elem = products2[0].find("a")
    if first_product_link2_elem:
        first_product_link2 = urljoin("https://www.vatanbilgisayar.com", first_product_link2_elem["href"])
        print(first_product_link2)
    else:
        print("İlgili sonuç Vatan Bilgisayar stoktlarında bulunamamıştır.")

time.sleep(0.5)

first_product_link3 = None

#GAMİNGGENTR.COM ÜRÜN BULMA İŞLEMİ
products3 = soup3.find_all("ul", class_="products columns-3")
if products3:
    first_product_link3 = urljoin("https://www.gaming.gen.tr", products3[0].find("a")["href"])
    print(first_product_link3)
else:
    print("İlgili sonuç Gaming Gen TR stoktlarında bulunamamıştır.")

time.sleep(0.5)

first_product_link5 = None

#AKAKCE ÜRÜN BULMA İŞLEMİ
products5 = soup5.find_all("ul", {"class": "pl_v9 qv_v9"})
if products5:
    first_product_link5_elem = products5[0].find("a")
    if first_product_link5_elem:
        first_product_link5 = urljoin("https://www.akakce.com", first_product_link5_elem["href"])
        print(first_product_link5)
    else:
        print("İlgili sonuç Akakçe stoktlarında bulunamamıştır.")

first_product_link11 = None

#HEPSİBURADA.COM SİSTEM BULMA İŞLEMİ
products11 = soup11.find_all("ul", {"class": "productListContent-frGrtf5XrVXRwJ05HUfU productListContent-rEYj2_8SETJUeqNhyzSm"})
if products11:
    first_product_link11 = urljoin("https://www.hepsiburada.com", products11[0].find("a")["href"])
    print(first_product_link11)
else:
    print("İlgili sonuç Hepsiburada stoktlarında bulunamamıştır.")
    #############################################################BURDAN SONRASI PARÇA ÖNERİSİ İÇİN YAZILDI######################################################################
#Sinerji.com arama yapma gpu
url4 = f"https://www.sinerji.gen.tr/arama?q={encoded_gpu_name}-s"
get4 = requests.get(url4, headers=header)
content4 = get4.content
soup4 = BeautifulSoup(content4, "html.parser")

#sinerji.com arama yapma cpu
url12 = f"https://www.sinerji.gen.tr/arama?q={encoded_cpu_name}-s"
get12 = requests.get(url12, headers=header)
content12 = get12.content
soup12 = BeautifulSoup(content12, "html.parser")

#CİMRİ.com arama yapma gpu
url6 = f"https://www.cimri.com/arama?q={encoded_gpu_name}"
get6 = requests.get(url6, headers=header)
content6 = get6.content
soup6 = BeautifulSoup(content6, "html.parser")

#CİMRİ.com arama yapma cpu
url7 = f"https://www.cimri.com/arama?q={encoded_cpu_name}"
get7 = requests.get(url7, headers=header)
content7 = get7.content
soup7 = BeautifulSoup(content7, "html.parser")

#N11.COM ARAMA YAPMA GPU
url8 = f"https://www.n11.com/bilgisayar/bilgisayar-bilesenleri/ekran-karti?q={encoded_gpu_name}"
get8 = requests.get(url8, headers=header)
content8 = get8.content
soup8 = BeautifulSoup(content8, "html.parser")
#ITOPYA.COM CPU KATEGORİSİ GELMİYOR FİLTRELEME İŞLEMİ YAPILMIYOR O YÜZDEN EKRAN KARTINI GETİREBİLİYORUM SADECE

#hepsiburada.COM ARAMA YAPMA CPU
url9 = f"https://www.hepsiburada.com/ara?q={encoded_cpu_name}&filtreler=MainCategory.Id:46&kategori=2147483646_8_46"
get9 = requests.get(url9, headers=header)
content9 = get9.content
soup9 = BeautifulSoup(content9, "html.parser")

#hepsiburada.com arama yapma gpu
url10 = f"https://www.hepsiburada.com/ara?q={encoded_gpu_name}&filtreler=MainCategory.Id:204&kategori=2147483646_8_204"
get10 = requests.get(url10, headers=header)
content10 = get10.content
soup10 = BeautifulSoup(content10, "html.parser")

########################################################parça ürünü bulma işlemi############################################################################################################
#Ürün bulma sinerji gpu
first_product_link4 = None

products4 = soup4.find_all("section", {"class": "row productList"})
if products4:
    # url dönüştürme işlemi
    first_product_link4 = urljoin("https://www.sinerji.gen.tr", products4[0].find("a")["href"])
    print(first_product_link4)
else:
    print("İlgili sonuç Sinerji stoktlarında bulunamamıştır.")

first_product_link12 = None
#ürün bulma sinerji cpu
products12 = soup12.find_all("section", {"class": "row productList"})
if products12:
    # url dönüştürme işlemi
    first_product_link12 = urljoin("https://www.sinerji.gen.tr", products12[0].find("a")["href"])
    print(first_product_link12)

first_product_link6 = None
#ürün bulma cimri gpu
products6 = soup6.find_all("div", {"class": "s1cegxbo-1 cACjAF"})
if products6:
    first_product_link6 = urljoin("https://www.cimri.com", products6[0].find("a")["href"])
    print(first_product_link6)
else:
    print(f"İlgili sonuç Cimri stoktlarında bulunamamıştır.")

first_product_link7 = None
# Ürün bulma cimri cpu
products7 = soup7.find_all("div", {"class": "s1cegxbo-1 cACjAF"})
if products7:
    first_product_link7 = urljoin("https://www.cimri.com", products7[0].find("a")["href"])
    print(first_product_link7)

first_product_link8 = None
#ÜRÜN BULMA N11 GPU
products8 = soup8.select("ul.list-ul a")
if products8:
    anchor_tags = products8[0].find_all("a")
    if anchor_tags:
        first_product_link8 = urljoin("https://www.n11.com", anchor_tags[0]["href"])
        print(first_product_link8)

else:
    print(f"İlgili sonuç N11 stoktlarında bulunamamıştır.")

first_product_link9 = None
#ÜRÜN BULMA HEPSİBURADA CPU
products9 = soup9.find_all("ul", {"class": "productListContent-frGrtf5XrVXRwJ05HUfU productListContent-rEYj2_8SETJUeqNhyzSm"})
if products9:
    first_product_link9 = urljoin("https://www.hepsiburada.com", products9[0].find("a")["href"])
    print(first_product_link9)

first_product_link10 = None
#ÜRÜN BULMA HEPSİBURADA GPU
products10 = soup10.find_all("ul", {"class": "productListContent-frGrtf5XrVXRwJ05HUfU productListContent-rEYj2_8SETJUeqNhyzSm"})
if products10:
    first_product_link10 = urljoin("https://www.hepsiburada.com", products10[0].find("a")["href"])
    print(first_product_link10)

def write_to_csv(file_path, data):

    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for item in data:
            writer.writerow([item])

# CSV'ye yazılacak URL'lerin listesi
urls_to_write = [
    first_product_link1, first_product_link2, first_product_link3,
    first_product_link5, first_product_link11, first_product_link4,
    first_product_link12, first_product_link6, first_product_link7,
    first_product_link8, first_product_link9, first_product_link10
]

# URL'leri CSV'ye yaz
output_file_path = 'SystemFinder/Main/Game_Forge_Mate_Main/2_product_links.csv'  
write_to_csv(output_file_path, urls_to_write)
