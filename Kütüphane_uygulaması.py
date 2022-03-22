import sqlite3
import string
import datetime 
import locale

locale.setlocale(locale.LC_ALL, '')

veritabani = sqlite3.connect("Kitaplar.sqlite")
veritabani_2 = sqlite3.connect("id.sqlite")

imlec = veritabani.cursor()
imlec_2 = veritabani_2.cursor()
imlec.execute("CREATE TABLE IF NOT EXISTS kitaplik (kitap_id INTEGER PRIMARY KEY, kitap_ismi, kitap_yazari, basim_yili, yayinevi, kitabin_durumu)")
imlec_2.execute("CREATE TABLE IF NOT EXISTS kullanicilar (id INTEGER PRIMARY KEY, isim, soyisim, sifre)")

id_no = 1
kitap_id_no = 1
secim_id = 0


def veritabanı_tarama():

    # Burda yazan kod uygulama her başlatıldığında veritabanlarını tarayıp en son hangi id de kaldığını buluyor ve kayıt işlemlerinde id numarasının tekrar 1 den başlamasını engelliyor.

    global id_no
    global kitap_id_no

    tarama_1 = []
    ekleme_1 = imlec.execute("SELECT kitap_id FROM kitaplik").fetchall()
    tarama_1 = tarama_1 + ekleme_1
    kitap_id_no = kitap_id_no + len(tarama_1) 

    tarama_2 = []
    ekleme_2 = imlec_2.execute("SELECT id FROM kullanicilar").fetchall()
    tarama_2 = tarama_2 + ekleme_2
    id_no = id_no + len(tarama_2)


def giris_ekrani():
    # Giriş ekranı açılıyor
    global id_no

    print("""

    *******HOŞGELDİNİZ*******

    [1] Yeni Kayıt
    [2] Giriş Yap
    [3] Yetkili Girişi
    [4] Çıkış

    """)

    try:
        giris = int(input("Yapmak istediğiniz işlemi seçiniz: "))
    except ValueError:
        print("Lütfen sadece menüdeki sayılardan birini giriniz!")  # Hata yakalama
        return

    def yeni_kayit(id,isim,soyisim,sifre):
        deger_gir_2 = "INSERT INTO kullanicilar VALUES ('{}', '{}', '{}', '{}')".format(id,isim,soyisim,sifre)  # Yeni kayıt oluşturuluyor.
        imlec_2.execute(deger_gir_2)
        veritabani_2.commit()
        
    if giris == 1:

        isim = str(input("İsminiz: "))  # İsim soyisim alınıyor.
        soyisim = str(input("Soyisminiz: "))

        try:
            sifre = int(input("Şifrenizi giriniz: "))
            sifre_kontrol = int(input("Şifrenizi tekrar giriniz: "))    
        except ValueError:
            print("Şifre harflerden oluşmamalıdır. Tekrar deneyiniz!")      # Şifrenin sadece sayılardan oluşabileceğini belirtiyor.
            return

        if sifre == sifre_kontrol:
            yeni_kayit(id_no, isim, soyisim, sifre)         # Şifreler aynıysa kayıt oluşturuluyor değilse uygulama kullanıcıyı uyarıyor.
            print("Kayıt oluşturuldu! Id numaranız: {}".format(id_no))

            id_no += 1
            giris_ekrani()
        
        else:
            print("Şifreler uyuşmuyor. Tekrar deneyiniz!")
        

    if giris == 2:

        # Giriş ekranı

        hesap_giris = []
        global secim_id

        try:
            id_giris = int(input("Id numaranızı giriniz: "))    # Sorgulama
            secim_id = secim_id + id_giris 
            sifre_giris = int(input("Şifrenizi giriniz: "))
        except ValueError:
            print("Lütfen tekrar deneyiniz!")
            return

        imlec_2.execute("SELECT * FROM kullanicilar WHERE id = '{}'".format(id_giris))      # Alınan id_giriş değişkeni veritabanında sorgulanıyor eğer varsa şifresini karşılaştırıyor
        hesap_giris = hesap_giris + imlec_2.fetchall()
        print(hesap_giris)
        
        if (int(hesap_giris[0][0]) == id_giris) and (int(hesap_giris[0][3]) == sifre_giris):    # Şifre sorgulama
            print("Hoşgeldin {}".format(hesap_giris[0][1]))
            ana_menu()

        elif (int(hesap_giris[0][0]) == id_giris) and (int(hesap_giris[0][3]) != sifre_giris):  # Şifre doğru değilse program kullanıcıyı uyarıyor
            print("Şifreniz yanlış!")
            
    if giris == 3:
        sifre = 123456789
        yetkili_sifre = int(input("Yetkili şifresini giriniz: "))   # Yetkili sayfasına giriş

        if sifre == yetkili_sifre:
            yetkili()

    if giris == 4:
        veritabani.close()
        veritabani_2.close()
        quit() 
      
