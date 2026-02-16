#1)Composition = Bir sınıfın başka bir sınıfı içinde barındırmasıdır.
class Motor:
    def __init__(self, beygir):
        self.beygir = beygir

    def calistir(self):
        print("Motor calisti")

class Araba:
    def __init__(self, marka, beygir):
        self.marka = marka
        self.motor = Motor(beygir)  # composition

    def araba_calistir(self):
        print(f"{self.marka} araba calisiyor...")
        self.motor.calistir()

araba1 = Araba("Toyota", 150)#içinde iki tane nesne oluşturduğumuz için 2 parametre gonderiyoruz. Marka ve beygir.
araba1.araba_calistir()  # Motor çalıştı ===>print ifadesi olduğu için geriye döndürülen değer yok direk çağrılabilir.
#print(araba1.araba_calistir()) yaparsan da return self.motor.calistir() yazmak gerekir
print(araba1.motor.beygir)  # 150

#2)Eğer üst sınıft yapacağın değişiklik alt sınıfları da etklesin isteniyorsa bu yöntem kullanılır. Bu sayee her değişiklikte yeniden kodları düzenlemekten kurtulunur.
class ElektrikMotor:
    def calistir(self):
        print("Elektrik motor calisti")

class DizelMotor:
    def calistir(self):
        print("Dizel motor calisti")

class Araba:
    def __init__(self, motor):  
        self.motor = motor

    def araba_calistir(self):
        self.motor.calistir() #motoru çalıştır dedik ama iki tane çalıştır fonksiyonu var hangisinin çalışacağını bizim göndereceğimiz parametre belirler
 
Araba(ElektrikMotor()).araba_calistir()#elektrikli motor parametre olarak gönderildiği için elektrik motor çalışır
Araba(DizelMotor()).araba_calistir()#dizel motor parametre olarak gönderildiği için dizel motor çalışır

#3)Strong vs Weak Composition=birbiri içinde tanımlanan sınıflar üst sınıfın silinmesi halinde:
#alt sınıfların da silinmesi(üst ile kuvvetli bir bağı var) strong composition, alt sınıfların silinmemesi(üst sınıftan daha bağımsız) weak composition olarak adlandırılır.
#Strong Composition Örneği:
class Motor:
    def __init__(self, beygir):
        self.beygir = beygir
    def calistir(self):
        print("Motor calisti")  
class Araba:
    def __init__(self, marka, beygir):
        self.marka = marka
        self.motor = Motor(beygir)  # composition;eğer bu Araba sınıfından tanımladığımız nesneyi silersek motor da içinde olduğu için silinecek.
    def araba_calistir(self):
        print(f"{self.marka} araba calisiyor...")
        self.motor.calistir()# ilk fonksiyonun içinde tanımlanmış motor nesnemize erşiştik.
araba1 = Araba("Toyota", 150)
print(araba1.motor.beygir)  # 150   
del araba1  # Araba nesnesini siliyoruz
# print(araba1.motor.beygir)  # Hata: araba1 artık var değil, çünkü silindi. Motor nesnesi de silindi, çünkü Araba sınıfı içinde tanımlanmıştı (weak composition).
#================================================================
#Weak Composition Örneği:
class Motor:
    def __init__(self, beygir):
        self.beygir = beygir
    def calistir(self):
        print("Motor calisti")
class Araba:
    def __init__(self, marka, motor):
        self.marka = marka
        self.motor = motor  # composition; motor nesnesi Araba sınıfının içinde tanımlanmadığı için Araba nesnesi silindiğinde motor nesnesi silinmez.
    def araba_calistir(self):
        print(f"{self.marka} araba calisiyor...")
        self.motor.calistir()
motor1 = Motor(150)  # Motor nesnesi oluşturuluyor
araba1 = Araba("Toyota", motor1)  # Araba nesnesi oluşturuluyor, motor nesnesi parametre olarak gönderiliyor
#araba1 = Araba("Toyota", Motor(150))
print(araba1.motor.beygir)  # 150 
del araba1  # Araba nesnesini siliyoruz
print(motor1.beygir)  # 150; motor nesnesi hala var çünkü weak composition kullanıldı.

#WEAK COMPOSİTİON==Dependency Injection ilişkisi=bir sınıfın ihtiyaç duyduğu bağımlılıkları dışarıdan almasıdır. Bu sayede sınıflar arasındaki bağımlılık azaltılır ve kod daha esnek hale gelir.
"""
class Car:
    def __init__(self):
        self.engine = Engine()  ----strong----Car sınıfı Engine sınıfına bağımlıdır, çünkü kendi içinde bir Engine nesnesi oluşturur. Bu durumda Car sınıfını kullanmak istediğimizde Engine sınıfının da tanımlanmış olması gerekir.

        
class Car:
    def __init__(self, engine):
        self.engine = engine    ----weak----  Car sınıfı Engine sınıfına bağımsdır, ancak bu bağımlılık dışarıdan sağlanır. Bu sayede Car sınıfını kullanmak istediğimizde sadece bir Engine nesnesi sağlamamız yeterlidir, Car sınıfının içinde Engine sınıfının tanımlanmış olması gerekmez.


"""