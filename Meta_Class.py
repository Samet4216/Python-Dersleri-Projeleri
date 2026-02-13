#NOT:toplama islemi arka planda __add__() methodu ile yapilir a+b ifadesi aslinda a.__add__(b) seklinde calisir
a=4                          #Implement=tasarimi hayata gecirmek
b=7                          #Interface=arayuz
print(a.__add__(b))#11

"----Meta Class----""" #abstruct dekoratoru ozellesmis bir metaclass'tir.
#1)Bir SİHA'nin gorev bilgisayarinda yuzlerce farkli modul (Radar, Lazer, Motor) calisir. Eger bir yazilimci, bu modullerden birini yazarken standartlara uymazsa
#(ornegin shutdown() metodunu yazmayi unutursa), sistem felakete suruklenebilir. Meta siniflar, bu hatayi kod daha calismadan, hatta sinif tanimlanirken yakalar.
#class Drone: yazdiginda tanimladigin o sinif da bellekte yasayan bir nesnedir.Sinifi "Metaclass" olusturur.

#2)Python bir sinif tanimladiginda (class A: ...) arka planda sunu calistirir:
#type(name, bases, attrs)
class Radar:
    pass
Radar = type("Radar", (), {})#arka planda bu calisir


class DenetleyiciMeta(type):#sinif uretme mekanizmasi olan type'dan miras aldik artik type'i override edebiliriz
    def __new__(mcs, name, bases, attrs):#name=sinifin adi    bases=miras aldigi siniflar   attrs=sinifin icindeki degiskenler(dict)
        if "frekans" in attrs:
            if attrs["frekans"] <= 0:#attributes'leri attrs sozlugunde saklariz eger frekans degerimiz negatif gelirse class olusturulmadan hata verir.
                raise ValueError("Frekans pozitif olmali!")
        print(f"{name} sinifi su an yaratiliyor...")
        
        return super().__new__(mcs, name, bases, attrs)

class Radar(metaclass=DenetleyiciMeta):
    frekans=-6 #===> Radar = DenetleyiciMeta("Radar", (), {'__module__': '__main__', '__qualname__': 'Radar', 'frekans': 10})
# cikti: HATA ALIR cunku frekansi negatif deger verdik.
#3)abstruct gorevinde:
class SensorMeta(type):
    registry = []
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if name != "Sensor":#Bizim Sensor sinifimiz metaclass ile SensorMetadan mirasa aldigi icin onu registry(kayit defteri) icine eklememize gerek yok
            mcs.registry.append(cls)#bu yuzden sadece sonradan olusturulanlara registry eklemek icin ismi Sensor olmayana ekle talimati veriyoruz.
        return cls
class Sensor(metaclass=SensorMeta):
    pass
class Radar(Sensor):
    pass
class Lidar(Sensor):
    pass
print(SensorMeta.registry) #[<class '__main__.Radar'>, <class '__main__.Lidar'>]--->registry olan siniflar
"""
1) Python class govdesini okur
2) Metaclass new cagrilir
3) super().new class’i uretir
4) Biz o class’i aliriz
5) Listeye koyariz
"""