#1)Asyncio, Python’da asenkron (non-blocking) Input/Output islemleri yonetmek icin kullanilan standart kutuphanedir. CPU’yu paralel kullandirmaz. 
#Thread degildir. Process degildir. Tek thread uzerinde, bir event loop ile calisir. Bekleme suresi kullanilarak zamandan kazanc saglanir.
#Eger gorev bekleme durumuna gecerse (await), kontrol event loop’a geri doner ve diger gorevler calismaya devam eder. Boylece bekleme suresi boyunca CPU bosta kalmaz.
import asyncio

async def gorev(isim):
    print(f"{isim} basladi")
    await asyncio.sleep(2) # Normal time.sleep() gibi bloklama yapmaz kontrolu loop'a verir.
    print(f"{isim} bitti")

async def main(): # Özel tanimli (continued) bir fonksiyondur.
    await asyncio.gather( # Await=> bu noktada bekliyorum programi loop al komutu verir.
        gorev("A"),  #gather=>birden fazla gorev varsa hepsini tek bir await ile bekleyebiliriz.
        gorev("B"),
        gorev("C")
    )

asyncio.run(main())# Çalistiracagimiz fonksiyon icinde asenkron calisacak fonksiyonlari gather ile tanimla. 
# Agir islemlerde kullanilirsa bloklama yapar:
# Goruntu isleme (OpenCV heavy compute)
# Makine ogrenmesi egitim
# Buyuk matematik hesaplari

#============SENKRON KULLANIM=============
import time

def telemetri_al():
    print("Telemetri bekleniyor...")
    time.sleep(2)  
    print("Telemetri alindi.")

def radar_tara():
    print("Radar taramasi yapiliyor...")
    time.sleep(1)
    print("Radar temiz.")

def main():
    start = time.time()
    telemetri_al()
    radar_tara()
    print(f"Toplam Sure: {time.time() - start:.2f} saniye")

main()# Çikti: Toplam Sure: 3.00 saniye (Sirayla yapti, zaman kaybi buyuk)

#============ASENKRON KULLANIM=============
import asyncio

async def telemetri_al():
    print("Telemetri bekleniyor...")
    await asyncio.sleep(2) 
    print("Telemetri alindi.")

async def radar_tara():
    print("Radar taramasi yapiliyor...")
    await asyncio.sleep(1)
    print("Radar temiz.")

async def main():
    start = time.time()
    await asyncio.gather(telemetri_al(), radar_tara())# gather icine parametre olarak yapilacak fonksiyonlar gonderilir.
    print(f"Toplam Sure: {time.time() - start:.2f} saniye")

# Bunu yazmak gerekli degildir ama anlami sadece bu dosya calistirilirsa kodu calistir eger kutuphane olarak cagirilirsa calistirma demektir.
if __name__ == "__main__":
    asyncio.run(main()) # Çikti: Toplam Sure: 2.00 saniye

#2) Bazen yeterince beklenirse veri zaman asimina ugrayabilir bunun icin bu kutuphaneye timeout ekleyebiliriz(wait_for() fonksiyonu ile). Eger veri belirtilen sure icinde gelmezse TimeoutError firlatiriz.:
import asyncio
import random

async def lidar_verisi_oku():
    gecikme = random.choice([0.5, 5]) #Rastgele gecikme uretir
    await asyncio.sleep(gecikme)
    return {"mesafe": 120}

async def ana_kontrol_dongusu():
    try:
        # Eger veri 1.0 saniye icinde gelmezse TimeoutError firlatir
        veri = await asyncio.wait_for(lidar_verisi_oku(), timeout=1.0)
        print(f"Lidar verisi alindi: {veri}")
    except asyncio.TimeoutError:
        print("KRİTİK HATA: Lidar zaman asimina ugradi Yedek sensore geciliyor...")

# Çalistir
asyncio.run(ana_kontrol_dongusu())

#3)Producer-Consumer (Üretici-Tuketici Kuyrugu):Bir taraf (Producer) surekli veriyi kuyruga atar, diger taraf (Consumer) kuyruktan alip isler. Aralarinda "buffer" (tampon bolge) olur.
# Bu sayede birbirlerini beklemeden veri basmak yerine once veriyi alir sonra islerler.
#asyncio.Queue--- kullanilir:
import asyncio
import random

