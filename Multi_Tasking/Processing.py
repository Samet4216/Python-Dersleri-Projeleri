"""
1)Her process'in kendine ait:
Bellek alanı (heap, stack)--Değişkenler (global ve local)--Açık dosya tanımlayıcıları (file descriptors)--Çalışma durumu (registerlar, program sayacı) vardır.
Process birbirinden izole edilmiş bir çalışma ortamıdır. 

Multi-processing, birden fazla process'in aynı anda (paralel olarak) çalıştırılmasıdır.
Her process kendi Python yorumlayıcısına ve dolayısıyla kendi GIL'ine (Global Interpreter Lock) sahiptir.

Bir ana process (parent process) başlatılır.multiprocessing modülü ile yeni process'ler (child process) oluşturulur.
İşletim sistemi, bu process'leri farklı CPU çekirdeklerine dağıtarak aynı anda çalışmalarını sağlar.
NEGATİF YÖNLERİ:
Process'ler arası iletişim (IPC) zorluğu: Veri paylaşmak için özel mekanizmalar (Queue, Pipe, shared memory) kullanmak gerekir. Bu mekanizmalar threading'deki paylaşımlı belleğe göre daha yavaş ve karmaşıktır.
"""

import multiprocessing
import os

def worker(name):
    """Çalışan fonksiyon"""
    print(f"Merhaba, ben {name}, PID: {os.getpid()}")

if __name__ == "__main__":# Eğer dosya çalıştırılıyorsa kodlar işlensin ama yok dosya import ediliyorsa yani dışarıdan çağrılıyorsa çalışmasın istenir.Eğer bu koruma olmazsa, process oluşturma kodu sonsuz döngüye girer.
    # Process oluştur
    p1 = multiprocessing.Process(target=worker, args=("Ali",))
    p2 = multiprocessing.Process(target=worker, args=("Veli",))
    # Başlat
    p1.start()
    p2.start()
    # Bitmesini bekle
    p1.join()
    p2.join()
    print("Ana process bitti.")

#2)Process Havuzu (Pool):
from multiprocessing import Pool
import time
def kare_al(sayi):
    time.sleep(1)  
    return sayi * sayi
if __name__ == "__main__":
    sayilar = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # 4 işçi process içeren bir havuz oluştur
    with Pool(processes=4) as pool:
        # map fonksiyonu ile tüm sayıları işçilere dağıt
        sonuclar = pool.map(kare_al, sayilar)
    print(sonuclar)

#3)Process'ler Arası İletişim (IPC):
#a) Queue (Kuyruk):
from multiprocessing import Process, Queue

def uretici(queue):
    for i in range(5):
        queue.put(i)#gönderme işlemi
        print(f"Üretici: {i} koydu")
    queue.put(None)  # bitiş sinyali

def tuketici(queue):
    while True:
        veri = queue.get()#alma işlemi
        if veri is None:
            break
        print(f"Tuketici: {veri} aldi")

if __name__ == "__main__":
    q = Queue()
    p1 = Process(target=uretici, args=(q,))
    p2 = Process(target=tuketici, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()


#b) Pipe (Boru):
from multiprocessing import Process, Pipe

def gonderici(mesaj):
    mesaj.send("Merhaba")
    mesaj.close()

def alici(mesaj):
    veri = mesaj.recv()
    print(f"Alıcı: {veri} aldı")
    mesaj.close()

if __name__ == "__main__":
    parent_mesaj, child_mesaj = Pipe()
    p1 = Process(target=gonderici, args=(parent_mesaj,))
    p2 = Process(target=alici, args=(child_mesaj,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

#4)Senkronizasyon (Lock):

from multiprocessing import Process, Lock

def yazici(lock, isim):
    with lock:
        print(f"{isim} başladı")
        print(f"{isim} bitti")

if __name__ == "__main__":
    lock = Lock()
    processler = []#join kullanımı için
    for i in range(5):
        p = Process(target=yazici, args=(lock, f"Process-{i}"))
        processler.append(p)#join kullanımı için
        p.start()

    for p in processler:
        p.join()#bütün process'lere join uygular
"""
Process-0 başladı
Process-1 başladı
Process-0 bitti
Process-2 başladı
Process-1 bitti
# KARMAŞIK ÇIKTI 


Process-0 bitti
Process-1 başladı
Process-1 bitti
Process-2 başladı
Process-2 bitti
# DÜZENLİ ÇIKTI
"""

#5)Görüntü İşleme (CPU-bound):Diyelim ki 1000 tane büyük boyutlu resmi yeniden boyutlandıracaksınız. Tek process ile saatler sürebilir. Multiprocessing ile işlemi hızlandırabilirsiniz:
from multiprocessing import Pool
from PIL import Image
import os

def resim_boyutlandir(dosya_adi):
    img = Image.open(dosya_adi)
    img = img.resize((800, 600))
    img.save("kucuk_" + dosya_adi)
    return dosya_adi

if __name__ == "__main__":
    dosyalar = [f for f in os.listdir() if f.endswith(".jpg")]#mevcut dizinde jpg uzantılı dosyaları toplar.
    with Pool() as pool:
        pool.map(resim_boyutlandir, dosyalar)