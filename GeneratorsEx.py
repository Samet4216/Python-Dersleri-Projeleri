"""13.02.26
raw_data_stream(): Bu bir generator fonksiyonu olsun. Sonsuz bir dongu icinde (while True) rastgele veya bir listeden sayilar uretsin.
cleaner_pipeline(stream): Baska bir generator olsun. Parametre olarak bir stream (baska bir generator) alsin.
Gelen veri None veya negatifse (< 0) o veriyi atlamali (continue).
Gecerli veriyi yield etmeli.
converter_pipeline(stream): Temizlenmis verileri alsin ve bunlari desibel (dB) cinsinden hesaplasin.
Formul: dB = 10 *log{10}{deger} (Eger matematik kutuphanesi kullanmak istersen import math).
Bu ucunu birbirine bagla ve ilk 10 gecerli sonucu ekrana yazdir.
"""
import math
import random
def raw_data_stream():
    while True:
        yield random.uniform(-10, 10) #-10 ile 10 arasinda rastgele sayilar uretir.
def cleaner_pipeline(stream):
    for veri in stream:
        if veri is None or veri < 0:
            continue
        yield veri
def converter_pipeline(stream):
    for veri in stream:
        if veri > 0: #logaritma negatif veya sifir icin tanimli olmadigindan sadece pozitif degerler icin hesaplama yapariz.
            db = 10 * math.log10(veri)
            yield db
#generatorlari birbirine baglama
raw_stream = raw_data_stream()
cleaned_stream = cleaner_pipeline(raw_stream)
converted_stream = converter_pipeline(cleaned_stream)

for _ in range(10):
    print(next(converted_stream))