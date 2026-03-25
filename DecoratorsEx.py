"""
require_role(role) parametreli dekoratör olacak
log dekoratörü olacak
measure_time olacak
Bir tane örnek fonksiyon yazacaksın (mesela delete_user() ya da veritabani_temizle() gibi)
Üç dekoratörü de üst üste kullanacaksın
Rolü "user" yapınca erişim engellenecek
Rol "admin" olunca çalışacak
"""
def decorator(func):
    def wrapper(*args, **kwargs):
        print("Fonksiyon cagrilmadan onceki islem")
        func(*args, **kwargs)
        print("Fonksiyon cagrildiktan sonraki islem")
    return wrapper
