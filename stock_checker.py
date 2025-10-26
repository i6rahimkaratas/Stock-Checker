import requests
from bs4 import BeautifulSoup
import time
import json

class StokKontrol:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def sayfayi_getir(self):
        """Web sayfasını indirir"""
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Hata: Sayfa yüklenemedi - {e}")
            return None
    
    def stok_durumu_kontrol(self, html_content):
        """HTML içeriğinden stok durumunu çıkarır"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Yaygın stok göstergeleri
        stokta_kelimeler = ['stokta', 'in stock', 'available', 'mevcut', 'var']
        stok_yok_kelimeler = ['stok yok', 'out of stock', 'tükendi', 'unavailable', 'sold out']
        
        # Tüm metni küçük harfe çevir
        page_text = soup.get_text().lower()
        
        # Stok durumunu tespit et
        for kelime in stokta_kelimeler:
            if kelime in page_text:
                return "STOKTA VAR ✓"
        
        for kelime in stok_yok_kelimeler:
            if kelime in page_text:
                return "STOK YOK ✗"
        
        return "BELİRSİZ ?"
    
    def fiyat_bul(self, html_content):
        """Ürün fiyatını bulmaya çalışır"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Yaygın fiyat etiketleri
        fiyat_etiketleri = [
            {'class': 'price'},
            {'class': 'product-price'},
            {'itemprop': 'price'},
            {'class': 'sale-price'}
        ]
        
        for etiket in fiyat_etiketleri:
            fiyat = soup.find(attrs=etiket)
            if fiyat:
                return fiyat.get_text(strip=True)
        
        return "Bulunamadı"
    
    def kontrol_et(self):
        """Ana kontrol fonksiyonu"""
        print(f"\n{'='*60}")
        print(f"URL Kontrol Ediliyor: {self.url}")
        print(f"{'='*60}\n")
        
        response = self.sayfayi_getir()
        if not response:
            return
        
        stok_durumu = self.stok_durumu_kontrol(response.text)
        fiyat = self.fiyat_bul(response.text)
        
        print(f"Stok Durumu: {stok_durumu}")
        print(f"Fiyat: {fiyat}")
        print(f"\nKontrol Zamanı: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        return {
            'url': self.url,
            'stok': stok_durumu,
            'fiyat': fiyat,
            'zaman': time.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def surekli_kontrol(self, sure_dakika=5):
        """Belirtilen aralıklarla sürekli kontrol eder"""
        print(f"\n{sure_dakika} dakikada bir kontrol başlatılıyor...")
        print("Durdurmak için Ctrl+C basın\n")
        
        try:
            while True:
                self.kontrol_et()
                print(f"\nBir sonraki kontrol {sure_dakika} dakika sonra...")
                time.sleep(sure_dakika * 60)
        except KeyboardInterrupt:
            print("\n\nKontrol durduruldu.")


# KULLANIM ÖRNEKLERİ
if __name__ == "__main__":
    
    # Örnek 1: Tek seferlik kontrol
    print("ÖRNEK 1: Tek Kontrol")
    url = "https://www.example.com/urun-sayfasi"  # Buraya gerçek URL yazın
    kontrol = StokKontrol(url)
    kontrol.kontrol_et()
    
    # Örnek 2: Sürekli kontrol (yorumu kaldırarak aktif edin)
    # print("\nÖRNEK 2: Sürekli Kontrol")
    # kontrol.surekli_kontrol(sure_dakika=5)
    
    # Örnek 3: Birden fazla ürün kontrolü
    print("\n\nÖRNEK 3: Çoklu Ürün Kontrolü")
    urunler = [
        "https://www.example.com/urun1",
        "https://www.example.com/urun2",
    ]
    
    for url in urunler:
        kontrol = StokKontrol(url)
        kontrol.kontrol_et()
        time.sleep(2)  # Siteden ban yememek için bekleme