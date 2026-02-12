""" 12.02.26
Muhimmat adinda bir sinif oluştur.
__init__ metodu şu üç parametreyi alsin: seri_no (string), sicaklik (float) ve basinc (float).
Güvenlik Kontrolü (Constraint): * Eğer sicaklik -40 ile +85 derece dişindaysa,Veya basinc 0 ile 1013 hPa dişindaysa,
Bu nesne oluşturulmamali ve bir RuntimeError firlatmali.
Eğer veriler normalse, self.onay_kodu adinda bir değişkene seri_no'nun ilk 3 harfini büyük harf yaparak ata.
"""
class Ammunition:
    def __init__(self,id,temperature,pressure):
        if not ((temperature>=-40 and temperature<=85) and (pressure>=0 and pressure<=1013)):
            raise RuntimeError("Invalid temperature or pressure values") 
        
        self.id=id
        self.temperature=float(temperature)
        self.pressure=float(pressure)
        self.confirmation_code = id[:3].upper()

object=Ammunition("konya123", 25, 1010)
print(object.confirmation_code)
#object nesnesi uzerinden onay_kodu degiskenine erisilir ve ekrana yazdirilir. Cikti: KON

"""12.02.26
Battery adinda bir sinif olustur.
__init__ icinde charge_level (%0-100 arasi) ve is_connected (True/False) ozelliklerini tanimla.
Su Instance Method'lari yaz:
connect_to_charger(): Bataryayi sarja baglar (is_connected = True).
disconnect(): Bataryayi sarjdan ayirir.
charge(amount): Bataryayi belirtilen miktar kadar doldurur. Sarj %100'ü geçemez.
get_status(): Mevcut sarj seviyesini ve bagli olup olmadigini bir string olarak döndürsün.
"""

class Battery:
    def __init__(self,charge_level,is_connected):
        self.charge_level=charge_level
        self.is_connected=is_connected
    def connect_to_charger(self):
        self.is_connected=True
    def disconnect(self):
        self.is_connected=False
    def charge(self, amount):
        if self.is_connected:
            if amount < 0 and self.charge_level + amount > 100:
                raise ValueError("Charge amount must be positive")
            self.charge_level = min(100, self.charge_level + amount)
        else:
            raise RuntimeError("Charge Error: Not Connected")
    def get_status(self):
        return f"Charge Level: {self.charge_level}%, Connected: {self.is_connected}"
    
battary=Battery(50,False)
print(battary.get_status()) #Cikti: Charge Level: 50%, Connected: False
battary.connect_to_charger()
battary.charge(30)
print(battary.get_status()) #Cikti: Charge Level: 80%, Connected: True

""""
  if self.is_connected:
           self.charge_level = min(100, self.charge_level + amount)

yapilabilir. min() fonksiyonu, iki veya daha fazla degeri karsilastirir ve en kucuk olani döndürür.
"""