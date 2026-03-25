#1)Bir sistemin aynı anda birden fazla işi yapmasıdır.
#Concurrency (Eşzamanlılık): Birden fazla görevin aynı zaman dilimi içinde ilerlemesidir. İşlemci, görevler arasında çok hızlı geçiş yapar.
#--->Tek bir aşçının aynı anda hem çorba karıştırıp hem soğan doğramasıdır.
#Parallelism (Paralellik): Birden fazla görevin tam olarak aynı anda farklı çekirdeklerde (CPU Cores) çalışmasıdır.
#--->İki farklı aşçının iki farklı tencerede yemek yapmasıdır.
#+++Threading+++ Pythonda aynı anda birden fazla iş yapmamıza yarayan modüldür.

import threading
import time

def gorev():
    print("Thread başladı")
    time.sleep(2)
    print("Thread bitti")

t = threading.Thread(target=gorev) #Kullanılacak fonksiyon bizim target parametremiz olacak.

t.start()   #Thread’i başlatır
t.join()    #Bitmesini bekler

#argümanlı:
def hesapla(x):
    print(x *x)

t = threading.Thread(target=hesapla, args=(5,)) #Fonksiyonumuz argüman alıyorsa bunu tuple olarak göndermek zorundayız bu yüzden virgül kuallanılır.
t.start()
t.join()


#2)threading kullanımı:
import threading
import time

def isim_yazdir(isim):
    for i in range(5):
        print(f"Merhaba {isim} - {i}")
        time.sleep(1)

# Thread oluşturur
thread1 = threading.Thread(target=isim_yazdir, args=("Ali",))
thread2 = threading.Thread(target=isim_yazdir, args=("Ayşe",))

# Thread'leri başlatır
thread1.start()
thread2.start()

# Thread'lerin bitmesini bekler
thread1.join()
thread2.join()

print("Tüm thread'ler tamamlandı!")
#===================================================================================================
#2+ eş zamanlı işlemde işini önce bitiren dışarıya ilk çıktıyı verir.
import threading
import time

def gorev(num):
    print(f"Thread {num} basladi")
    time.sleep(1)
    print(f"Thread {num} bitti")

threads = []#hazır kuyrukta beklesin bu liste içinde biz sonradan o threadları çalıştıralım istiyoruz.

for i in range(5):
    t = threading.Thread(target=gorev, args=(i,))#thread objesi oluşturulur.
    t.start()#yeni bir thread gönderebileceiği sinyalini yollar yani thread1 giderken arkasına thread2 başlatılır hemen
    threads.append(t)

for t in threads:
    t.join()#bütün threadlar bitene kadar bekler.Yani ilk girenin işlemini bitirmesinibekler ikinciyi göndermeden önce

"""
---ilk deneme---
Thread 0 basladi
Thread 1 basladi
Thread 2 basladi
Thread 3 basladi
Thread 4 basladi

=====BU NOKTAYA KADAR HEPSİ AYNI ZAMAN DİLİMİNDE SİSTEME GİRER AMA HANGİSİ MİLİSANİYE ÖNCE İŞLEME ALINIRSA İLK O ÇIKAR====

Thread 4 bitti ===BU HEPSİNDEN ÖNCE İŞLEME ALINMIŞ VE JOİN 4 BİTİNCE SIRADAKİ 2.Yİ BİTİRİR.
Thread 2 bitti
Thread 1 bitti
Thread 3 bitti
Thread 0 bitti

---ikinci deneme---
Thread 0 basladi
Thread 1 basladi
Thread 2 basladi
Thread 3 basladi
Thread 4 basladi

=====BU NOKTAYA KADAR HEPSİ AYNI ZAMAN DİLİMİNDE SİSTEME GİRER AMA HANGİSİ MİLİSANİYE ÖNCE İŞLEME ALINIRSA İLK O ÇIKAR====

Thread 3 bitti ===BU HEPSİNDEN ÖNCE İŞLEME ALINMIŞ VE JOİN 3. BİTİNCE SIRADAKİ 2. Yİ BİTİRİR.
Thread 2 bitti
Thread 1 bitti
Thread 0 bitti
Thread 4 bitti

---üçüncü deneme---
Thread 0 basladi 
Thread 1 basladi
Thread 2 basladi
Thread 3 basladi
Thread 4 basladi

=====BU NOKTAYA KADAR HEPSİ AYNI ZAMAN DİLİMİNDE SİSTEME GİRER AMA HANGİSİ MİLİSANİYE ÖNCE İŞLEME ALINIRSA İLK O ÇIKAR====


Thread 2 bitti ===BU HEPSİNDEN ÖNCE İŞLEME ALINMIŞ VE JOİN 2. BİTİNCE SIRADAKİ 1. Yİ BİTİRİR.
Thread 1 bitti
Thread 4 bitti
Thread 3 bitti
Thread 0 bitti

tamamen rastegelelik esaslıdır hangi thread milisaniyelik farkla önce girerse ilk o çıkar
"""

