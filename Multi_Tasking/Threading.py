#==1)THREADİNG KULLANIMI==:
import threading
import time
def gorev_yap(isim, sure):
    print(f"{isim} basladi...")
    time.sleep(sure)  
    print(f"{isim} bitti.")
# Thread'leri olusturuyoruz
t1 = threading.Thread(target=gorev_yap, args=("Gorev-1", 3)) # Target calistirilan fonksiyon, args ise o fonksiyona gonderilen argumanlar.
t2 = threading.Thread(target=gorev_yap, args=("Gorev-2", 4))
# Thread'leri baslatiyoruz
t1.start()
t2.start()
# İlgili thread islemi bitmeden sonraki satira gecmesini engeller
t1.join()
t2.join()
print("Tum gorevler tamamlandi, ana program bitiyor.")


#==2)KENDİ THREAD SINIFIMIZI YAZMAK==:
import threading
class BenimThreadim(threading.Thread):
    def __init__(self, mesaj):
        super().__init__()
        self.mesaj = mesaj
    def run(self):#thread icindeki otomatik run() komutudur.
        print(f"Thread calisiyor: {self.mesaj}")
t1 = BenimThreadim("Merhaba")
t1.start()
t1.join()
t2 = BenimThreadim("Gunaydin")
t2.start()
t2.join()

#==3)EŞ ZAMANLI İŞLEM==:
import threading
import time

def toplama(isim,x,y,sure):
    print(f"{isim} basladi...")
    time.sleep(sure) 
    print(f"{isim} sonucu: {x} + {y} = {x+y}")

def carpma(isim, a, b, sure):
    print(f"{isim} basladi...")
    time.sleep(sure)
    print(f"{isim} sonucu: {a} x {b} = {a * b}")
t1 = threading.Thread(target=toplama, args=("Toplama-1", 2, 3, 2))
t2 = threading.Thread(target=toplama, args=("Toplama-2", 4, 5, 3))
t3 = threading.Thread(target=carpma, args=("Çarpma-1", 5, 7, 1))#en kisa sure bittigi icin(1 saniye) ilk ekrana yazilir
t1.start()
t2.start()
t3.start()
t1.join()
t2.join()
t3.join()


