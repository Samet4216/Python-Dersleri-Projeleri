import random
import time
from datetime import datetime


def su_faturasi():
    sayilar = list(range(200, 1200))
    weights = []
    for s in sayilar:
        if s <= 500:
            weights.append(1)
        elif s<=800:
            weights.append(0.6)
        else:
            weights.append(0.3)

    su = random.choices(sayilar, weights=weights, k=1)[0]
    return su

def elektrik_faturasi():
    sayilar = list(range(200, 1100))
    weights = []
    for s in sayilar:
        if s <= 500:
            weights.append(1)
        elif s<=800:
            weights.append(0.6)
        else:
            weights.append(0.3)

    elektrik = random.choices(sayilar, weights=weights, k=1)[0]
    return elektrik

def dogalgaz_faturasi():#kış aylarında daha yüksek olabilir, yaz aylarında daha düşük olabilir...
    now=datetime.now()
    weights = []
    
    if now.month in [12, 1, 2]:
        sayilar = list(range(12500, 2500))
        for s in sayilar:
            if s <= 1750:
                weights.append(1)
            elif s <= 2200:
                weights.append(0.7)
            else:
                weights.append(0.3)
    else:
        sayilar = list(range(300, 1100))
        for s in sayilar:
            if s <= 500:
                weights.append(1)
            elif s <= 800:
                weights.append(0.5)
            else:
                weights.append(0.2)

    dogalgaz = random.choices(sayilar, weights=weights, k=1)[0]
    return dogalgaz

def internet_faturasi():#sinirsiz ev interneti+cep interneti
    sayilar = list(range(500, 1250))
    weights = []
    for s in sayilar:
        if s <= 700:
            weights.append(1)
        elif s<=1000:
            weights.append(0.5)
        else:
            weights.append(0.2)

    internet = random.choices(sayilar, weights=weights, k=1)[0]
    if internet > 1000:
        print("Bu ay cep internetinizi 2 kere yenilediniz, bu yüzden faturaniz biraz daha yüksek olabilir.")
    return internet

def fatura_olustur():
    now=datetime.now()
    if now.day==24:
        print("Bu ayki faturalariniz olusturuluyor...")
        time.sleep(2)
        print("Faturalariniz olusturuldu!")
        time.sleep(1) 
        su = su_faturasi()
        elektrik = elektrik_faturasi()
        dogalgaz = dogalgaz_faturasi()
        internet = internet_faturasi()
    else:
        return "Faturalariniz her ayin 1'inde olusturulur."
    return su, elektrik, dogalgaz, internet

def yeni_hesap_fatura_olustur(kullanici_id):
    try:
        import sqlite3
        from datetime import timedelta
        
        now = datetime.now()
        # Sonraki ayın fatura günü
        odeme_tarihi = (now.replace(day=1) + timedelta(days=32)).replace(day=1)
        
        # Fatura tutarlarını oluştur
        su = su_faturasi()
        elektrik = elektrik_faturasi()
        dogalgaz = dogalgaz_faturasi()
        internet = internet_faturasi()
        
        # Veritabanına ekle
        connect = sqlite3.connect("kullanici_data.db")
        cursor = connect.cursor()
        cursor.execute(
            "INSERT INTO debts (kullanici_id, elektrik, dogalgaz, su, internet, odeme_tarihi) VALUES (?, ?, ?, ?, ?, ?)",
            (kullanici_id, elektrik, dogalgaz, su, internet, odeme_tarihi)
        )
        connect.commit()
        connect.close()
    except Exception as e:
        print(f"Fatura olusturulurken hata: {e}")

import sqlite3
from datetime import timedelta

def fatura_goster(kullanici_id):
    now=datetime.now()
    connect= sqlite3.connect("kullanici_data.db")
    cursor = connect.cursor()
    
    # Bu ay için zaten fatura var mı kontrol et
    ay_basi = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    cursor.execute("SELECT su, elektrik, dogalgaz, internet FROM debts WHERE kullanici_id=? AND odeme_tarihi >= ? ORDER BY odeme_tarihi DESC LIMIT 1", (kullanici_id, ay_basi))
    mevcut_fatura = cursor.fetchone()
    
    if mevcut_fatura:
        # Bu ay için fatura zaten var, mevcut faturayı döndür
        print("Mevcut faturalariniz getiriliyor...")
        time.sleep(1)
        connect.close()
        return mevcut_fatura  # (su, elektrik, dogalgaz, internet)
    
    # Bu ay için fatura yok, yeni oluştur
    faturalar = fatura_olustur()
    
    # Eğer ayın belirlenen günü ise yeni fatura oluştur
    if isinstance(faturalar, tuple):
        odeme_tarihi = (now.replace(day=1) + timedelta(days=32)).replace(day=1)
        cursor.execute("INSERT INTO debts (kullanici_id, elektrik, dogalgaz, su, internet, odeme_tarihi) VALUES (?, ?, ?, ?, ?, ?)", (kullanici_id, faturalar[1], faturalar[2], faturalar[0], faturalar[3], odeme_tarihi))
        connect.commit()
        connect.close()
        return faturalar
    else:
        # Belirlenen gün değilse, veritabanından son faturayı getir
        cursor.execute("SELECT su, elektrik, dogalgaz, internet FROM debts WHERE kullanici_id=? ORDER BY odeme_tarihi DESC LIMIT 1", (kullanici_id,))
        fatura_sonuc = cursor.fetchone()
        connect.close()
        if fatura_sonuc:
            return fatura_sonuc  # (su, elektrik, dogalgaz, internet)
        else:
            print(faturalar)
            return None

