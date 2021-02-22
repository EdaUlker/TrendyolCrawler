
from bs4 import BeautifulSoup
import requests
import xlsxwriter
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler

list_of_url = []


for i in range(30):
    response = requests.get("https://www.trendyol.com/laptop?pi=" + str(i))
    

    beautifulsoup=BeautifulSoup(response.content)
    mydivs=beautifulsoup.findAll("div",{"class":"p-card-chldrn-cntnr"})
    

    for div in mydivs:
        x=div.find_all("a")
        #print(div.get("href"))
        for a in x:
            #print(a.get("href"))
            url= a.get("href")
            full_url = "https://www.trendyol.com" + url
            list_of_url.append(full_url)


workbook = xlsxwriter.Workbook('onislemesiz_veri1.xlsx')
worksheet = workbook.add_worksheet()
count = 2


worksheet.write('A1', 'MARKA')
worksheet.write('B1', 'ISLEMCI TIP')
worksheet.write('C1', 'RAM')
worksheet.write('D1', 'SSD')
worksheet.write('E1', 'EKRAN BOYUTU')
worksheet.write('F1', 'FIYAT')



for i, url in enumerate(list_of_url):
    print(f"{i}/{len(list_of_url)} url isleniyor...")
    
    response=requests.get(url)
    bs = BeautifulSoup(response.content)
 
    fiyat = bs.findAll("span", {"class": "prc-slg"})[0]
    baslik = bs.findAll("h1",{"class":"pr-new-br"})[0]
    marka = baslik.get_text().split(" ")[0]
    urunozellikleri = bs.findAll("div",{"class":"prop-item"})
    
    worksheet.write('A' + str(count), marka)
    worksheet.write('F' + str(count), str(fiyat))
    worksheet.write('G' + str(count), url)
    


    for items in urunozellikleri:
        if items.get_text().startswith("İşlemci Tipi"): 
            #print(items.get_text().split(":")[1])
            worksheet.write('B' + str(count), items.get_text().split(":")[1])
        
        elif items.get_text().startswith("Ram"):
            #print(items.get_text().split(":")[1])
            worksheet.write('C' + str(count), items.get_text().split(":")[1])
        elif items.get_text().startswith("SSD"):
            #print(items.get_text().split(":")[1])
            worksheet.write('D' + str(count), items.get_text().split(":")[1])
        elif items.get_text().startswith("Ekran Boy"):
            #print(items.get_text().split(":")[1])
            worksheet.write('E' + str(count), items.get_text().split(":")[1])
    
    count += 1





list_of_url = []

for i in range(30):
    response = requests.get("https://www.trendyol.com/laptop?pi=" + str(i))
    
    
    beautifulsoup=BeautifulSoup(response.content)
    mydivs=beautifulsoup.findAll("div",{"class":"p-card-chldrn-cntnr"})
    
    for div in mydivs:
        x=div.find_all("a")
        #print(div.get("href"))
        for a in x:
            #print(a.get("href"))
            url= a.get("href")
            full_url = "https://www.trendyol.com" + url
            list_of_url.append(full_url)


workbook = xlsxwriter.Workbook('onislemelilaptop_verisi.xlsx')
worksheet = workbook.add_worksheet()
count = 2
worksheet.write('A1', 'MARKA')
worksheet.write('B1', 'ISLEMCI TIP')
worksheet.write('C1', 'RAM')
worksheet.write('D1', 'SSD')
worksheet.write('E1', 'EKRAN BOYUTU')
worksheet.write('F1', 'FIYAT')

for i, url in enumerate(list_of_url):
    print(f"{i}/{len(list_of_url)} url isleniyor...")
    
    response=requests.get(url)
    bs = BeautifulSoup(response.content)
    
    fiyat = bs.findAll("span", {"class": "prc-slg"})[0].get_text().replace("TL","")
    baslik = bs.findAll("h1",{"class":"pr-new-br"})[0]
    marka = baslik.get_text().split(" ")[0]
    urunozellikleri = bs.findAll("div",{"class":"prop-item"})
    
    worksheet.write('A' + str(count), marka)
    worksheet.write('F' + str(count), str(fiyat))
    
    for items in urunozellikleri:
        if items.get_text().startswith("İşlemci Tipi"):      
            #print(items.get_text().split(":")[1])
             worksheet.write('B' + str(count), items.get_text().split(":")[1])
               
        elif items.get_text().startswith("Ram"):
            # print(items.get_text().split(":")[1])
             worksheet.write('C' + str(count), items.get_text().split(":")[1].replace("GB",""))
            
        elif items.get_text().startswith("SSD"):
            #print(items.get_text().split(":")[1])
             worksheet.write('D' + str(count), items.get_text().split(":")[1].replace("GB","").replace("1 TB","1024"))
            
        elif items.get_text().startswith("Ekran Boy"):
            # print(items.get_text().split(":")[1])
             worksheet.write('E' + str(count), items.get_text().split(":")[1].replace("inç",""))
                
    count += 1





dataset = pd.read_excel('onislemelilaptop_verisi.xlsx')

dataset = dataset.dropna()

X_orginal = dataset.iloc[:, :-1]
Y_orginal = dataset.iloc[:, -1].values

X_orginal["MARKA"] = X_orginal["MARKA"].apply(lambda x:x.upper())
X_orginal["MARKA"] = X_orginal["MARKA"].apply(lambda x:x.replace("-", ""))


ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(sparse=False), [0])], remainder='passthrough')
X = ct.fit_transform(X_orginal)

count = 0


for a in X[0]:
    if type(a) == str:
        break
    count+=1

ct2 = ColumnTransformer(transformers=[('encoder', OneHotEncoder(sparse=False), [count])], remainder='passthrough')
X = ct2.fit_transform(X)

for i in range(X.shape[0]):
    X[i, -2] = X[i, -2].replace('Yok', '0')
    X[i, -1] = X[i, -1].replace('.', '')
    X[i, -1] = X[i, -1].replace(',', '.')
    X[i, -1] = float(X[i, -1])
    X[i, -2] = float(X[i, -2].replace(' TB', 'e3'))
        
min_max  = MinMaxScaler()
min_max.fit(X)
X_normal = min_max.transform(X)

for i in range(Y_orginal.shape[0]):
    Y_orginal[i] = Y_orginal[i].replace(".", "")
    Y_orginal[i] = Y_orginal[i].replace(",", ".")
    Y_orginal[i] = float(Y_orginal[i])
    
Y_orginal = Y_orginal.reshape(-1, 1)
min_max_y = MinMaxScaler()
min_max_y.fit(Y_orginal)
Y_normal = min_max_y.transform(Y_orginal)


birlesik = np.concatenate((X_normal, Y_normal), axis=1)
data_f = pd.DataFrame(birlesik)
data_f.to_excel('onislenmislaptop_verisi.xlsx')