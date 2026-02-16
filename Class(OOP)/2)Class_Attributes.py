#1)Class Attributes, dogrudan sinifin icine, metotlarin disina tanimlanir. Bu degiskenler o siniftan uretilen tum nesneler icin ortaktir.
class Asker:
    ordu_adi = "TÜRK KARA KUVVETLERİ"  # Class Attribute

    def __init__(self, isim, kilo):
        self.isim = isim
        self.kilo = kilo 

#2)Namespace (Isim Alani): Sinif nitelikleri ClassName.__dict__ icinde tutulurken, instance nitelikleri instance.__dict__ icinde tutulur. 
#Python bir degiskeni ararken once nesneye (-->self.ordu_adi?), bulamazsa sinifa (-->ordu_adi = "TÜRK KARA KUVVETLERİ") bakar.

#3)Tracking (Takip): Belli bir sinifin icinde uretilen nesnelerin sayisini belirlemede kullanilir.

class IHA:
    aktif_iha_sayisi = 0 

    def __init__(self, iha_id):
        self.iha_id = iha_id
        # Her yeni nesne olusturuldugunda sayaci artiriyoruz.
        IHA.aktif_iha_sayisi += 1
        print(f"IHA {self.iha_id} sisteme girdi. Aktif Sayi: {IHA.aktif_iha_sayisi}")

    def __del__(self):
        # Nesne silindiginde (gorev bittiginde) sayaci azaltiyoruz.
        IHA.aktif_iha_sayisi -= 1
        print(f"IHA {self.iha_id} sistemden ayrildi. Kalan Aktif Sayi: {IHA.aktif_iha_sayisi}") 

#NOT:Attribute= iha_id, aktif_iha_sayisi gibi degiskenlerdir. Method= __init__, __del__ gibi fonksiyonlardir.