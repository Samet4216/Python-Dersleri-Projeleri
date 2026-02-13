"""13.02.26
SensorStream adinda bir sinif olustur.
__init__ metodunda bir veri listesi (data_list) ve bir threshold (esik deger) alsin.
Custom Iterator Uygula:
__next__ metodu her cagrildiginda listedeki bir sonraki veriyi kontrol etsin.
Eger veri threshold degerinden kucukse bu gurultudur; onu atlasin ve bir sonraki gecerli veriyi bulana kadar devam etsin.
Liste bittiginde StopIteration firlatsin.
Sinif icinde o ana kadar kac adet "gecerli" veri donduruldugunu takip eden bir sayac tut.
"""
class SensorStream():
    def __init__(self, data_list, threshold):
        self.data_list = data_list
        self.threshold = threshold
        self.index = 0  #guncel konum
        self.sayac = 0  #kac adet gecerli var?

    def __iter__(self):
        return self
    
    def __next__(self):
        while self.index < len(self.data_list):
            veri = self.data_list[self.index]
            self.index += 1 
            #eger veri threshold'dan buyuk veya esitse gecerlidir
            if veri >= self.threshold:
                self.sayac += 1
                return veri
        raise StopIteration

sensor = SensorStream([1, 5, 3, 10, 2, 3, 21], threshold=5)
print("Gecerli veriler (threshold 5 icin):")
for veri in sensor:
    print(f"Veri: {veri} Toplam gecerli veri sayisi: {sensor.sayac}")