def ana_menu():
    print("""
    
    ******* ANA MENÜ *******

    [1] Kitap alma
    [2] Kitap teslim
    [3] Ceza durumu
    [4] Çıkış
    
    """)

    try:
        ana_menu_kontrol = int(input("Yapmak istediğiniz işlemi seçiniz: "))    # Hata yakalama
    except ValueError:
        print("Lütfen sadece menüdeki sayılardan birini giriniz!")
        return

    if ana_menu_kontrol == 1:   # Kitap arama menüsüne geçiş yapılıyor. 
        arama_menusu()

    if ana_menu_kontrol == 2:

        print("Kitabın ön kapağının arkasında kitabın id numarası bulunmaktadır.")      # Kitap iadesi işlemleri yapılıyor
        iade = int(input("Teslim edilecek kitabın id numarası: "))
        kitap_durum_mevcut(iade)
        print("Teslim işlemi başarılı! Ana menüye dönmek için herhangi bir tuşa basınız.")
        input()
        ana_menu()

    if ana_menu_kontrol == 3:
        pass

    if ana_menu_kontrol == 4:
        veritabani.close()
        veritabani_2.close()
        quit()
        
def arama_menusu():

    # Kitap arama menüsü

    print("""
        
        Arama yöntemini seçiniz:

        [1] Kitabın ismine göre ara.
        [2] Kitabın yazarına göre ara.
        [3] Kitabın basım yılına göre ara.
        [4] Kitabın yayıneine göre ara.

        """)

    arama_kontrol = int(input("Yapmak istediğiniz değeri seçiniz: "))   # 4 çeşit kitap arama menüsü soruluyor

    if arama_kontrol == 1:
        arama_fonksiyonu("ismini")

    if arama_kontrol == 2:
        arama_fonksiyonu("yazarını")

    if arama_kontrol == 3:
        arama_fonksiyonu("basım yılını")

    if arama_kontrol == 4:
        arama_fonksiyonu("yayınevini")
        
