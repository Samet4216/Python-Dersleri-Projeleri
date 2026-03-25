import calendar
from datetime import datetime
from fatura import fatura_goster, fatura_ode, fatura_olustur
from db import *
from sesler import *
import threading
import time

giris_yapan_kullanici = {}

# İşlem kaydı tutma fonksiyonu
def islem_kaydet(islem_turu, tutar, aciklama=""):
    try:
        connect = sqlite3.connect("kullanici_data.db")
        cursor = connect.cursor()
        cursor.execute(
            "INSERT INTO transactions (kullanici_id, islem_turu, tutar, aciklama) VALUES (?, ?, ?, ?)",
            (giris_yapan_kullanici['id'], islem_turu, tutar, aciklama)
        )
        connect.commit()
        connect.close()
    except Exception as e:
        print(f"İşlem kaydi sirasinda hata: {e}")

def atm_baslat():
    maas_sistemini_baslat() #otomatik maaş sistemini başlat
    hosgeldiniz()#ilk girişte bir kez çalacak
    while True:
        print("Hangi tur islem yapacaksiniz?\n  1) Kartli islem\n  2) Kartsiz islem\n  3) Cikis\n")
        islem_turu_konustur()
        secenek1 = int(sesli_input())
        try:
            match secenek1:
                case 1:
                    kartli()
                case 2:
                    kartsiz()
                case 3:
                    print("Çikis yapiliyor...")
                    return
                case _:
                    print("Geçersiz seçenek! Lutfen 1, 2 veya 3 girin.\n")
        except ValueError:
            print("Hata! Lutfen bir sayi girin.\n")
                
def kartli():
    while True:
        print(" 1)Mevcut Hesap\n 2)Yeni Hesap\n 3)Geri\n")
        dogrula=int(sesli_input(""))
        islem_turu_konustur()
        match dogrula:
            case 1:
                hesap_dogrula_konustur()
                print(" Mevcut hesap dogrulaniyor")
                mevcut_hesap_dogrula()
                return 
            case 2:
                yeni_hesap_ac()
                return
            case 3:
                return
            case _:
                print(" Lutfen 1, 2 veya 3 giriniz")
                dogrula=int(sesli_input(" 1)Mevcut Hesap\n 2)Yeni Hesap\n 3)Geri\n"))

def mevcut_hesap_dogrula():
    connect = sqlite3.connect("kullanici_data.db")
    cursor = connect.cursor()
    sayac=0
    sayac2=0
    while sayac <3 or sayac2 <5:
        kullanici_adi = sesli_input(" Hesap adinizi giriniz(or:AD_SOYAD, AD123, A1B2C3) '1' tusuna basip islemi iptal edebilirsiniz..: ")
        if kullanici_adi == "1":
            connect.close()
            return  
        cursor.execute("SELECT * FROM users WHERE kullanici_adi=?", (kullanici_adi,))
        result = cursor.fetchone()
        if result:
            if result[3] == 0: 
                print("Bu hesap bloke edilmistir! Banka subesi ile iletisime geçiniz.")
                connect.close()
                return 
            
            while sayac <3:
                sifre = sesli_input(" Sifrenizi giriniz: ...'1' tusuna basip islemi iptal edebilirsiniz..: ")
                if sifre == "1":
                    connect.close()
                    return
                if sifreli_parola(sifre) == result[2]:
                    print("Giris basarili")
                    global giris_yapan_kullanici
                    giris_yapan_kullanici = {'id': result[0], 'kullanici_adi': result[1], 'sifre': result[2], 'bakiye': result[4], 'cep_bakiyesi': result[5], 'iban': result[6]}
                    connect.close()
                    islem()  
                    return 
                else:
                    sayac +=1
                    if sayac == 3:
                        cursor.execute("UPDATE users SET aktif=0 WHERE kullanici_adi=?", (kullanici_adi,))
                        connect.commit()
                        print("3 yanlis denemeden sonra hesabiniz bloke edilmistir.")
                        connect.close()
                        return 
                    print(f"Yanlis sifre! Kalan deneme hakki: {3-sayac}")
        else:
            print("Hatali kullanici adi!")
            sayac2 +=1
            print(f"Kalan deneme hakki: {5-sayac2}")
            if sayac2 == 5:
                print("KULLANICI BULUNAMADI! ...Ana menuye yonlendiriliyorsunuz")
                connect.close()
                return  
   
