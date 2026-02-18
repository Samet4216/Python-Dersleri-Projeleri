#----- yeni_liste = [(ifade) for (eleman) in (iterable) if (kosul)]---- 

#1) yerel değişken dişaridaki değişkeni değiştiremez (local scope)
x = 10
lst = [x for x in range(5)]


#2)filtreleme işleminde kullanilir:
cift_kareler = [x**2 for x in range(1, 11) if x % 2 == 0]


# List comprehension, sonucun tamamini bellekte (RAM) bir kerede oluşturur.


#3) Eğer listeye hemen ihtiyacin yoksa, köşeli parantez yerine normal parantez () kullanarak ihtiyaç halinde oluşturulup,kullanilir.
lst = (x for x in range(5)) #anlik oluşturulur,anlik işlenir.


#4) Nested Comprehension (İç İçe Döngüler): Matris işlemleri veya 3D koordinat dönüşümleri için kullanilir:
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

buyut = [[eleman * 2 for eleman in satir] for satir in matrix] #satirlari alir gereken islemi yapip yeni matrix oluşturur.

#cikti:
[
 [2, 4, 6],
 [8, 10, 12],
 [14, 16, 18]
]

