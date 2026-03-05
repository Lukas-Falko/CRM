
import requests
from . import daneScrap as ds
from . import scraper_logika as sl
import csv
import os


from tkinter import filedialog



class data:
    headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124'}

def fetch_site(url_entry): 
    try:
        
        response = requests.get(url_entry, headers=data.headers, timeout=10)
        
        if response.status_code == 200:
            print("Connecting | Sukces! Strona pobrana.")
            return response
        elif response.status_code == 404:
            print("Connecting | Nie znaleziono strony (404).")
        elif response.status_code == 403:
            print("Connecting | Brak dostępu (403 - blokada).")
            
    except requests.exceptions.MissingSchema:
        print(f"Błąd | Nieprawidłowy format URL: '{url_entry}'. Zapomniałeś o http://?")
    except requests.exceptions.ConnectionError:
        print(f"Błąd | Nie można połączyć się z serwerem: {url_entry}")
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")

    return None  # Zwracamy None, jeśli cokolwiek poszło nie tak
   
def scrap_data(response):
    
    firma_nazwa = ds.pobierz_firme(response)
    
    data = ds.pobierz_date(response)
    adres = ds.pobierz_adres(response)
    miasto = ds.pobierz_miasto(response)
    kraj = ds.pobierz_kraj(response)
    telefon = ds.pobierz_telefon(response)
    email = ds.pobierz_email(response)
    strona = ds.pobierz_strona(response)

    return {
        "Nazwa": firma_nazwa,
        "Data": data,
        "Adres": adres,
        "Miasto": miasto,
        "Kraj": kraj,
        "Telefon": telefon,
        "Email": email,
        "Strona internetowa": strona,
    }
  
def zapisz_do_csv(pakiet, sciezka_folderu):
    if not sciezka_folderu:
        print("Błąd: Nie wybrano folderu zapisu!")
        return

    # Tworzymy pełną ścieżkę do pliku
    sciezka_pliku = os.path.join(sciezka_folderu, "wyniki_scrapingu.csv")
    plik_istnieje = os.path.isfile(sciezka_pliku)

    try:
        # 'utf-8-sig' sprawia, że polskie znaki dobrze wyglądają w Excelu
        with open(sciezka_pliku, mode='a', newline='', encoding='utf-8-sig') as plik:
            writer = csv.DictWriter(plik, fieldnames=pakiet.keys(), delimiter=';')

            # Nagłówek zapisujemy tylko raz na początku pliku
            if not plik_istnieje:
                writer.writeheader()

            writer.writerow(pakiet)
            print(f"Pomyślnie zapisano firmę: {pakiet['Nazwa']}")
    except Exception as e:
        print(f"Błąd zapisu CSV: {e}")

def run(url_entry):
    response = fetch_site(url_entry)
    pakiet = scrap_data(response)
    zapisz_do_csv(pakiet, sl.sciezka)
    
    
    

  
    
    
 
    
 

