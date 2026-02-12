#1)Lambda; tek bir satira sigan, ismi olmayan fonksiyonlardir.
#Küçük bir işiniz için kocaman bir def tanimlamadan işinizi halletmenize yarar.

#--fonksiyon
def karesini_al(x):
    return x**2

#--Lambda
kare_lambda = lambda x: x**2

#2)lambda içinde print yapabilirsin ama if x: y=1 gibi bir atama yapamazsin.

#3)filtrelemede kullanilir (filter operatoru ile) ekrana yazdirmak için listeye cevirilir:

voltages = [1.2, 4.5, 0.8, 5.5, 2.1]
# 2.0 Volt üzerindeki değerleri seç
high_voltages = list(filter(lambda v: v > 2.0, voltages))

#3.2 any/all operatorleri ile filtreleme
sayilar = [2,1,4,6,10,8,14,12]
kontrol = lambda sayilar: any(x % 2==1 for x in sayilar)#cikti olarak kontrol degeri 1 (1 elemani var)
kontrol = lambda sayilar: all(x % 2==1 for x in sayilar)#cikti olarak kontrol degeri 0 (1 elemani var)

#4)siralama islemlerinde kullanilir(sorted operatoru ile):

liste = [(1, 5), (2, 3), (4, 1)]
#--fonksiyon:
def ikincieleman(x):
    return x[1]
sirali = sorted(liste, key=ikincieleman)
#--lambda:
sirali = sorted(liste, key=lambda x: x[1])

#5)iterator bir nesne cevirmek için kullanilir (map operatoru ile) ekrana yazdirmak için listeye cevirilir:
sayilar = [1, 2, 3, 4]
sonuc = list(map(lambda x: x * 2, sayilar))

#6)fonksiyonda ic referans olarak kullanilir:
def carp(n):
    return lambda x: x * n

ikiyle_carp = carp(2)# n degeri 2 olarak kaldi hala fonksiyonun x degeri belirsiz
print(ikiyle_carp(5))# x degeri 5 aldi ....cikti= 2*5 den 10

#7)min/max problemlerinde kullanilir:
ogrenciler = [
    {"isim": "Ali", "not": 70},
    {"isim": "Ayşe", "not": 90},
    {"isim": "Mehmet", "not": 60}
]

en_yuksek = max(ogrenciler, key=lambda x:x["not"])
en_dusuk = min(ogrenciler, key=lambda x:x["not"])

#8) toplam ve yuvarlama islemlerinde sum/round operatorleri ile kullanilir.
# Bu operatorler iterable nesne almasi lazim yani map operatoru ile kullanacagiz.

ogrenciler = [
    {"isim": "Ali", "not": 76},
    {"isim": "Ayşe", "not": 74}
]
toplam = sum(map(lambda x: x["not"], ogrenciler))
#yuvarlama islemlerinde kullanilir:
max(ogrenciler, key=lambda x: round(x["not"] / 10))

