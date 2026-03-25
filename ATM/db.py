import sqlite3
import hashlib
import re


connect = sqlite3.connect("kullanici_data.db")
cursor = connect.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kullanici_adi TEXT NOT NULL,
    sifre TEXT NOT NULL,
    aktif INTEGER DEFAULT 1,
    bakiye REAL DEFAULT 1000,
    cep_bakiyesi REAL DEFAULT 0,
    iban TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kullanici_id INTEGER NOT NULL,
    islem_turu TEXT NOT NULL,
    tutar REAL NOT NULL,
    tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    aciklama TEXT,
    FOREIGN KEY (kullanici_id) REFERENCES users(id)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS personal_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kullanici_id INTEGER NOT NULL,
    meslek TEXT NOT NULL,
    maas REAL NOT NULL,
    maas_gunu INTEGER,
    maas_turu TEXT NOT NULL,  
    FOREIGN KEY (kullanici_id) REFERENCES users(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS debts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kullanici_id INTEGER NOT NULL,
    elektrik REAL NOT NULL,
    dogalgaz REAL NOT NULL,
    su REAL NOT NULL,
    internet REAL NOT NULL,           
    odeme_tarihi DATE NOT NULL,
    FOREIGN KEY (kullanici_id) REFERENCES users(id)
)
""")


connect.commit()
connect.close()


def sifreli_parola(sifre):
    return hashlib.sha256(sifre.encode()).hexdigest()

def sifre_kontrol(sifre):
    if len(sifre)<8:
        print("Sifre en az 8 karakter olmalidir.")
        return False
    if not re.search(r'[A-Z]', sifre):
        print("Sifre en az bir buyuk harf icermelidir.")
        return False
    if not re.search(r'[a-z]', sifre):
        print("Sifre en az bir kucuk harf icermelidir.")
        return False
    if not re.search(r'[0-9]', sifre):
        print("Sifre en az bir rakam icermelidir.")
        return False
    return True
    
def iban_uret():
    import random
    iban = "TR"
    for _ in range(24):
        iban += str(random.randint(0, 9))
    iban = iban[:4] + " " + iban[4:8] + " " + iban[8:12] + " " + iban[12:16] + " " + iban[16:20] + " " + iban[20:24] + " " + iban[24:]
    return iban

def yeni_hesap_ac():
    from fonksiyonlar import mevcut_hesap_dogrula
    from fatura import yeni_hesap_fatura_olustur
    connect = sqlite3.connect("kullanici_data.db")
    cursor = connect.cursor()
    kullanici_adi = input("Yeni hesap adinizi giriniz: ")
    
    cursor.execute("SELECT * FROM users WHERE kullanici_adi=?", (kullanici_adi,))
    result = cursor.fetchone()
    
    if result:
        print("Bu kullanici adi zaten kayitli! Lutfen baska bir kullanici adi seciniz.")
        connect.close()
        return yeni_hesap_ac()
    
    while True:
        sifre = input("Yeni sifrenizi giriniz: ")
        if not sifre_kontrol(sifre):
            print("Sifre uygun degil.")
        else:
            break
    sifre_hash = sifreli_parola(sifre)
    iban = iban_uret()
    cursor.execute("INSERT INTO users (kullanici_adi, sifre, bakiye, cep_bakiyesi, iban) VALUES (?, ?, ?, ?, ?)", (kullanici_adi, sifre_hash, 1000, 0, iban))
    connect.commit()
    
    # Yeni oluşturulan kullanıcının ID'sini al
    cursor.execute("SELECT id FROM users WHERE kullanici_adi=?", (kullanici_adi,))
    kullanici_id = cursor.fetchone()[0]
    connect.close()
    
    print("Kayit basarili")
    print("Bankamiza hos geldiniz! 1000TL hediye bonusunuz hesabiniza tanimlanmistir....")
    
    # Yeni hesap için otomatik olarak fatura oluştur
    yeni_hesap_fatura_olustur(kullanici_id)
    
    return mevcut_hesap_dogrula()