async def veri_okuyucu_uart(q):
    """Producer: Seri porttan veriyi okur ve kuyruga atar."""
    while True:
        data = f"Paket_{random.randint(10,20)}"
        # Kuyruga at (put)
        await q.put(data) 
        print(f"[UART] Veri geldi ve kuyruga atildi: {data}")
        await asyncio.sleep(0.5) # Veri akis hizi

async def veri_isleyici_gui(q):
    """Consumer: Kuyruktan veriyi alir ve ekrana basar."""
    while True:
        # Kuyruktan al (get) - Eger kuyruk bossa burada bekler, hata vermez
        veri = await q.get()
        print(f" [GUI] Arayuz guncellendi: {veri}")
        # İsin bittigini bildir
        q.task_done()
        await asyncio.sleep(1) # İsleme hizi (Daha yavas olsa bile veri kaybolmaz, kuyrukta bekler)

async def main():
    # Kuyruk (Buffer) olusturuyoruz
    kuyruk = asyncio.Queue(maxsize=10) # En fazla 10 paket tutsun, tasmasin.
    # İki gorevi de tampon bolgede (buffer/kuyruk) birlestirip calistiriyoruz
    task1 = asyncio.create_task(veri_okuyucu_uart(kuyruk))
    task2 = asyncio.create_task(veri_isleyici_gui(kuyruk))
    
    # return_exceptions=True herhangi bir hata alininca gorevi durdurma
    await asyncio.gather(task1, task2, return_exceptions=True)

asyncio.run(main())

#=========KOŞULLU TASK İPTALİ ÖRNEKLERİ=========

#YÖNTEM 1: Kosula gore iptal 
import asyncio

async def sensor_okuyucu(stop_event):
    """Stop event tetiklenene kadar calisir"""
    sayac = 0
    while not stop_event.is_set():# is_set()=>flag'in aktif olup olmadigini kontrol eder.
        print(f"Sensor verisi: {sayac}")
        sayac += 1
        await asyncio.sleep(0.5)
    print("Sensor okuyucu durdu.")

async def kontrol_sistemi(stop_event):
    """5 saniye sonra stop sinyali gonderir"""
    await asyncio.sleep(7)
    print("STOP sinyali gonderiliyor!")
    stop_event.set() # Flag'i aktif et

async def main_event():
    stop_flag = asyncio.Event()
    """
    QUEUE= veri tasimak icin:
    Producer -> Consumer arasinda veri transferi
    Her paket/mesaj/obje ayri ayri tasinir
    FIFO yapisi (ilk giren ilk cikar)
    Veri iletisimi icin

    EVENT= durum bildirmek icin:
    Bir gorev digerine "dur" sinyali verir
    Task'ler arasi koordinasyon/senkronizasyon
    Veri tasimaz, sadece "EVET/HAYIR" durumu
    Dur", "Basla", "Hazir" gibi durumlar icin
    """
    task1 = asyncio.create_task(sensor_okuyucu(stop_flag))
    task2 = asyncio.create_task(kontrol_sistemi(stop_flag))
    await asyncio.gather(task1, task2)

asyncio.run(main_event())

#YÖNTEM 2: Veri degerine gore iptal
import asyncio
import random

async def veri_uretici_kosullu(q, stop_event):
    """Buyuk deger gelirse durdur sinyali gonderir"""
    while not stop_event.is_set(): # Stop sinyali gelene kadar uretmeye devam eder
        deger = random.randint(1, 20)
        await q.put(deger)
        print(f"Üretildi: {deger}")
        
        if deger > 17: # Eger 17'ten buyukse dur
            print("KRİTİK DEĞER! Sistem durduruluyor...")
            stop_event.set() # Stop sinyali gonder
        await asyncio.sleep(0.5)

async def veri_isleyici_kosullu(q, stop_event):
    """Stop sinyali gelene kadar isler"""
    while not stop_event.is_set():
        try:
            veri = await asyncio.wait_for(q.get(), timeout=0.5)
            print(f"İslendi: {veri}")
            q.task_done()
        except asyncio.TimeoutError:
            continue 

async def main_kosullu():
    kuyruk = asyncio.Queue() #veri tasimak icin
    stop_flag = asyncio.Event() #durdurma sinyali icin
    
    producer = asyncio.create_task(veri_uretici_kosullu(kuyruk, stop_flag))
    consumer = asyncio.create_task(veri_isleyici_kosullu(kuyruk, stop_flag))
    
    await asyncio.gather(producer, consumer, return_exceptions=True)

asyncio.run(main_kosullu())