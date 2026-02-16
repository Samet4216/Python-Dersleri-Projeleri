#Kalitim, bir sinifin ozelliklerini ve metotlarini baska bir sinifa aktarmasidir.
#1)Bir nesnenin ortak ozelliklerini baska bir siniftan alir kendine has ozelliklerini ustune eklersin.
class Platform:  # Ata (Parent) Sinif
    def __init__(self, serial_no):
        self.serial_no = serial_no
        self.energy = "Full"

class IHA(Platform):  # Yavru (Child) Sinif
    def fly(self):
        print(f"{self.seri_no} armed.")

#2)super() Kullanm: Yavru sinifin constructor'nda (__init__), ata sinifin constructor'ni cagirmak için kullanilir.
# Bu, "temel hazirliklar ata sinif yapisina, ben üzerine ekleme yapayim" demektir.
class Platform:
    def __init__(self, seri_no):
        self.seri_no = seri_no
        self.enerji_durumu = "Tam"

    def sistem_durumu(self):
        print(f"{self.seri_no} sistem aktif.")
class IHA(Platform):
    def __init__(self, seri_no, kanat_acikligi):#ekstra eklenecek/degistirilecek parametreler
        super().__init__(seri_no)#Varsayilanlar kalmasini ayrica seri no ve kanat acikligi ekleyecegini bildirmek icin super() kullanilir.
        self.kanat_acikligi = kanat_acikligi


#3)Overriding: Ata sinifta olan bir metodu yavru sinifta ayni isimle tekrar tanimlarsan, yavru sinifin metodu gecerli olur.
class Amminition:
    def ignition(self):
        print("Ammunition was dropped..")

class GuidedMissile(Amminition):
    def ignition(self):  # Overriding
        print("The target was locked on and fired.")

#4)MRO(Method Resolution Order) =Python metod ararken hangi srayla siniflara bakacak? 
class A:
    def selam(self):
        print('A')

class B(A):
    pass

class C(A):
    def selam(self):
        super().selam()

class D(B, C):
    pass

print(D.mro())#cikti= [D, B, C, A, object]

#D-->B'ye gider orada bir cikti yok D geri doneriz -->C'ye gider cikti var selam objesi yazdrir.
#python ilk buldugunu calistirir.

print(D())#sadece obje ciktisi verir ('A' objesi)
print('--------')
D().selam()#C ye geldiginde super() fonksiyonu ile A'ya erisir.D'den A'ya erismek icin selam fonksiyonunu kullaniriz.  

#5)Hiyerarsiyi dogru belirlemelisin. Her SIHA esasnda IHA da olan ozelliklere sahiptir ozel olarak ayrica silah ve muhimmat tasir.Ama her IHA bir SIHA degildir.
#Temel sinifi ve yavru siniflari dogru belirlemelisin.

class HavaAraci: # En temel sinif
    def __init__(self):
        self.havada_mi = False

class Iha(HavaAraci): # Iha, bir HavaAraci'dir.
    def otonom_uc(self):
        pass

class Siha(Iha): # Siha, bir Iha'dr. (Dolaysyla bir HavaAraci'dir)
    def lazer_isaretle(self):
        pass
    def atesle(self):
        pass

class GozcuIha(Iha): # GozcuIha da bir Iha'dr.
    def termal_tara(self):
        pass
#6)Soyut sinifla calisirken,ABC kullanmak için abc modülünden ABC sinif ve @abstractmethod dekoratörünü kullaniriz.
from abc import ABC, abstractmethod#abstract-->soyutlamak

class Sensor(ABC):
    @abstractmethod #eger farkli bir sinif Sensor sinifini miraslarsa veri_oku() fonksiyonuna kesinlikle sahip olmalidir.
    def veri_oku(self):
        pass

#6.2)bu siniftan miras alan alt sinif, o metodu override (iptal edip kendi kodunu yazmak) etmezse, alt siniftan da nesne üretilemez.
class SicaklikSensoru(Sensor):
    def veri_oku(self):
        return 30.2
    
    def veri_yaz(self):
        return 12 
print(SicaklikSensoru().veri_oku())
print(SicaklikSensoru().veri_yaz()) #farkl bir veri_yaz() nesnesi olusturduk istenen veri_oku() kullanidigi icin nesne olusturulamaz.
print(SicaklikSensoru())#istenen veri_oku() fonksiyonuna sahip olmadigi icin hata verir.