def islem():
    while True:
        print("Hangi islemi yapmak istediğinizi belirtiniz?\n 1) Para Çekme\n 2) Para Transferleri\n 3) Para Yatirma\n 4) Ödeme İslemleri\n 5) Maas Takibi\n 6) Diğer İslemler\n 7) Geri\n")
        islem_turu_konustur()
        try:
            secenek2 = int(sesli_input(""))
            match secenek2:
                case 1:
                    para_cek()
                case 2:
                    para_transferi()
                case 3:
                    para_yatirma()
                case 4:
                    odeme_islemleri()
                case 5:
                    maas_takibi()
                case 6:
                    diger_islemler()
                case 7:
                    return
                case _:
                    print(" Geçersiz seçenek! Lutfen 1-7 arasinda bir sayi girin.\n")
        except ValueError:
            print(" Hata! Lutfen sayi giriniz.\n")

def para_cek():
    secenek=int(sesli_input("Çekmek istediginiz tutari seciniz:\n 1) 100 TL\n 2) 500 TL\n 3) 1000 TL\n 4) 2000 TL\n 5) 5000 TL\n 6) 10000 TL\n 7) Baska tutar gir\n 8) Geri\nSecenek: "))
    if secenek==8:
        return
    match secenek:
        case 1:
            tutar=100
        case 2:
            tutar=500
        case 3:
            tutar=1000
        case 4:
            tutar=2000
        case 5:
            tutar=5000
        case 6:
            tutar=10000
        case 7:
            tutar=int(sesli_input("Cekmek istediginiz tutari giriniz... geri gelmek icin 1 tusuna basiniz: "))
            if tutar==1:
                return
        case _:
            print("\nLutfen gecerli bir tutar giriniz...")
            return
    if tutar>10000:
        print("\nGunluk para cekme limitini gectiniz") 
    elif tutar<=giris_yapan_kullanici["bakiye"]:
        giris_yapan_kullanici["bakiye"] -= tutar
        giris_yapan_kullanici["cep_bakiyesi"] += tutar
        connect = sqlite3.connect("kullanici_data.db")
        cursor = connect.cursor()
        cursor.execute("UPDATE users SET bakiye=?, cep_bakiyesi=? WHERE kullanici_adi=?", (giris_yapan_kullanici['bakiye'], giris_yapan_kullanici['cep_bakiyesi'], giris_yapan_kullanici['kullanici_adi']))
        connect.commit()
        connect.close()
        print(f"\n{tutar} TL para cekiliyor...")
        print(f"Kalan bakiyeniz: {giris_yapan_kullanici['bakiye']} TL")
        print(f"Cep bakiyeniz: {giris_yapan_kullanici['cep_bakiyesi']} TL")
        islem_kaydet("Para Çekme", tutar, f"{tutar} TL nakit çekildi\n")
        para_cek_ses()
    else:
        print("Hesabinizda yeterli tutar yok...\n")
           
def para_transferi():
    tutar=int(sesli_input("geri gelmek icin 1 tusuna basiniz...\nLutfen gondermek istediginiz tutari giriniz... "))
    if tutar==1:
        return 
    if tutar>10000:
        print("\nGunluk para transfer limitini gectiniz")
        return
    elif tutar<=giris_yapan_kullanici["bakiye"]:
        iban_input="TR"+sesli_input("\ngeri gelmek icin 1 tusuna basiniz...\nLutfen gondermek istediginiz hesabin IBAN numarasini giriniz (sadece numaralar, TR otomatik eklenecektir): ")
        if iban_input=="TR1":
            return 
        alici_iban_sayi = iban_input[:4] + " " + iban_input[4:8] + " " + iban_input[8:12] + " " + iban_input[12:16] + " " + iban_input[16:20] + " " + iban_input[20:24] + " " + iban_input[24:]
        connect = sqlite3.connect("kullanici_data.db")
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM users WHERE iban=?", (alici_iban_sayi,))
        result = cursor.fetchone()
        if result:
            giris_yapan_kullanici["bakiye"] -= tutar
            cursor.execute("UPDATE users SET bakiye=? WHERE kullanici_adi=?", (giris_yapan_kullanici['bakiye'], giris_yapan_kullanici['kullanici_adi']))
            connect.commit()
            cursor.execute("UPDATE users SET bakiye=bakiye+? WHERE iban=?", (tutar, alici_iban_sayi))
            connect.commit()
            print(f"\n{tutar} TL para transferi yapiliyor....")
            islem_kaydet("Para Transferi", tutar, f"IBAN: {alici_iban_sayi} adresine {tutar} TL transfer")
        else:
            print("\nGirdiginiz IBAN numarasina sahip bir hesap bulunamadi...\n")
        connect.close()
        
