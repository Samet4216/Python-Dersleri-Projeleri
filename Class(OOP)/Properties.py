#1)Properties, verilerimizin etrafina ordugumuz "akilli koruma kalkanlaridir".Verilerin disaridan degistirilmesini engeller.
#ornegin bir agirlik/uzunluk birimi negatif deger alamaz eger biz korumaya almazsak disaridan yanlislikla bu degerler negatif girilebilir.
class LazerSensor:
    def __init__(self):
        self.mesafe = 0

sensor = LazerSensor()
sensor.mesafe = -50  # Negatif mesafe fizikte mumkun degildir ama kod HATA VERMEDİ-->arka planda sistemsel sorunlar yasanir.
print(sensor.mesafe) # cikti: -50 (Sistem mantiken coktu)

class LazerSensor:
    def __init__(self):
        self._mesafe = 200 #dogru kullanimi bu sekildedir.Boylece disaridan degistirilemez.
sensor.mesafe = -50 #hata verir
print(sensor.mesafe)

#A)Getter: Veriyi okurken calisir.Veriyi disariya servis eder.
#B)Setter: Veriyi degistirirken (atama yaparken) calisir.Disaridan gelen veriyi kontrol ederek iceri alir.kapinin anahtridir.

class LazerSensor:
    def __init__(self):
        # "_" isareti ile bu degiskeni kapsule aliyoruz(ENCAPSULATION)
        self._mesafe = 0 

    #GETTER (Okuma Kismi)
    @property #_mesafe nesnesini sanki normal bir mesafe nesneymis(attribute) gibi cagirmamizi sagladi== print(sensor.mesafe) 
    def mesafe(self):
        print("Veri okunuyor...")
        return self._mesafe

    #SETTER (Yazma Kismi)---->BU KISIM OLMADAN O DEgERİ DEgİsTİREMEZSİN(AttributeError alirsin) SADECE VARSAYILAN DEgERİ OKURSUN
    @mesafe.setter#mesafe ozelligine yazma islemi yaptigimizi @ ile bildiririz.
    def mesafe(self, yeni_deger):
        if yeni_deger < 0:
            print("Mesafe negatif olamaz Deger 0'a sabitlendi.")
            self._mesafe = 0
        elif yeni_deger > 1000:
            print("Sensor menzili asildi Maksimum 1000m girilebilir.")
            self._mesafe = 1000
        else:
            self._mesafe = yeni_deger
            print(f"Mesafe guvenle ayarlandi: {self._mesafe}m")

sensor = LazerSensor()
#Hatali veri gonderme
sensor.mesafe = -200  # cikti:Mesafe negatif olamaz Deger 0'a sabitlendi.
# Dogru veri gonderme
sensor.mesafe = 150   # cikti: Mesafe guvenle ayarlandi: 150m
# Veriyi okuma
print(sensor.mesafe)  # cikti: 150

#2)Eger veriyi setter ile bile degistirmek istemiyorsan yani kapiyi direk ortadan kaldirmak istiyorsa __ kullanilir.
class KaraKutu:
    def __init__(self):
        self.public_veri = "Ucus No: TK1923"     # Herkes gorebilir
        self._korumali = "Pilot: Ahmet"          # Setter ile ayarlanabilir(Tek cizgi)
        self.__cok_gizli = "Koordinat: 41.0082"  # Disaridan dogrudan degistirilemez/erisilemez sabittir(cift cizgi)

kutu = KaraKutu()

# Herkesin gordugu veri
print(kutu.public_veri) # cikti: Ucus No: TK1923
# Tek cizgili veri (Erisebilirsin ama yapmamalisin)
print(kutu._korumali)   # cikti: Pilot: Ahmet
#cift cizgili veri (Hata alirsin)
print(kutu.__cok_gizli) # HATA: 'KaraKutu' object has no attribute '__cok_gizli'


#4)Deleter: Veriyi silerken calisir.
class KaraKutu:
    def __init__(self):
        # Baslangicta gizli verimiz var
        self._gorev_verisi = "Hedef Koordinat: 36.5, 42.1"

    # 1. GETTER (Veriyi Okuma)
    @property
    def veri(self):
        return self._gorev_verisi

    # 2. DELETER (Silme / İmha Etme)
    @veri.deleter
    def veri(self):
        print("ACİL DURUM PROTOKOLu DEVREDE")
        print("Veriler guvenli sekilde temizleniyor...")
        
        # Gercek silme islemini burada biz yapiyoruz
        self._gorev_verisi = None 

iha_kutusu = KaraKutu()

# Veriyi okuyalim
print(f"Mevcut Durum: {iha_kutusu.veri}") # cikti: Hedef Koordinat: 36.5, 42.1

del iha_kutusu.veri 
# cikti: 
# ACİL DURUM PROTOKOLu DEVREDE
# Veriler guvenli sekilde temizleniyor...

# Tekrar okumaya calisalim
print(f"Son Durum: {iha_kutusu.veri}") # cikti: None