from sesler import sesli_input

def fatura_ode(kullanici_id, bakiye):
    from fonksiyonlar import islem_kaydet
    
    connect = sqlite3.connect("kullanici_data.db")
    cursor = connect.cursor()
    
    cursor.execute("SELECT elektrik, dogalgaz, su, internet, id FROM debts WHERE kullanici_id=? ORDER BY odeme_tarihi DESC LIMIT 1", (kullanici_id,))
    fatura = cursor.fetchone()
    
    if not fatura:
        print("Ödenecek faturaniz bulunmamaktadir.")
        connect.close()
        return
    
    elektrik, dogalgaz, su, internet, debt_id = fatura
    
    print("\n=== FATURA ÖDEME SİSTEMİ ===")
    print(f"Bakiyeniz: {bakiye} TL\n")
    print("Ödenecek Faturalar:")
    print(f"1) Su Faturasi: {su} TL")
    print(f"2) Elektrik Faturasi: {elektrik} TL")
    print(f"3) Doğalgaz Faturasi: {dogalgaz} TL")
    print(f"4) İnternet Faturasi: {internet} TL")
    print(f"5) Tümünü Öde: {su + elektrik + dogalgaz + internet} TL")
    print("0) Çikiş\n")
    
    secim = sesli_input("Hangi faturayi ödemek istersiniz? (0-5): ")
    
    fatura_bilgisi = {
        '1': ('Su', su),
        '2': ('Elektrik', elektrik),
        '3': ('Doğalgaz', dogalgaz),
        '4': ('İnternet', internet),
        '5': ('Tümü', su + elektrik + dogalgaz + internet)
    }
    
    if secim == '0':
        print("Çikiliyor...")
        connect.close()
        return
    
    if secim not in fatura_bilgisi:
        print("Geçersiz seçim!")
        connect.close()
        return
    
    fatura_adi, odeme_tutari = fatura_bilgisi[secim]
    
    if bakiye >= odeme_tutari:
        yeni_bakiye = bakiye - odeme_tutari
        islem_turu = ""
        islem_aciklama = ""

        if secim == '1':
            cursor.execute("UPDATE debts SET su=0 WHERE id=?", (debt_id,))
            islem_turu = "Su Faturasi"
            islem_aciklama = f"{odeme_tutari} TL su faturasi ödendi"
        elif secim == '2':
            cursor.execute("UPDATE debts SET elektrik=0 WHERE id=?", (debt_id,))
            islem_turu = "Elektrik Faturasi"
            islem_aciklama = f"{odeme_tutari} TL elektrik faturasi ödendi"
        elif secim == '3':
            cursor.execute("UPDATE debts SET dogalgaz=0 WHERE id=?", (debt_id,))
            islem_turu = "Dogalgaz Faturasi"
            islem_aciklama = f"{odeme_tutari} TL dogalgaz faturasi ödendi"
        elif secim == '4':
            cursor.execute("UPDATE debts SET internet=0 WHERE id=?", (debt_id,))
            islem_turu = "İnternet Faturasi"
            islem_aciklama = f"{odeme_tutari} TL internet faturasi ödendi"
        elif secim == '5':
            cursor.execute("UPDATE debts SET su=0, elektrik=0, dogalgaz=0, internet=0 WHERE id=?", (debt_id,))
            islem_turu = "Tüm Faturalar"
            islem_aciklama = f"{odeme_tutari} TL tüm faturalar ödendi"

        cursor.execute("UPDATE users SET bakiye=? WHERE id=?", (yeni_bakiye, kullanici_id))
        connect.commit()
        connect.close()
        
        # İşlem kaydını veritabanı bağlantısı kapatıldıktan sonra yap
        islem_kaydet(islem_turu, odeme_tutari, islem_aciklama)
        
        print(f"\n {fatura_adi} Faturasi başariyla ödendi!")
        print(f"  Ödenen Tutar: {odeme_tutari} TL")
        print(f"  Yeni Bakiyeniz: {yeni_bakiye} TL\n")
    else:
        eksik_tutar = odeme_tutari - bakiye
        print(f"\n Yetersiz bakiye...")
        print(f"  Ödenecek Tutar: {odeme_tutari} TL")
        print(f"  Mevcut Bakiye: {bakiye} TL")
        print(f"  Eksik Tutar: {eksik_tutar} TL\n")
        connect.close()