def para_yatirma():
    secenek=int(sesli_input("Yatirmak istediginiz tutari seciniz:\n 1) 100 TL\n 2) 500 TL\n 3) 1000 TL\n 4) 2000 TL\n 5) 5000 TL\n 6) 10000 TL\n 7) Baska tutar gir\n 8) Geri\nSecenek: "))
    if secenek==8:
        return
    match secenek:
        case 1:
            tutar=100
        case 2:
            tutar=500
        case 3:
            tutar=1000
        case 4:
            tutar=2000
        case 5:
            tutar=5000
        case 6:
            tutar=10000
        case 7:
            tutar=int(sesli_input("Yatirmak istediginiz tutari giriniz... geri gelmek icin 1 tusuna basiniz: "))
            if tutar==1:
                return
        case _:
            print("\nLutfen gecerli bir sayi giriniz...")
            return
    if tutar<=giris_yapan_kullanici["cep_bakiyesi"]:
        if  tutar>=0:
            giris_yapan_kullanici["bakiye"] += tutar
            giris_yapan_kullanici["cep_bakiyesi"] -= tutar
            connect = sqlite3.connect("kullanici_data.db")
            cursor = connect.cursor()
            cursor.execute("UPDATE users SET bakiye=?, cep_bakiyesi=? WHERE kullanici_adi=?", (giris_yapan_kullanici['bakiye'], giris_yapan_kullanici['cep_bakiyesi'], giris_yapan_kullanici['kullanici_adi']))
            connect.commit()
            print(f"{tutar} TL para yatiriliyor....")
            print(f"Kalan cep bakiyeniz: {giris_yapan_kullanici['cep_bakiyesi']} TL")
            print(f"Guncel bakiyeniz: {giris_yapan_kullanici['bakiye']} TL")
            islem_kaydet("Para Yatırma", tutar, f"{tutar} TL yatirildi")
            para_cek_ses()
        else:
            print("Lutfen yatirmak icin gecerli bir tutar giriniz yok...\n")
    else:
        print("Yatirmak istediginiz tutar cep bakiyenizden fazla... Lutfen gecerli bir tutar giriniz...\n")

def odeme_islemleri():#başka ödeme işlemlerinin ekleneceği senaryolar için diğerlerini boş bıraktım
    while True:
        match int(sesli_input("Hangi odeme islemini yapmak istiyorsunuz?\n 1) Fatura Odeme\n 2) Geri\n")):
            case 1:
                fatura_odeme()
            case 2:
                return
            case _:
                print("\nLutfen gecerli bir secenek giriniz...")

def fatura_odeme():
    faturalar = fatura_goster(giris_yapan_kullanici['id'])
    if isinstance(faturalar, str) or not faturalar:
        return
    su, elektrik, dogalgaz, internet = faturalar
    print("="*40)
    print(f"Su faturaniz: {su} TL\nElektrik faturaniz: {elektrik} TL\nDogalgaz faturaniz: {dogalgaz} TL\nInternet faturaniz: {internet} TL")
    secenek = int(sesli_input("Faturalarizi odemek istiyor musunuz? 1/0: "))
    print("="*40)
    while secenek:
        match secenek:
            case 1:
                fatura_ode(giris_yapan_kullanici['id'], giris_yapan_kullanici['bakiye'])
                return
            case 0:
                print("Faturalariniz odenemedi.")
                return
            case _:
                print("Lutfen gecerli bir sayi giriniz...")

def maas_takibi():
    secenek=int(input("Maasinizi hangi yöntemle aliyorsunuz lutfen belirtin...Geri gelmek icin 3 tusuna basiniz...\n 1) Elden(cep_bakiyesi)\n 2) Banka hesabina(bakiye)\n 3) Geri\n"))
    match secenek:
        case 3:
            return
        case 1:
            elden_maas_takibi()
        case 2:
            bankadan_maas_takibi()
        case _:
            print("Lutfen gecerli bir sayi giriniz...")
    print("Maas takibi islemi yapiliyor...")
    
def elden_maas_takibi():
    print("✓ Maasiniz elden (nakit) olarak cep bakiyenize yatirilacaktir.")
    maas(maas_turu="E")
    

def bankadan_maas_takibi():
    print("✓ Maasiniz banka hesabiniza otomatik olarak yatirilacaktir.")
    maas(maas_turu="B")
    


