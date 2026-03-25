#1)Dekoratorler; mevcut bir fonksiyonun veya metodun davranisini, onun kaynak kodunu degistirmeden genisletmenize veya degistirmenize olanak taniyan bir aractir. 
#Dekoratorler, fonksiyonlari sarmalayarak (wrap) onlarin calismasindan once veya sonra ek islemler yapilmasini saglar.
"""
Pythonda fonksiyonlar:
-)Fonksiyonlar degiskenlere atanabilir:
def selamla():
    print("Merhaba")
selam = selamla ----------selam adinda yeni bir degisken olusturduk ve selamla fonksiyonunu atadik.
selam() #Merhaba ---------selam() fonksiyonunu cagirinca aslinda selamla() fonksiyonu cagrilir.

-)Fonksiyonlar baska fonksiyonlara arguman olarak gecirilebilir:
def selamla():
    print("Merhaba")
def fonksiyon_cagir(func):
    func() 
fonksiyon_cagir(selamla) #Merhaba ---------fonksiyon_cagir() fonksiyonunu cagirirken selamla fonksiyonunu arguman olarak gonderdik ve fonksiyon_cagir() fonksiyonu icinde func() cagrildiginda aslinda selamla() fonksiyonu cagrilir.   

-)Fonksiyonlar baska fonksiyonlarin icinde tanimlanabilir:
def dis_fonksiyon(): 
    def ic_fonksiyon():
        print("Merhaba")
    ic_fonksiyon()------>dis_fonksiyon() cagrildiginda ic_fonksiyon() cagiran komut satiri.
dis_fonksiyon() #Merhaba ---------dis_fonksiyon() cagrildiginda ic_fonksiyon() cagrilir ve Merhaba yazdirilir.

-)Fonksiyonlar baska fonksiyonlardan deger dondurebilir:
def dis_fonksiyon():
    def ic_fonksiyon():
        return "Merhaba"
    return ic_fonksiyon() ----------dis_fonksiyon() cagrildiginda ic_fonksiyon() cagrilir ve Merhaba degeri doner.

(deger dondurdugu icin print ile yazdirabiliriz)
print(dis_fonksiyon()) #Merhaba ---------dis_fonksiyon() cagrildiginda ic_fonksiyon() cagrilir ve Merhaba degeri doner ve print ile yazdirilir.
"""

#2) @ isareti ile dekorator tanimlanir:
def dekorator(func):# func fonksiyonunu disaridan alacagimizi belirtiriz.
    def wrapper():
        print("Fonksiyon cagrilmadan onceki islem")
        func() #func() cagrildiginda aslinda dekoratorun arguman olarak aldigi fonksiyon cagrilir.
        print("Fonksiyon cagrildiktan sonraki islem")
    return wrapper

@dekorator #dekoratorun arguman olarak alacagi fonksiyonun ustune @dekorator yazilir.
def selamla():
    print("Merhaba")
selamla()   #Fonksiyon cagrilmadan onceki islem
            #Merhaba
            #Fonksiyon cagrildiktan sonraki islem 
dekorator(selamla) # fonksiyonunu cagirarak da ayni sonucu elde edebiliriz.

#3) Arguman Alan Fonksiyonlari Dekore Etmek:
def dekorator(func):
    print("Dekorator fonksiyonu cagrildi") #dekorator fonksiyonu cagrildiginda bu satir yazdirilir.
    def wrapper(*args, **kwargs): #*args ve **kwargs kullanarak dekoratorun arguman olarak alacagi fonksiyonun herhangi bir sayida ve turde arguman alabilecegini belirtiriz.
        print("Fonksiyon cagrilmadan onceki islem")
        func(*args, **kwargs)
        print("Fonksiyon cagrildiktan sonraki islem")
    return wrapper # geri deger dondermek zorundayiz. Bu sayede dekorator fonksiyonu cagirilinca geriye wrapper fonksiyonunu dondurur.
@dekorator
def topla(a, b):
    print(f"{a} + {b} = {a+b}")
topla(3, 5) #Fonksiyon cagrilmadan onceki islem
            #3 + 5 = 8
            #Fonksiyon cagrildiktan sonraki islem 
"""
@unlem_ekle
@buyuk_harf
def mesaj():
============Ayni Seydir==============
mesaj = unlem_ekle(buyuk_harf(mesaj)) 
"""
def plus_one(number):
    def add_one(number):
        return number + 1
    result = add_one(number)
    return result

print(plus_one(4)) #5