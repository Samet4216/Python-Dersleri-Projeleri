"""13.02.26
FuelTank adinda bir sinif olustur.
__init__ icinde _level (private) degiskenini 100.0 (yuzde) olarak baslat.
level adinda bir property tanimla:
Getter: Mevcut yakiti döndürsün.
Setter: Yeni gelen yakit miktarini kontrol etsin.
Eger yeni miktar, mevcut miktardan buyukse: "HATA: Yakit havada artirilamaz!" uyarisi ver ve islemi yapma (degeri degistirme).
Eger yeni miktar 0'dan kucukse: Yakiti 0'a esitle (Negatif yakit olamaz).
Aksi halde degeri guncelle.
is_critical adinda bir Computed Property (Sadece Getter) ekle.
Eger yakit %10'un altina duserse True, degilse False dondursun.
"""
class FuelTank():
    def __init__(self):
        self._level=100

    @property
    def current_fuel(self):
        return self._level
    @current_fuel.setter
    def current_fuel(self,control_fuel):
        if control_fuel>self._level:
            print("ERROR: Fuel cannot be increased in mid-air!")
        elif control_fuel<0:
            self._level=0
        else:
            self._level=control_fuel
    @property
    def is_critical(self):
        if self._level<=10:
            return True
        else:
            return False

tank = FuelTank()
tank.current_fuel = 10
print(tank.current_fuel)
print(f"Situation: {tank.is_critical}")

    