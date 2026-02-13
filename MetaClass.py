"""13.02.26
Senaryo:
Bir "Gorev Bilgisayari" (Mission Computer) icin moduller yaziliyor. Sistemin guvenligi icin iki kesin kuralimiz var:
Her modul sinifinin isminin sonunda _Module eki olmak zorundadir (orn: Navigation_Module gecerli, Navigation gecersiz). Bu, kod okunabilirligi ve standartlar icin kritiktir.
Her modulun icinde mutlaka emergency_stop adinda bir metot tanimlanmis olmalidir.
Gorev:
MissionComplianceMeta adinda bir meta sinif yaz.
__new__ metodunu kullanarak yukaridaki iki kurali denetle.
Eger sinif ismi _Module ile bitmiyorsa TypeError firlat.
Eger attrs sozlugunde emergency_stop yoksa TypeError firlat.
Bu meta sinifi kullanan iki ornek sinif yaz:
Weapon_Module: Kurallara uysun (Gecerli).
RadarSystem: Kurallara uymasin (Hata versin).
"""

class MissionComplianceMeta(type):
    def __new__(mcs, name, bases, attrs):
        if not name.endswith("_Module"):
            raise TypeError("Class name must end with '_Module'")
        if "emergency_stop" not in attrs:
            raise TypeError("Class must define an 'emergency_stop' method")
        return super().__new__(mcs, name, bases, attrs)

class Weapon_Module(metaclass=MissionComplianceMeta):
    def emergency_stop(self):
        print("Emergency stop activated!")

class RadarSystem(metaclass=MissionComplianceMeta):#eger boyle bir sinif tanimlarsak hata aliriz.
    pass

print(Weapon_Module().emergency_stop()) #Bu gecerli bir sinif oldugu icin calisir ve "Emergency stop activated!" ciktisini verir.
print(RadarSystem()) #Bu sinif gecerli olmadigi icin TypeError firlatir ve "Class name must end with '_Module'" hatasini verir. 