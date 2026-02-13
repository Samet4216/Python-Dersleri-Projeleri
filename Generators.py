#Generator'lar, normal fonksiyonlara benzerler ama return yerine yield kullanirlar.
#1)yield, fonksiyonun durumunu kaydeder ve bir sonraki cagrildiginda kaldigi yerden devam etmesini saglar.
def basit_sensor_ureteci():
    yield 10.1
    yield 10.5
    yield 11.0

gen = basit_sensor_ureteci()
print(next(gen)) # 10.1
print(next(gen)) # 10.5

#2)cagri olmadan once deger uretilmez her next cagrisinda siradaki gelir bellege
def liste_uret():
    return [i for i in range(1_000_000)]#hepsini ayni anda uretir ve 1m veri bellekte saklanir
def gen_uret():
    for i in range(1_000_000):#ihtiyaci oldukca siradaki veriyi uretir yani 1 den 2 ye gecerken 1 i hafizadan siler.
        yield i
#list comprehension da [] kullanilir ve hepsi ayni anda bellekte saklanirken generator ler () kullanir.

#3)generatorler ayni zamanda iteratordur:
g = gen_uret()

print(hasattr(g, "__iter__"))  # True
print(hasattr(g, "__next__"))  # True

#4)send() ile iceri veri gonderirsin:
def ortalama_hesapla():
    toplam = 0
    adet = 0
    while True:#disaridan veri aliyorsak sonsuz dongu kullanmaliyiz cunku kac data gelecek bilmiyoruz.
        yeni = yield #son kalan degisken yield ile yeri tutulur.
        toplam += yeni
        adet += 1
        print("Ortalama:", toplam/adet)

g = ortalama_hesapla()
next(g)  #baslatmak zorundayiz

g.send(10)#disaridan fonksiyona veri gondermek icin send kullaniriz
g.send(20)
g.send(30)

#5)baska yiekd fonksiyonundah uretilen veriyi disari gondermek icin:
def diger():
    yield 1
    yield 2
    yield 3

def wrapper():
    yield from diger()#from kullanilarak belirtilen fonksiyona kopru saglariz.

def wrapper():
    return diger()#boyle de yapilabilir.

for i in wrapper():
    print(i)