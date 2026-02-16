#1)Ayni arayuzun(fonksiyonun) farkli veriler icin farkli sekillerde calisabilmesidir.Bir nesne; ihtiyacimiz olan metoda sahipse, o nesneyi kullanabiliriz.
class Kedi:
    def ses_cikar(self):
        return "Miyav"
class Kopek:
    def ses_cikar(self):
        return "Hav hav"
class Inek:
    def ses_cikar(self):
        return "Moo"
# Ayni fonksiyonu kullanarak farkli nesnelerle(hayvanlarla) farkli sonuclar elde ediyoruz.
def hayvan_sesi(hayvan):
    return hayvan.ses_cikar()# Butun hayvanlar icin ortak olan fonksiyondur.Sadece ortak fonksiyonlarla islem yapabiliriz.
# Hayvan_sesi fonksiyonuna parametre olarak istedigimiz sinifi gondeririz.
print(hayvan_sesi(Kedi()))    # Çikti: Miyav
print(hayvan_sesi(Kopek()))   # Çikti: Hav hav
print(hayvan_sesi(Inek()))    # Çikti: Meee


#2)Operator Overloading(Tanimli operatorun ustune yazmak/overloading islemi)=tanimli operatoru degistirip yeni ozellik kazandirmak.
class Vektor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, diger):
        # " + " operatorunun davranisini tanimliyoruz
        return Vektor(self.x + diger.x, self.y + diger.y)
    def __str__(self):
        return f"Vektor({self.x}, {self.y})"

v1 = Vektor(3, 4)
v2 = Vektor(1, 2)
v3 = v1 + v2  #*** v3= v1.__add__(v3) yani v1'e v3 eklenmesi istenir. v1=Vektor(3, 4) yani=> Vektor(3, 4).__add__(v2)
print(v3)
v3 = Vektor(3, 4) + Vektor(1, 2)
print(v3)     # Çikti: Vektor(4, 6)


#3)Method Overriding=ust sinifin methodunu(fonksiyonunu) ezerek kendi davranisini tanimlamasidir.
class Sekil:
    def alan_hesapla(self):
        return "Bilinmeyen sekil alani"
    def tanit(self):
        return "Ben bir sekilim"
class Daire(Sekil):
    def __init__(self, yaricap):
        self.yaricap = yaricap
    def alan_hesapla(self):  # Üst sinif metodu eziyoruz
        return 3.14 * self.yaricap ** 2
    # tanit() metodunu ezmiyoruz, ust siniftan aynen kullanmaya devam ederiz.
class Dikdortgen(Sekil):# Şekil sinifina kalitim yapmak zorunda degil nede olsa 2 methodu da ezmis class Dikdortgen(): seklinde de kullanilabilir.
    def __init__(self, en, boy):
        self.en = en
        self.boy = boy
    def alan_hesapla(self):  # Üst sinif metodu eziyoruz
        return self.en * self.boy
    def tanit(self):  # Üst sinif metodu eziyoruz
        return "Ben bir dikdortgenim"
# Polymorphism kullanimi
sekil_listesi = [Daire(5), Dikdortgen(4, 6), Sekil()]

for sekil in sekil_listesi:
    print(f"{sekil.tanit()}: {sekil.alan_hesapla()}")# Daire(5).tanit() /=/ Dikdortgen(4, 6).tanit() /=/ Sekil().tanit()
    # Daire(5).alan_hesapla() /=/ Dikdortgen(4, 6).alan_hesapla() /=/ Sekil().alan_hesapla()
# Çikti:
# Ben bir sekilim: 78.5
# Ben bir dikdortgenim: 24
# Ben bir sekilim: Bilinmeyen sekil alani


#4)*args ve **kwargs=bir fonksiyona istedigimiz kadar parametre gonderebilmemizi saglar. *args sirali parametreler icin, **kwargs ise anahtar kelime parametreleri icin kullanilir.

def toplayici(*args): #Farkli turde ve sayida argumani toplayan fonksiyon
    sonuc = 0
    for arg in args:
        if isinstance(arg, (int, float)): #isinstance==>soldaki verinin sagdaki turlerden biri olup olmadigini kontrol eder. 1 veya 0 dondurur.
            sonuc += arg
        elif isinstance(arg, str): #Eger arguman(parametre) string ise uzunlugunu ekle
            sonuc += len(arg)  # String'in uzunlugunu ekle
        elif isinstance(arg, list): #Eger arguman(parametre) liste ise icindeki sayilari topla
            sonuc += sum(arg)  # Liste icindeki sayilari topla
    return sonuc

print(toplayici(1, 2, 3))                 # 6
print(toplayici(1, "merhaba", [1, 2, 3])) # 1 + 7 + 6 = 14
print(toplayici("a", "b", "c"))           # 1 + 1 + 1 = 3


#5) functools.singledispatch=bir fonksiyonun farkli turdeki argumanlara gore farkli davranmasini saglar. Bu tek bir fonksiyon adi altinda farkli turler icin ozel islemler tanimlamamiza olanak tanir.
# Her bir veri tipine gore farkli fonksiyonu isleme aliriz.

from functools import singledispatch
#sablon(default) fonksiyon=>@singledispatch ile isaretlenir.
@singledispatch #varsayilan davranistir eger asagidakilere uymayan arguman gelirse bu fonksiyon calisir.Switch-Case yapisindaki default gibi dusunebiliriz.
def bilgi_yazdir(arg):
    print(f"Tip: {type(arg).__name__}, Deger: {arg}")

@bilgi_yazdir.register(int)#eger arguman int turunde ise bu fonksiyon calisir
def _(arg):
    print(f"Tam sayi: {arg} (kupu: {arg**3})")

@bilgi_yazdir.register(str)#eger arguman str turunde ise bu fonksiyon calisir
def _(arg):
    print(f"Metin: '{arg}' (uzunluk: {len(arg)})")

@bilgi_yazdir.register(list)#eger arguman list turunde ise bu fonksiyon calisir
def _(arg):
    print(f"Liste: {arg} (eleman sayisi: {len(arg)})")

@bilgi_yazdir.register(dict)#eger arguman dict turunde ise bu fonksiyon calisir
def _(arg):
    print(f"Sozluk: {arg} (anahtar sayisi: {len(arg)})")

bilgi_yazdir(42)                # Tam sayi: 42 (kupu: 74088)
bilgi_yazdir("Python")           # Metin: 'Python' (uzunluk: 6)
bilgi_yazdir([1, 2, 3])          # Liste: [1, 2, 3] (eleman sayisi: 3)
bilgi_yazdir({"a": 1, "b": 2})   # Sozluk: {'a': 1, 'b': 2} (anahtar sayisi: 2)
bilgi_yazdir(3.14)               # Tip: float, Deger: 3.14 (varsayilan)