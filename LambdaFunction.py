"""12.02.26
Bu listeyi sorted() fonksiyonu ve bir lambda kullanarak sirala. Buyukten-Kucuge
tehlike_puani= speed/distance  ile hesaplanir.
Eğer iki hedefin skoru esitse, distance degeri kucuk olan daha öncelikli sayilmali.

"""


targets = [
    {"id": 1, "distance": 500, "speed": 120, "type": "UAV"},
    {"id": 2, "distance": 200, "speed": 850, "type": "MISSILE"},
    {"id": 3, "distance": 1000, "speed": 240, "type": "JET"},
    {"id": 4, "distance": 150, "speed": 50, "type": "UAV"}
]
sorted_targets = sorted(targets, key=lambda x: (x["speed"] / x["distance"], -x["distance"]), reverse=True)
print(sorted_targets)


"""tuple dondurdugumuz icin: (x["speed"] / x["distance"], -x["distance"]) ilk once birinci ifadeye bakilir ---x["speed"] / x["distance"]---
eger esit ise ikinci ifadeye bakilarak siralanir.-----x["distance"]---- bu ifadeye bakilir.

not: sorted() fonksiyonu varsayilan olarak kucukten buyuge siralar, ancak reverse=True parametresi ile buyukten kucuge siralama yapilir.
"""