"""16.02.26
Bir IKA (Insansiz Kara Araci) tasarliyorsun. Bu arac farkli catisma ortamlarina gore uzerine farkli silah kuleleri takabiliyor.
1. Asama: Polimorfizm (Silah Arayuzu)
SilahSistemi adinda bir temel sinif (Base Class) olustur.
Bu sinifin ates_et() adinda bir metodu olsun.
Bu siniftan tureyen 3 farkli silah alt sinifi yaz:
MakineliTufek: Ateslendiginde "Tak-tak-tak! 7.62mm mermi atildi." yazsin.
FuzeSistemi: Ateslendiginde "Isi gudumlu fuze firlatildi! Hedef kilitli." yazsin.
ElektronikHarp: Ateslendiginde "Frekans karistirma baslatildi. Sinyaller kesildi." yazsin.
2. Asama: Kompozisyon (İKA Govdesi)
KaraAraci sinifi olustur.
Bu arac sunlara sahip (Composition) olmali:
Bir batarya_seviyesi (int: 0-100 arasi).
Bir takili_silah (Yukaridaki polimorfik siniflardan biri).
Aracta gorev_icra_et() metodu olsun.
3. Asama: Muhendislik Kisiti
gorev_icra_et() metodu cagrildiginda, arac once Batarya Kontrolu yapmali.
Eger batarya %20'nin altindaysa hicbir silah ateslenemez, "Dusuk batarya! Guvenlik moduna gecildi." uyarisi vermeli.
Eger batarya yeterliyse, takili olan silahin ates_et() metodunu tetiklemeli.
Senden Bekledigim Cikti=
Kodun su sekilde bir senaryoyu calistirmali:
Araca once MakineliTufek tak ve batarya %50 iken ates et.
Araca sonra ElektronikHarp tak ve batarya %10 iken ates etmeyi dene (Hata vermeli).
Bataryayi %100 yap ve tekrar ates et.
"""
class WeaponSystem:
    def fire(self):
        pass
class MachineGun(WeaponSystem):
    def fire(self):
        print("Tap-tap-tap! A 7.62mm bullet was fired.")
class MissileSystem(WeaponSystem):
    def fire(self):
        print("Heat-seeking missile launched! Target locked.")
class ElectronicWarfare(WeaponSystem):
    def fire(self):
        print("Frequency scrambling initiated. Signals disrupted.")
class LandVehicle:
    def __init__(self, battery_level, equipped_weapon):
        self.battery_level = battery_level
        self.equipped_weapon = equipped_weapon
    def perform_mission(self):
        if self.battery_level < 20:
            print("Low battery! Entering safety mode.")
        else:
            self.equipped_weapon.fire() #equipped_weapon=> belirtilen silaha gire fire() modulu calistirilir.
# Senaryo
vehicle= LandVehicle(50, MachineGun())
vehicle.perform_mission()  # Tap-tap-tap! A 7.62mm bullet was fired.
vehicle.equipped_weapon = ElectronicWarfare()  # Elektronik Harp sistemini takiyoruz elle manuel olarak degistirdik.
#LandVehicle(50, ElectronicWarfare()) sunu yapiyoruz yani bir nevi

vehicle.battery_level = 10  # LandVehicle(10, MachineGun()) gibi ayarlama yapiyoruz.

vehicle.perform_mission()  # Low battery! Entering safety mode. LandVehicle(50, MachineGun()).perform_mission() fonksiyonunu cagirdigimizda batarya seviyesi 10 oldugu icin silah ateslenemez ve dusuk batarya uyarisi verir.

vehicle.battery_level = 100  # Batarya seviyesini %100 yapiyoruz
vehicle.perform_mission()  # Frequency scrambling initiated. Signals disrupted.