#CPU-bound işlerde threading hız kazandırmaz.I/O-bound(input/output) işlerde işe yarar.programın dış dünya ile konuştuğu kısımlar:
"""
I/O-bound işler:===THREADİNG===
Dosya okuma / yazma
Veritabanı sorgusu
API isteği (HTTP request)  #örneğin sunucuya isstek gönderince cevap beklerken farklı bir sekme(sunucu) açıp oraya da istek göndermek gibi
Sensörden veri bekleme
Ağ üzerinden veri alma
"""
"""
CPU-bound işler:===MULTİPROCESSİNG===
Görüntü işleme
Şifre çözme
Büyük matris hesapları

GIL = Global Interpreter Lock bizim elimizde ağır işlemleri çözen böyle bir anahtar eleman var eğer işlem çok ağırsa tek bir GIL'i o işleme veririz.
thread kullanmadan 2 saniyeden 5 problem 10 saniye sürüyorsa thread ile de aynı sürer çünkü GIL tek bir görevde.Küçük işleri python ilisaniyelik farkla yaptığı için sanki eş zamanlı yapıyor izlenimi verir.
misal 2 saniyeden 5 sunucuya istek attık.Bu 2 saniyenin 1.999 saniyesi bekleme.Yani sen isteği gönderiyorsun → sunucu cevap verene kadar boş bekliyorsun.
CPU o sırada neredeyse hiçbir şey yapmıyor.I/o işlerde thread kullanımı bu bekleme süresini süpürüp 2 saniyeye yakın işin bitmesini sağlar.

multiprocessing=bu işleri aynı bellek alanıyla yapamazsın 2 farklı bellek alanına ihtiyacın var yani basitçe 2 farklı aşçıya ihtiyacımız var.
"""
#3)Jitter=Bir işlemin beklenen zamandan sapmasıdır.Bunu önlemek için Lock kullanılabilir.
#Lock = paylaşılan veriyi koruma mekanizması.Yani bize ilk giren veri işlenene kadar kapıyı kilitleme veri işlemden çıkınca kapıyı açma imkanı sağlar.
#Birden fazla thread aynı anda aynı değişkene erişmeye çalıştığında yarış durumu (race condition) oluşur. Lock, bu sorunu önler:

lock = threading.Lock()#kilit objesi oluşturur.

def arttir():
    global counter
    for _ in range(1000000):
        with lock:
            counter += 1  #sadece 1 thread alır ve işlemi yapıp dışarı çıkartır.           
            
            
            
            # Lock OLMADAN - YANLIŞ sonuç verir:
            
            #counter = 0
            
            # Thread 1 ve Thread 2 aynı anda çalışırsa:
            # Her ikisi de counter=0 okur, 1 ekler, 1 yazar
            # Sonuç: 2 yerine 1 olur 
            
            # Lock İLE - DOĞRU sonuç verir:  
            
            #counter = 0
            
            # Lock sayesinde sırayla çalışır:
            # Thread 1: 0→1, Thread 2: 1→2
            # Sonuç: 2 
counter = 0
t1 = threading.Thread(target=arttir)
t2 = threading.Thread(target=arttir)
t1.start()
t2.start()
t1.join()
t2.join()
print(f"Lock ile sonuç: {counter}")  # Beklenen: 2000000

print("\n" + "="*50)
print("LOCK OLMADAN ORNEK (Race Condition):")
print("="*50 + "\n")

# Lock OLMADAN - Yarış durumu oluşur
def arttir_locksuz():
    global counter2
    for _ in range(1000000):
        counter2 += 1  # Burada kilit yok, race condition oluşacak

counter2 = 0
t3 = threading.Thread(target=arttir_locksuz)
t4 = threading.Thread(target=arttir_locksuz)
t3.start()
t4.start()
t3.join()
t4.join()
print(f"Lock olmadan sonuc: {counter2}")  # Beklenen: 2000000, gerçek: ~1500000 gibi yanlış sonuç
#=====================================================================================================

#4)Deamon() fonksiyonu ile bir threada arka plan olma görevi atayabiliriz:


import threading
import time

def arkaplan_gorevi():
    """Sürekli çalışan arka plan görevi"""
    sayac = 0
    while True:
        sayac += 1
        print(f"Arka plan işlemi çalışıyor... ({sayac})")
        time.sleep(1)

def ana_gorev():
    """Ana thread'in yapacağı iş"""
    print("Ana görev başladı")
    for i in range(5):
        print(f"Ana görev: {i}. adım")
        time.sleep(1)
    print("Ana görev bitti!")

# Daemon thread oluştur
arkaplan = threading.Thread(target=arkaplan_gorevi)
arkaplan.daemon = True 

# Ana thread
ana = threading.Thread(target=ana_gorev)

# Başlat
arkaplan.start()
ana.start()

# Ana thread'in bitmesini bekle
ana.join()

# Program burada bitecek, daemon thread otomatik kapanacak
print("Program sonlandı!")