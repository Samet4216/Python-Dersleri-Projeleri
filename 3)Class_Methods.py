#Instance method'lar nesneyle, Class method'lar ise dogrudan sinifin kendisini degistirir.
#Instance method'lar, nesnenin durumunu degistirebilir veya ona erisebilirken, Class method'lar genellikle sinifin genel durumunu yönetmek veya sinif duzeyinde islemler yapmak icin kullanilir.
#Instance method'lar, nesne olusturulduktan sonra cagrilabilirken, Class method'lar sinif adi üzerinden dogrudan cagrilabilir ve genellikle @classmethod dekoratoru ile tanimlanir.

#1)sinif methodlarinin parametresi cls dir. Dekorator kullanilarak fonksiyonun sinif methodu oldugu belirtilir.
class UAV:
    counter = 0

    def __init__(self):
        self.id = self.generate_id()#biz id belirlerken generate_id() fonksiyonunu cagiririz.

    @classmethod #sinifin icindeki her nesne icin ortaktir.
    def generate_id(cls):
        cls.counter += 1
        return cls.counter #deger dönderdik cunku self.id=   satiri ile id degiskeninin degerini bekliyoruz.
u1 = UAV()
u2 = UAV()
u3 = UAV()
print(u1.id)#cikti 1 olur
print(u3.id)#cikti 3 olur

#2)yanlis formatta gelen verileri duzenleyip fonksiyona parametre olarak gonderir.
class UAV:
    def __init__(self, x, y, altitude):
        self.x = x
        self.y = y
        self.altitude = altitude

    @classmethod
    def from_tuple(cls, coords):
        return cls(*coords) #eger veriler bir tuple icinde geliyorsa o verileri ayristirir ve kullanilabilir parametrelere cevirir ve UAV sinifina gonderir.
        # yildiz(*) isareti coords tuple'ni acmak icin kullanilmistir.  
    @classmethod
    def from_string(cls, data_str):
        x, y, altitude = map(int, data_str.split(","))#gelen verileri birbirinden virgullerle ayirir ve cls ile UAV sinifina kullanilabilir parametreleri gonderir.
        return cls(x, y, altitude)

u = UAV.from_string("120,45,300")
v = UAV.from_tuple((2,4,200)) 
print(u.altitude)
print(v.x)