#1)Bir nesnenin uzerinde tek tek dolasabiliyorsan, o nesne iterable’dir.
#Bir nesnenin iterable olmasi icin icinde __iter__() metodu olmali.Bu metod bir iterator dondurur.
#Iterable = uzerinde dolasilabilir sey     Iterator = dolasma islemini yapan sey

nums = [1,2,3]#nums= bir itreable nesnedir
it = iter(nums)
print(next(it))
print(next(it))#it= bir iteratordur
print(next(it))
#print(next(it))#Eger donecek eleman kalmadiysa StopIteration hatasi firlatir.

#2)map fonksiuyonu islem yapmak icin bir iterable nesne bekler.
nums = [1,2,3]
result = map(lambda x: x*2, nums)#result= iterable bir objedir.

#3)any/all itreable ustunde calisir
nums = [0,1,2]
print(any(nums))  # en az bir True var mi?
print(all(nums))  # hepsi True mu?

#4)unpacking=pythonun listeyi itrable olarak kullanip sirayla veri cekmesidir.
a, b, c = [1,2,3]
a, *rest = [1,2,3,4]# a sadece ilk elemani alir kalan elemanlar liste halinde rest degiskeninde saklanir.
print(rest)

#5)enumerate ile index,value verir
for i, val in enumerate([10,20,30]):
    print(i, val)#0 10
                 #1 20
                 #2 30

#6)Custom iterator yapimi:
#State (durum) tutmak
class CiftSayilar:
    def __init__(self, max_deger):#max deger sinir ve current deger suanki degerimiz
        self.max = max_deger
        self.current = 0

#__iter__() yazmak
    def __iter__(self):
        return self#objemizin kendisinin iterator oldugunu belirtir
    """
    class CiftSayilar:
    def __init__(self, max_deger):
        self.max = max_deger

    def __iter__(self):
        return CiftSayilarIterator(self.max) -------- 2 parcaya ayirdik iteratorumuzun belirtilen fonksiyon(CiftSayilarIterator(self.max)) oldugunu bildirdilk.


    class CiftSayilarIterator:
        def __init__(self, max_deger):
            self.max = max_deger
            self.current = 0

        def __iter__(self):
            return self ---------bu fonksiyonun iterator oldugunu yeniden tastikledik

        def __next__(self):
            if self.current <= self.max:
                val = self.current
                self.current += 2
                return val
            else:
                raise StopIteration

    """
#__next__() yazmak
    def __next__(self):
        if self.current <= self.max:#eger siniri gecmediysek suanki durumu val icine at ve suanki durumu 1 arttir.
            val = self.current
            self.current += 1
            return val
        else:
            raise StopIteration #eger siniri gecersek hata firlat.
