"""01.02.26-12.02.26
Drone adinda bir sinif olustur.
Class Attributes:
drone_count: Uretilen her drone ile 1 artan bir sayac.
operation_code: Tüm filo icin ayni olan bir string (Örn: "ZEYTİN_DALI").
Instance Attributes:
unit_id: Her drone'a ozel bir kimlik.
Metotlar:
__init__: Her yeni drone eklendiginde drone_count'u artirmali.
get_fleet_info: Toplam drone sayisini ve operasyon kodunu döndüren bir instance method.
"""

class drone:
    drone_count = 0
    operation_code = "ZEYTİN_DALI" 
    def __init__(self,id):
        drone.drone_count +=1 #drone_countun alindigi yeri bildirmek icin drone.drone_count kullanilir.
        self.id=id
    def unit_id(self):
        return self.id[:3].upper()
    def get_fleet_into(self):
        return f"The total number of drones is {drone.drone_count}"
    #disaridan drone_count almiyoruz ama f-stringde belirtirken ust classta oldugu bildirilir.

t1=drone("turkiye42")
t2=drone("konya123")
t3=drone("ankara789")
print(t1.unit_id())
print(t1.get_fleet_into())