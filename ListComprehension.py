""" 12.02.26
ham veriyi işle metre==feet dönüşümü yap
negatif değerleri alma
5k üstü irtifayi kritik 0-5k arasi irtifayi normal olacak şekilde tuple içine al
"""

raw_altitudes = [1500.5, -20.0, 2100.2, 545.0, -999.0, 3050.0]#ham irtifa--  
#1 metre yaklaşik 3.2 feet
filtered_altitudes = [x*3.2 for x in raw_altitudes]

normal_altitudes = ("NormalAltitudes",) #normal irtifalar--
high_altitudes = ("CriticalAltitudes",) #kritik irtifalar--

normal = [x for x in filtered_altitudes if x *3.2 > 0 and x <= 5000]
critical = [x for x in filtered_altitudes if x *3.2 > 5000]

normal_altitudes = normal_altitudes + tuple(normal)
high_altitudes = high_altitudes + tuple(critical)

print(normal_altitudes)
print(high_altitudes)