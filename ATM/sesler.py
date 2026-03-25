import pyttsx3
from playsound import playsound

hosgeldiniz_global = True
islem_turu_global = True

def ses():
    playsound("sesler_resimler/bip.mp3")

def para_cek_ses():
    playsound("sesler_resimler/para_sayma.mp3")

def sesli_input(prompt=""):
    """Input girişi yapıldığında bip sesini çal"""
    while True:
        girdi = input(prompt)
        if girdi.strip():  # Boş olmayan giriş kontrol et
            ses()
            return girdi
        print("Hata: Lütfen bir değer giriniz!")

def hosgeldiniz():
    global hosgeldiniz_global
    if hosgeldiniz_global:
        ses_okuma = pyttsx3.init()#calıstır
        ses_okuma.setProperty('rate', 120) 
        ses_okuma.say("welcome to TURKBANK")#konustur
        ses_okuma.runAndWait()#durdur
        hosgeldiniz_global = False  #bir daha çalmasın

def islem_turu_konustur():
    global islem_turu_global
    if islem_turu_global:  #sadece ilk girişten sonra çalacak
        ses_okuma = pyttsx3.init()
        ses_okuma.setProperty('rate', 150) 
        ses_okuma.say("Please choose your transaction.")
        ses_okuma.runAndWait()
        islem_turu_global = False 

def hesap_dogrula_konustur():
    ses_okuma = pyttsx3.init()
    ses_okuma.setProperty('rate', 150) 
    ses_okuma.say("Verifying account information.")
    ses_okuma.runAndWait()

def pin_konustur():
    ses_okuma = pyttsx3.init()
    ses_okuma.setProperty('rate', 150) 
    ses_okuma.say("Please enter your PIN.")
    ses_okuma.runAndWait()