from db import *
from fonksiyonlar import *

def kullanici_aktiflik_ayarla():
    kullanici=input("Aktiflik acmak istediginiz hesabin ismini giriniz...? geri gelmek icin 1 tusuna basiniz..: ")
    if kullanici == "1":
        return    
    connect = sqlite3.connect("kullanici_data.db")
    cursor = connect.cursor()

    cursor.execute("SELECT aktif FROM users WHERE kullanici_adi=?", (kullanici,))
    result = cursor.fetchone()
    
    if not result:
        print(f"{kullanici} isimli kullanici bulunamadi!\n")
        connect.close()
        return
    
    if result[0] == 1:
        print("Hesap zaten aktif!\n")
        connect.close()
        return
    
    cursor.execute("UPDATE users SET aktif=1 WHERE kullanici_adi=?", (kullanici,))
    connect.commit()
    connect.close()
    print(f"{kullanici} isimli kullanicinin aktifligi acildi.")


while True:
    print("Admin paneline hos geldiniz!\n")
    print("1- Kullanici aktifligi acma")
    print("2- Cikis")

    secenek = input("Seceneginizi giriniz: ")
    if secenek == "1":
        kullanici_aktiflik_ayarla()
    elif secenek == "2":
        print("Cikis yapiliyor...\n")
        break
    else:
        print("Geçersiz secenek!\n")