def diger_islemler():
    while True:
        print("Hangi islemi yapmak istediğinizi belirtiniz?\n 1) Hesap Bilgileri\n 2) Kart Yenileme\n 3) Şifre Değistirme\n 4) Kart Bloke\n 5) İşlem Geçmişi\n 6) Geri\n")
        islem_turu_konustur()
        try:
            secenek3 = int(sesli_input(""))
            match secenek3:
                case 1:
                    hesap_sorgula()
                case 2:
                    kart_yenileme()
                case 3:
                    sifre_degistirme()
                case 4:
                    kart_bloke()
                case 5:
                    islem_gecmisi_goster()
                case 6:
                    return
                case _:
                    print("Geçersiz seçenek! Lutfen 1-6 arasinda bir sayi girin.\n")
        except ValueError:
            print("Hata! Lutfen sayi giriniz.\n")

def hesap_sorgula():
    print("Hesap bilgileri sorgulama islemi yapiliyor...") 
    print("="*40)
    print(f"Hesap adi: {giris_yapan_kullanici['kullanici_adi']}")
    print(f"Mevcut bakiyeniz: {giris_yapan_kullanici['bakiye']} TL")
    print(f"Cep bakiyeniz: {giris_yapan_kullanici['cep_bakiyesi']} TL")
    print(f"IBAN Numaraniz: {giris_yapan_kullanici['iban']}")
    print("="*40)

def kart_yenileme():
    print("Kart yenileme islemi yapiliyor...\n")
    print("Yeni kartiniz en kisa zamanda adresinize gonderilecektir.")
    a=sesli_input("Mevcut sifrenizi degistirmek istiyor musunuz? 1/0: ")
    if a == "1":
        sifre_degistirme()
    print("\nKart yenileme islemi ile yeni iban alacaksiniz.")
    giris_yapan_kullanici['iban'] = iban_uret()
    print("Yeni kart bilgileriniz guncelleniyor...")
    connect = sqlite3.connect("kullanici_data.db")
    cursor = connect.cursor()
    cursor.execute("UPDATE users SET iban=? WHERE kullanici_adi=?", (giris_yapan_kullanici['iban'], giris_yapan_kullanici['kullanici_adi']))
    connect.commit()
    print(f"\nYeni IBAN Numaraniz: {giris_yapan_kullanici['iban']}")

def islem_gecmisi_goster():
    connect = sqlite3.connect("kullanici_data.db")
    cursor = connect.cursor()
    cursor.execute(
        "SELECT id, islem_turu, tutar, tarih FROM transactions WHERE kullanici_id=? ORDER BY tarih DESC LIMIT 20",
        (giris_yapan_kullanici['id'],)
    )
    islemler = cursor.fetchall()
    connect.close()
    
    if not islemler:
        print("\nHenuz islem gecmisiniz yok.\n")
        return
    
    print("="*70)
    print(f"{'Sıra':<5} {'İşlem Türü':<20} {'Tutar (TL)':<15} {'Tarih':<25}")
    print("="*70)
    
    for idx, (islem_id, islem_turu, tutar, tarih) in enumerate(islemler, 1):
        print(f"{idx:<5} {islem_turu:<20} {tutar:<15.2f} {tarih:<25}")
    print("="*70 + "\n")

def sifre_degistirme():
    print("Sifre degistirme islemi yapiliyor...")
    print("\nMevcut sifreniz: ", giris_yapan_kullanici['sifre'])
    while True:
        yeni_sifre=sesli_input("Yeni sifrenizi giriniz: ")
        if not sifre_kontrol(yeni_sifre):
            print("Sifre uygun degil.")
        else:
            break
    connect = sqlite3.connect("kullanici_data.db")
    cursor = connect.cursor()
    yeni_sifre_hash = sifreli_parola(yeni_sifre)
    cursor.execute("UPDATE users SET sifre=? WHERE id=?", (yeni_sifre_hash, giris_yapan_kullanici['id']))
    connect.commit()
    print("\nSifre basariyla degistirildi.")

def kart_bloke():
    secenek = sesli_input("Kartinizi bloke etmek istediginize emin misiniz? 1/0: ")
    while secenek:
        match secenek:
            case "1":
                connect = sqlite3.connect("kullanici_data.db")
                cursor = connect.cursor()
                cursor.execute("UPDATE users SET aktif=0 WHERE id=?", (giris_yapan_kullanici['id'],))
                connect.commit()
                connect.close()
                print("Kartiniz basariyla bloke edildi.\n")
                return diger_islemler()
            case "0":
                return diger_islemler()
            case _:
                print("Lutfen gecerli bir sayi giriniz...")





