"""
1- MULTI-TASKING +++MANTIGI+++
Elimizde islemleri tamamlamasi icin CPU var. Biz 5 farkli is gonderirsek CPU bu isleri cok kisa surede isler. Ancak sonuclarin bize ulasmasi disk, network veya bekleme (sleep) gibi sebeplerinden dolayi zaman alabilir.
Amacimiz CPU’nun bekleme surelerini bosa harcamamasidir.
Yani 1. isi milisaniyede bitirip sonucu 2 saniye gelmesini beklerken bos durmak yerine, yeni bir iplik (thread) ile baska bir ise gecmesini saglariz.

Thread’ler isletim sistemi ve Python scheduler’i tarafindan zaman dilimleriyle sirayla calistirilir.
Boylece bir is Input/Output yuzunden beklerken baska bir is calisabilir ve ekranda sonuclari daha verimli sekilde goruruz.

Bir program calistiginda buna process (surec) denir.
Her process’in en az bir thread’i vardir (main thread).



diagram = 
+---------------------------------------------+
|                                             |
|   +-------------+      +-------------+      |
|   |    Core     |      |    Core     |      |
|   +-------------+      +-------------+      |
|                                             |
|   +-------------+      +-------------+      |
|   |    Core     |      |    Core     |      |
|   +-------------+      +-------------+      |
|                                |            |
+--------------------------------|------------+
                                 |
                                 |
                                \|/
                    +------------V----------+
                  |   +---------+ +---------+ |
                  |   | Thread  | | Thread  | |
                  |   +---------+ +---------+ |
                  |   +---------+ +---------+ |
                  |   | Thread  | | Thread  | |
                  |   +---------+ +---------+ |
                    +-----------------------+

her procesin de kendine has threadlari vardir.
multi-processing ise farkli core(process) kullanir.

Threading = Ascinin yemek piserken bos durmayip salata hazirlamasi gibi dusunebiliriz.CPU’yu hizlandirmaz, sadece bekleme zamanlarini verimli kullanir.
================================================================
GIL = Global Interpreter Lock.
CPython icinde bulunan bir kilit mekanizmasidir.

Bir thread Python bytecode calistirmadan once GIL’i alir ve isi bitince birakir.Bu nedenle ayni anda yalnizca 1 thread Python bytecode calistirabilir.
4 thread farkli CPU cekirdeklerine dagitilabilir; ancak GIL nedeniyle ayni anda yalnizca biri Python kodu yurutur.Digerleri sirayla bekler.

Eger bir thread Input/Output yapiyorsa (disk, network vs. basit isler), GIL birakilir ve baska thread calisabilir.Bu yuzden threading I/O-bound islerde avantaj saglar.
Buyuk problemlerde (CPU-bound, yani saf Python hesaplama yogun isler):

Threading zaman kazandirmaz.Sebebi ayni anda paralel Python kodu calisamamasidir (GIL nedeniyle).Her thread hesap yaparken digerleri GIL’i bekler.
Bu yuzden gercek paralellik olusmaz.

=================================================================
PROCESSING (Multiprocessing):

Farkli CPU cekirdeklerinde calisan ayri process’ler olusturur.Her process’in kendi GIL’i vardir.
Bu nedenle CPU-bound islerde(zor isler) gercek paralellik saglar.
Ancak maliyeti vardir:
Bellek kopyalama, process olusturma ve processler arasi iletisim (IPC=Inter-Process Communication) maliyeti olusur.Yani daha fazla kaynak kullanir ve daha karmasiktir.
=================================================================
Sonuc olarak:

I/O-bound islerde -> Threading mantiklidir.
CPU-bound (zor Python) islerde -> Multiprocessing daha uygundur.
"""
