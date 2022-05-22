from wsgiref import headers
import requests
from bs4 import BeautifulSoup 
import pandas as pd

yes = pd.DataFrame()
a=1
for i in range(a,13): # WEB SAYFASINDA SON 13 SAYFALIK SONUCLAR GÖRÜNTÜLENDİĞİ İÇİN 13 SAYFALIK DÖNGÜ İCERİSİNDE KODLARIMIZI YAZDIK
    URL = 'https://sgodds.com/football/results-past-odds/page/{}'.format(a)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'}
    sayfa = requests.get(URL, headers = headers)
    icerik = BeautifulSoup(sayfa.content,"lxml")
    a +=1
    takimAdlari =icerik.find_all("div", attrs = {"class":"row border-bottom m-0"})
    strong = icerik.find_all("strong")
    # TAKIMLARI VE SKORLAR LİSTELERE ATILDI
    takimlar = []
    skorlar = []
    for takimAdi in takimAdlari:
        takimlar.append(takimAdi.a.text)
        skorlar.append(takimAdi.find("div", attrs = {"row"}).text)
    
    # HATALI GELEN SKORLARI 0-0 / 0-0 OLARAK GÜNCELLEDİK    
    
    for i in skorlar:
        b = skorlar.index(i)
        if len(i) != 6:
            skorlar[b] = "0-00-0"
        if i == "\xa0 -\xa0 -":
            skorlar[b] = "0-00-0" 
        
        
    # SKORLAR MAC SONUCU VE İLK YARI OLARAK AYRILDI
    
    macSonucu = []    
    ilkYari = []
    for ilk in skorlar:
        ilkYari.append(ilk[0:3])
    for ms in skorlar:
        macSonucu.append(ms[3:len(ms)])
        
    # MAC SKORLARINA GORE 2.5 ALT-UST TESPİTİ YAPILDI 
    
    altUst = []
    for i in skorlar:
        if (int(i[0]) + int(i[2]) + int(i[3]) + int(i[5])) > 2.5:
            altUst.append("UST")
        else:
            altUst.append("ALT")
            
    # İLK YARI SONUCLARINA VE MAÇ SONUÇLARINA GÖRE VERİLERİ AYIRDIK 
    evSahibiiy = []
    dePiy = []
    evSahibiMs = []
    depMs = []
    for i in ilkYari:
        evSahibiiy.append(int(i[0]))

    for i in ilkYari:
        dePiy.append(int(i[2]))
        
    for i in macSonucu:
        evSahibiMs.append(int(i[0]))

    for i in macSonucu:
        depMs.append(int(i[2]))

    # HANGİ TAKIMIN KAZANDIGINI 1-0-2 OLARAK BELİRLEDİK

    kazananTakım = []

    for i in range(len(depMs)):
        if evSahibiMs[i] > depMs[i]:
            kazananTakım.append(1)
        if depMs[i] > evSahibiMs[i]:
            kazananTakım.append(2)
        if depMs[i] == evSahibiMs[i]:
            kazananTakım.append(0)
        
    # TÜM ORANLAR ÇEKİLİP BİR LİSTEYE ATILDI  

          
    oranlar = []      
    for i in strong:
        oranlar.append(i.text)
        
    yeniOranlar = oranlar[2:-6]
    
    # ORANLAR(HER MAÇTA 3 ORAN OLACAĞI İCİN(EV SAHİBİ-BERABERLİK-DEPLASMAN)) 3'ERLİ GRUPLARA AYRILDI
    
    N = 3
    subList = [yeniOranlar[n:n+N] for n in range(0, len(yeniOranlar), N)]  
    
    # ORANLAR 3 BÖLÜME AYRILDI 
    
    evSahibiOran = []
    beraberlikOran= []
    deplasmanOran= []

    for i in subList:
        evSahibiOran.append(float(i[0]))
    for i in subList:
        beraberlikOran.append(float(i[1]))
    for i in subList:
        deplasmanOran.append(float(i[2]))
        
    # TAKIM ISIMLERI AYRI LİSTELERE ALDINDI
    
    evSahibi = []
    deplasman = []
    for i in takimlar:
        evSahibi.append(i.split("vs")[0])
        
    for i in takimlar:
        deplasman.append(i.split("vs")[1])
        
    # TÜM LİSTELER BİR SÖZLÜKTE BİRLEŞTİRİLDİ VE DATAFRAME OLUŞTURULDU
    
    dicti = {'Ev Sahibi':evSahibi,'Deplasman Takımı':deplasman,'Ev IY':evSahibiiy,"Dep IY":dePiy,"Ev MS":evSahibiMs,"Dep MS":depMs,"Ev Oran":evSahibiOran,"Beraberlik Oran":beraberlikOran,"Dep Oran":deplasmanOran,"Mac Sonucu":kazananTakım,"ALT-UST":altUst}
    
    daf = pd.DataFrame(dicti)
    
    yes = pd.concat([yes,daf])

# SONUCLAR BİR EXCELL DOSYASINA KAYDEDİLDİ

yes.to_csv("sonuclar.csv",index=False)
print(yes)