#========================================================================
# Kartsız islem icin QR kodu okuma fonksiyonları===yapay/zeka dan alinti
#========================================================================

import cv2
from pyzbar.pyzbar import decode
from tkinter import filedialog, Tk

img = cv2.imread("sesler_resimler/QR.png")

def kayitli_qr_icerik_al():
    qr_kodlari = decode(img)
    if qr_kodlari:
        return qr_kodlari[0].data.decode("utf-8")
    return None

def resimden_giris():
    # File dialog'u açmak için Tk penceresini oluştur (gizli)
    root = Tk()
    root.withdraw()  # Pencereyi gizle
    root.attributes('-topmost', True)  # Pencereyi öne al
    
    # Resim dosyası seç
    dosya_yolu = filedialog.askopenfilename(
        title="QR kodlu resmi seçiniz",
        filetypes=[("Resim Dosyaları", "*.png *.jpg *.jpeg *.bmp"), ("Tüm Dosyalar", "*.*")]
    )
    
    root.destroy()  # Tk penceresini kapat
    
    # Kullanıcı iptal ettiyse
    if not dosya_yolu:
        print("Islem iptal edildi.")
        return
    
    # Seçilen resmi oku
    secilen_img = cv2.imread(dosya_yolu)
    if secilen_img is None:
        print("!!! Resim okunamadi! Dosya yolunu kontrol ediniz.")
        return
    
    # QR kodu çöz
    qr_kodlari = decode(secilen_img)
    if qr_kodlari:
        qr_icerik = qr_kodlari[0].data.decode("utf-8")
        kayitli_qr = kayitli_qr_icerik_al()
        
        if qr_icerik == kayitli_qr:
            print("Yetkili QR kod tanindi!")
            print("Sisteme giris yapiliyor...")
            islem()
        else:
            print("!!! Yetkisiz QR kod! Giris reddedildi.")
            print(f"Okunan: {qr_icerik}")
    else:
        print("!!!Secilen resimde QR kod bulunamadi!!!")

