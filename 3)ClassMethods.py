"""01.02.26-12.02.26
Dogrudan koordinat olarak (x, y, z).
Sifreli bir telsiz mesaji olarak (Format: "ID101_X500_Y200_Z1000").
Görev:
Target adinda bir sinif olustur.
__init__ metodu sadece target_id, x, y ve z degerlerini alsin.
Class Method: from_radio_signal(cls, signal_string) adinda bir metot yaz. Bu metot, yukaridaki formatta gelen string'i parcalasin ve yeni bir Target nesnesi döndürsün.
Class Attribute: total_targets adinda bir sayac tut ve her nesne uretildiginde artir.
"""
class target:
    total=0
    def __init__(self,target_id,x,y,z):
        self.target_id = target_id.lower()
        self.x = x
        self.y = y
        self.z = z
        target.total += 1
    @classmethod
    def from_radio_signal(cls, signal_string):
        return signal_string.lower()
    
target1=target("SAKJD_ASNID2_28DJDK",45,67,89)
target2=target("ASDKO_2JWS0A_SAIGA1",356,27,189)
target3=target("NSJ34_NJD24_DDSI12",325,7,349)

print(target1.total)
print(target2.target_id)
print(target3.x)