# Python'da bir sınıftan nesne türettiğimizde otomatik olarak çalışan metoda __init__ diyoruz.
# __init__ metodu, sınıfın bir örneği oluşturulduğunda çağrılır ve genellikle nesnenin başlangıç durumunu ayarlamak için kullanılır.
# Eğer bir nesnenin oluşturulma sürecini tamamen kontrol etmek istiyorsan __new__ metodunu override edersin.
#__init__ bloğu içinde yapılan her atama (self.x = 10), Python'ın arkadaki __dict__ isimli sözlüğüne bir girdi ekler.

#1)self parametresi ile nesnenin kendisidir.
#----self.speed = speed----
#dışarıdan gelen speed degerini bu nesnenin icine koy demektir.
class Drone:
    def __init__(self, speed, range_km):
        self.speed = speed
        self.range_km = range_km

#2)Validation(dogrulama):
class Missile:
    def __init__(self, distance, speed):
        if speed <= 0:
            raise ValueError("Speed must be positive")
        self.distance = distance
        self.speed = speed
#if blogu ile disaridan alinan speed degerinin pozitif olup olmadıgı kontrol edilir.

#3)Instance_Methods: dişaridan veri almayan nesnenin ozelliklerine baglidir
class Drone:
    def __init__(self, speed):
        self.speed = speed

    def speed_kmh(self):
        return self.speed * 3.6
#speed_kmh disaridan self dıisinda parametre almasina gerek yoktur kendi verisiyle calisir.
def time_to_impact(self):
    return self.distance / self.speed
t1=time_to_impact(1000,200)
#bizim daha onceden tanimladigimiz ozellikleri kullanma imkani verir.
#fonksiyona parametre verip bir nesnenin icine atmamiz gerekir.
class Drone:
    def __init__(self, speed, distance):
        self.speed = speed
        self.distance = distance

    def speed_kmh(self):
        return self.speed * 3.6

    def time_to_impact(self):
        return self.distance / self.speed
d = Drone(100, 500)
#Eger: --d.speed_kmh()-- bunu cagirirsan 360 döndürür. Eger: --d.time_to_impact()-- bunu cagirirsan 5 döndürür.