def QR_giris():
    kayitli_icerik = kayitli_qr_icerik_al()
    if not kayitli_icerik:
        print("!!! Kayitli QR bulunamadi!")
        return
    print("Kamera aciliyor... Kayitli QR kodunuzu gosterin.")
    print("ESC tusuna basarak iptal edebilirsiniz.")
    
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("!!! Kamera acilamadi!")
            break
        h, w = frame.shape[:2]
        kare_boyut = int(min(h, w)*0.9)
        sol_ust = (w // 2 - kare_boyut // 2, h // 2 - kare_boyut // 2)
        sag_alt = (w // 2 + kare_boyut // 2, h // 2 + kare_boyut // 2)
        cv2.rectangle(frame, sol_ust, sag_alt, (0, 255, 0), 2)
        qr_kodlari = decode(frame)#tüm qr lari algilar ve listeye alir.
        for qr in qr_kodlari:
            veri = qr.data.decode("utf-8")
            cap.release()
            cv2.destroyAllWindows()
            if veri == kayitli_icerik:
                print("Yetkili QR kod tanindi!")
                print("Sisteme giris yapiliyor...")
                islem()
                return
            else:
                print("!!! Yetkisiz QR kod! Giris reddedildi.")
                print(f"Okunan: {veri}")
                return
        cv2.imshow("QR Okuyucu - Kayitli QR'inizi gosterin", frame)
        print("Kamera acik... Kayitli QR kodunuzu gosterin. ESC tusuna basarak iptal edebilirsiniz.")
        if cv2.waitKey(1) == 27:  # ESC
            print("Islem iptal edildi.")
            break
    cap.release()
    cv2.destroyAllWindows()

def kartsiz():
    while True:
        print(" Lutfen giris yönteminizi giriniz\n 1) Resim Sec\n 2) QR giris\n 3) Geri\n")
        islem_turu_konustur()
        try:
            secenek_kartsiz = int(sesli_input(""))
            match secenek_kartsiz:
                case 1:
                    resimden_giris()
                    return
                case 2:
                    QR_giris()
                    return
                case 3:
                    return
                case _:
                    print("Lutfen gecerli bir sayi giriniz...")
        except ValueError:
            print("Hata! Lutfen bir sayi giriniz...")
#========================================================================
# ZAMANLA ARTAN PARA ICIN MESLEK FONKSİYONU
#========================================================================
import time
def maas(maas1=None, meslek=None, maas_turu=None):
    print("Aylik hesabiniza maasinizi yatirabilmemiz icin lutfen maas bilgilerini giriniz...")
    # Eğer parametre gelmediyse input iste
    if maas1 is None:
        maas1 = int(sesli_input("Aylik gelirinizi giriniz (TL): "))
    if meslek is None:
        meslek = sesli_input("Lutfen mesleginizi giriniz: ")
    
    connect = None
    try:
        connect = sqlite3.connect("kullanici_data.db")
        cursor = connect.cursor()
        
        # Önce zaten kayıtlı maaş bilgisi var mı kontrol et
        cursor.execute("SELECT maas FROM personal_info WHERE kullanici_id=?", (giris_yapan_kullanici['id'],))
        mevcut = cursor.fetchone()
        if mevcut:
            print("Zaten maas bilgileriniz kayitli. Yeni bilgi eklenemez.")
            connect.close()
            return
        
        # Maaş gününü sor
        maas_gunu = maasa_kalan_sure()
        
        if maas_gunu is None:
            connect.close()
            return
        # Veritabanına kaydet
        cursor.execute(
            "INSERT INTO personal_info (kullanici_id, meslek, maas, maas_gunu, maas_turu) VALUES (?, ?, ?, ?, ?)",
            (giris_yapan_kullanici['id'], meslek, maas1, maas_gunu, maas_turu)
        )
        connect.commit()
        
        if maas_turu == "E":
            print(f"✓ Maaş bilgileriniz kaydedildi! (Elden/Nakit)")
        elif maas_turu == "B":
            print(f"✓ Maaş bilgileriniz kaydedildi! (Banka Hesabi)")
        else:
            print(f"✓ Maaş bilgileriniz kaydedildi!")
        
        print(f"Maasiniz her ayin {maas_gunu}. gunu otomatik olarak yatirilacaktir.")
        
        # Eğer bugün maaş günüyse hemen para yatır
        if datetime.now().day == maas_gunu:
            print("\n[HEMEN PARA YATIRILIYOR...]")
            if maas_turu == "E":
                # Elden - Cep bakiyesine yatır
                cursor.execute("UPDATE users SET cep_bakiyesi = cep_bakiyesi + ? WHERE id=?", (maas1, giris_yapan_kullanici['id']))
                connect.commit()
                giris_yapan_kullanici['cep_bakiyesi'] += maas1
                print(f"✓ {maas1} TL maasiniz cep bakiyenize yatirildi!")
                print(f"Yeni cep bakiyeniz: {giris_yapan_kullanici['cep_bakiyesi']} TL")
                # İşlem kaydı
                cursor.execute(
                    "INSERT INTO transactions (kullanici_id, islem_turu, tutar, aciklama) VALUES (?, ?, ?, ?)",
                    (giris_yapan_kullanici['id'], "Maaş (Elden)", maas1, f"{maas1} TL maaş elden yatirildi")
                )
                connect.commit()
            elif maas_turu == "B":
                # Banka - Bakiyeye yatır
                cursor.execute("UPDATE users SET bakiye = bakiye + ? WHERE id=?", (maas1, giris_yapan_kullanici['id']))
                connect.commit()
                giris_yapan_kullanici['bakiye'] += maas1
                print(f"✓ {maas1} TL maasiniz banka hesabiniza yatirildi!")
                print(f"Yeni bakiyeniz: {giris_yapan_kullanici['bakiye']} TL")
                # İşlem kaydı
                cursor.execute(
                    "INSERT INTO transactions (kullanici_id, islem_turu, tutar, aciklama) VALUES (?, ?, ?, ?)",
                    (giris_yapan_kullanici['id'], "Maaş (Banka)", maas1, f"{maas1} TL maaş bankadan yatirildi")
                )
                connect.commit()
        
    except Exception as e:
        print(f"Hata: {e}")
    finally:
        if connect:
            connect.close()

def maasa_kalan_sure():
    bugun = datetime.now()
    try:
        maas_gunu = int(sesli_input("Maasinizin yatacagi gunu giriniz (1-31, iptal: 0): "))
        if maas_gunu == 0:
            print("İşlem iptal edildi.")
            return None
        if maas_gunu < 1 or maas_gunu > 31:
            print("Lütfen 1-31 arasinda bir gün giriniz!")
            return maasa_kalan_sure()  #While veya match case yerine recursive daha mantıklı 
    except ValueError:
        print("Lütfen geçerli bir sayi giriniz...")
        return maasa_kalan_sure()
    
    #calender fonksiyonu ayın ilk gününü ve ayın gün sayısını döndürür bize 1. index yani gün sayisi lazım..
    bu_ay_gun_sayisi = calendar.monthrange(bugun.year, bugun.month)[1]#bugun.year, bugun.month iki parametre ister yılı ve ayı
    
    #eger kullanici 31 girdi ama bu ay 30 gun ise maas gunu 30 olacak sekilde duzenleme yapalim
    hedef_gun = min(maas_gunu, bu_ay_gun_sayisi)#aydaki gün sayısı ile uyumsuz bir imput almayı engeller.
    
    # Sadece günleri karşılaştır (saat problemini çöz)
    bugun_gun = bugun.day
    
    #eğer bugün maaş günüyse kalan gün 0
    if bugun_gun == maas_gunu:
        kalan_gun = 0
        print("✓ Bugun maas gununuz! Sisteme kayit tamamlandiginda maasiniz otomatik yatirilacak.")
    #eğer girilen maaş gününe daha gün varsa
    elif bugun_gun < maas_gunu:
        kalan_gun = maas_gunu - bugun_gun
        print(f"✓ Bir sonraki maasa {kalan_gun} gun kaldi.")
    else:#ama bu ayın maaş günü geçtiyse bir dahaki aya bak
        #aralık ayı için özel durum:
        if bugun.month == 12:
            yeni_yil = bugun.year + 1
            yeni_ay = 1
        else:#diğer aylar için aynı yılın sonraki ayında bir hedef belirleriz
            yeni_yil = bugun.year
            yeni_ay = bugun.month + 1
        
        #gelecek ay için yani bu ayki maaş gününü geçtiysek diğer ayın gün sayısını döndürürüz.
        yeni_ay_gun_sayisi = calendar.monthrange(yeni_yil, yeni_ay)[1]
        hedef_gun_gelecek = min(maas_gunu, yeni_ay_gun_sayisi)
        
        # Gelecek aydaki maaş gününe kadar kalan gün
        bugun_tarih = datetime(bugun.year, bugun.month, bugun.day)
        gelecek_maas = datetime(yeni_yil, yeni_ay, hedef_gun_gelecek)
        kalan_gun = (gelecek_maas - bugun_tarih).days
        print(f"✓ Bir sonraki maasa {kalan_gun} gun kaldi.")
    
    return maas_gunu  # Maaş gününü döndür (kaydedilecek)

#========================================================================
# OTOMATIK MAAŞ YATIRMA SİSTEMİ (ARKA PLAN)
#========================================================================

def tum_kullanicilar_maas_yatir_elden():
    connect = None
    try:
        bugun = datetime.now().day
        connect = sqlite3.connect("kullanici_data.db")
        cursor = connect.cursor()
        
        # Maaş günü bugün olan ve elden (E) maaş alan kullanıcıları bul
        cursor.execute("""
            SELECT p.kullanici_id, p.maas, u.kullanici_adi, u.cep_bakiyesi
            FROM personal_info p
            JOIN users u ON p.kullanici_id = u.id
            WHERE p.maas_gunu = ? AND u.aktif = 1 AND p.maas_turu = 'E'
        """, (bugun,))
        
        kullanicilar = cursor.fetchall()
        if kullanicilar:
            print(f"\n[SISTEM] {len(kullanicilar)} kullaniciya maas yatirilacak...")
        
        for kullanici_id, maas, kullanici_adi, mevcut_bakiye in kullanicilar:
            # Bugün zaten maaş yatırıldı mı kontrol et
            bugun_tarih = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("""
                SELECT COUNT(*) FROM transactions 
                WHERE kullanici_id = ? 
                AND islem_turu = 'Otomatik Maaş' 
                AND DATE(tarih) = ?
            """, (kullanici_id, bugun_tarih))
            
            if cursor.fetchone()[0] > 0:
                continue  # Bu kullanıcıya bugün zaten maaş yatırılmış
            
            # Maaş yatır (Elden - Cep Bakiyesi)
            cursor.execute("UPDATE users SET cep_bakiyesi = cep_bakiyesi + ? WHERE id=?", (maas, kullanici_id))
            cursor.execute(
                "INSERT INTO transactions (kullanici_id, islem_turu, tutar, aciklama) VALUES (?, ?, ?, ?)",
                (kullanici_id, "Otomatik Maaş (Elden)", maas, f"{maas} TL aylik maas elden yatirildi")
            )
            
            print(f"[SISTEM-ELDEN] {kullanici_adi} -> {maas} TL maas yatirildi. (Yeni cep_bakiyesi: {mevcut_bakiye + maas} TL)")
        
        connect.commit()
        
    except Exception as e:
        print(f"[SISTEM HATA] Maas yatirma sirasinda hata: {e}")
    finally:
        if connect:
            connect.close()

def tum_kullanicilar_maas_yatir_bakiye():
    connect = None
    try:
        bugun = datetime.now().day
        connect = sqlite3.connect("kullanici_data.db")
        cursor = connect.cursor()
        
        # Maaş günü bugün olan ve bankadan (B) maaş alan kullanıcıları bul
        cursor.execute("""
            SELECT p.kullanici_id, p.maas, u.kullanici_adi, u.bakiye
            FROM personal_info p
            JOIN users u ON p.kullanici_id = u.id
            WHERE p.maas_gunu = ? AND u.aktif = 1 AND p.maas_turu = 'B'
        """, (bugun,))
        
        kullanicilar = cursor.fetchall()
        if kullanicilar:
            print(f"\n[SISTEM] {len(kullanicilar)} kullaniciya maas yatirilacak...")
        
        for kullanici_id, maas, kullanici_adi, mevcut_bakiye in kullanicilar:
            # Bugün zaten maaş yatırıldı mı kontrol et
            bugun_tarih = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("""
                SELECT COUNT(*) FROM transactions 
                WHERE kullanici_id = ? 
                AND islem_turu = 'Otomatik Maaş' 
                AND DATE(tarih) = ?
            """, (kullanici_id, bugun_tarih))
            
            if cursor.fetchone()[0] > 0:
                continue  # Bu kullanıcıya bugün zaten maaş yatırılmış
            # Maaş yatır (Banka - Bakiye)
            cursor.execute("UPDATE users SET bakiye = bakiye + ? WHERE id=?", (maas, kullanici_id))
            cursor.execute(
                "INSERT INTO transactions (kullanici_id, islem_turu, tutar, aciklama) VALUES (?, ?, ?, ?)",
                (kullanici_id, "Otomatik Maaş (Banka)", maas, f"{maas} TL aylik maas bankadan yatirildi")
            )
            
            print(f"[SISTEM-BANKA] {kullanici_adi} -> {maas} TL maas yatirildi. (Yeni bakiye: {mevcut_bakiye + maas} TL)")
        
        connect.commit()
        
    except Exception as e:
        print(f"[SISTEM HATA] Maas yatirma sirasinda hata: {e}")
    finally:
        if connect:
            connect.close()

def maas_kontrol_sistemi_elden():
    son_kontrol_gunu = None
    
    while True:
        try:
            bugun = datetime.now().day
            
            # Günde bir kez kontrol et (gün değiştiğinde)
            if son_kontrol_gunu != bugun:
                print(f"\n[SISTEM] Tarih: {datetime.now().strftime('%d/%m/%Y %H:%M')} - Maas kontrol ediliyor...")
                tum_kullanicilar_maas_yatir_elden()
                son_kontrol_gunu = bugun
            # 1 saat bekle sonra tekrar kontrol et
            time.sleep(3600)
        except Exception as e:
            print(f"[SISTEM HATA] Kontrol sirasinda hata: {e}")
            time.sleep(3600)

def maas_kontrol_sistemi_bakiye():
    son_kontrol_gunu = None  
    while True:
        try:
            bugun = datetime.now().day
            # Günde bir kez kontrol et (gün değiştiğinde)
            if son_kontrol_gunu != bugun:
                print(f"\n[SISTEM] Tarih: {datetime.now().strftime('%d/%m/%Y %H:%M')} - Maas kontrol ediliyor...")
                tum_kullanicilar_maas_yatir_bakiye()
                son_kontrol_gunu = bugun
            # 1 saat bekle sonra tekrar kontrol et
            time.sleep(3600)
        except Exception as e:
            print(f"[SISTEM HATA] Kontrol sirasinda hata: {e}")
            time.sleep(3600)

def maas_sistemini_baslat():
    thread = threading.Thread(target=maas_kontrol_sistemi_elden, daemon=True)
    thread2 = threading.Thread(target=maas_kontrol_sistemi_bakiye, daemon=True)
    thread.start()
    thread2.start()

