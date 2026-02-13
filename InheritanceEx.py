"deneme 13.02.26"
from abc import ABC, abstractmethod
class WeaponSystem(ABC):
    @abstractmethod
    def aim(self):
        pass
    @abstractmethod
    def fire(self):
        pass

class LaserSystem(WeaponSystem):
    def aim(self):
        return f"The laser focused on the target"
    def fire(self):
        pass
print(LaserSystem().aim())
"""
BasePlatform adinda bir ata sinif olustur.
__init__ metodunda seri_no ve max_yuk parametrelerini alsin.
ozellikleri_goster adinda bir metodu olsun.
S_IHA (Silahli IHA) adinda bir sinif olustur ve BasePlatform'dan miras al.
__init__ kisminda super() kullanarak ata sinifi baslat, ek olarak muhimmat_kapasitesi parametresini al.
ates_et adinda bir metodun olsun.
K_IHA (Kesif IHA'si) adinda bir sinif olustur ve BasePlatform'dan miras al.
__init__ kisminda super() kullan, ek olarak kamera_cozunurlugu parametresini al.
goruntu_aktar adinda bir metodun olsun.
"""
class BasePlatform():
    def __init__(self,serial_no,max_load):
        self.serial_no=serial_no
        self.max_load=max_load
    def show_attributes():
        pass
class S_IHA(BasePlatform):
    def __init__(self, serial_no, max_load, ammunition):
        super().__init__(serial_no, max_load)
        self.ammunition = ammunition
    def fire():
        pass
class K_IHA(BasePlatform):
    def __init__(self, serial_no, max_load, resolution):
        super().__init__(serial_no, max_load)
        self.resolution = resolution
    def display_output():
        pass
print(K_IHA(12,34,45).serial_no)