def arama_fonksiyonu(aranacak):

    # Arama işlemi

    a = 0
    b = 1
    liste = []
    aranacak_kitap = input("Kitabın {} giriniz: ".format(aranacak))

    if aranacak == "ismini":
        bulunan = imlec.execute("SELECT * FROM kitaplik WHERE kitap_ismi = '{}'".format(aranacak_kitap)).fetchall()
    
    elif aranacak == "yazarını":
        bulunan = imlec.execute("SELECT * FROM kitaplik WHERE kitap_yazari = '{}'".format(aranacak_kitap)).fetchall()
    
    elif aranacak == "basım yılını":
        bulunan = imlec.execute("SELECT * FROM kitaplik WHERE basim_yili = '{}'".format(aranacak_kitap)).fetchall()
    
    elif aranacak == "yayınevini":
        bulunan = imlec.execute("SELECT * FROM kitaplik WHERE yayinevi = '{}'".format(aranacak_kitap)).fetchall()
        
    liste = liste + bulunan     # Sorgulanan kitaplar bir listeye atılıp kullanıcının ekranına yazdırılıyor
    print(liste)

    if len(liste) == 0:
        print("Aradığınız kitap bulunmamaktadır.")  # Kitap yoksa uyarılıyor
        return

    elif len(liste) > 0 :
        for i in range(len(liste)):
            print("Bulunan {} nolu kitap: {}".format(b, liste[a]))      # Bulunan her kitap for döngüsüne sokularak ekrana yazdırılıyor
            b += 1
            a += 1

        secim = int(input("Kaç nolu kitabı almak istersiniz: "))
        global secim_id

        kitap_durum_namevcut(liste[secim - 1][0])
        print("Kitap alma işlemi başarılı! Ana menüye dönmek için herhangi bir tuşa basınız!")
        input()
        ana_menu()

def yetkili():

    # Burada kitap eklenip kitap çıkarma işlemleri yapılıyor

    global kitap_id_no

    print("""

    [1] Kitap Ekle
    [2] Kitap Çıkar
    [3] Çıkış
    
    """)

    try:
        kontrol = int(input("İşlem seçiniz: "))
    except ValueError:
        print("Lütfen menüdeki sayılardan birini giriniz!")
        return

    def kitap_ekle(kitap_id,kitap_adi,kitap_yazari,basim_yili,yayinevi,durum):
        deger_gir = "INSERT INTO kitaplik VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(kitap_id,kitap_adi,kitap_yazari,basim_yili,yayinevi,durum)
        imlec.execute(deger_gir)
        veritabani.commit()
    
    if kontrol == 1:
        adet = int(input("Kaç adet kitap eklenecek: "))
        for i in range(adet):
            isim = str(input("Kitap ismi: "))
            yazar = str(input("Kitap yazarı: "))

            try:
                yil = int(input("Basım yılı: "))
            except ValueError:
                print("Lütfen basım yılını sayı biçiminde giriniz!")
                continue
            
            yayin = str(input("Yayınevi: "))
            durum = "mevcut"
            kitap_ekle(kitap_id_no,isim,yazar,yil,yayin,durum)
            kitap_id_no += 1
            i += 1

        yetkili()

    if kontrol == 2:
        cıkar = str(input("Çıkarılacak kitabın ismi: "))
        imlec.execute("SELECT * FROM kitaplik WHERE kitap_ismi = '{}'".format(cıkar))
        yazdır = imlec.fetchall()
        print(yazdır)

        print("""
        İşlemi onaylıyor musunuz?
        [1]EVET
        [2]HAYIR
        
        """)

        try:
            kontrol_1 = int(input("İşlem: "))
        except ValueError:
            print("Lütfen menüdeki sayılardan birini giriniz!")
            return

        if kontrol_1 == 1:
            imlec.execute("DELETE FROM kitaplik WHERE kitap_ismi = '{}'".format(cıkar))
            veritabani.commit()
            print("İşlem Başarılı! Yetkili sayfasına dönmek için herhangi bir tuşa basınız!")
            input()
            yetkili()
        if kontrol_1 == 2:
            yetkili()

    if kontrol == 3:
        giris_ekrani()

def kitap_durum_mevcut(id_numarası):

    # Kitap alındığında namevcut iade edildiğinde mevcut olduğunu ifade eden kod bloğu

    imlec.execute("UPDATE kitaplik SET kitabin_durumu = 'mevcut' WHERE kitap_id = {}".format(id_numarası))
    veritabani.commit()

def kitap_durum_namevcut(id_numarası):
    imlec.execute("UPDATE kitaplik SET kitabin_durumu = 'namevcut' WHERE kitap_id = {}".format(id_numarası))
    veritabani.commit()
    
veritabanı_tarama()
giris_ekrani()
     