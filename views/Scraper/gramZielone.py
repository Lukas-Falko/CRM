
import requests
import csv
import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv


from . import daneScrap as ds
from . import scraper_logika as sl
from . import gramZielone as gz


load_dotenv()


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
  
def zapisz_do_excel(pakiet, sciezka_folderu):
    if not sciezka_folderu:
        print("Błąd: Nie wybrano folderu zapisu!")
        return

    sciezka_pliku = os.path.join(sciezka_folderu, "wyniki_scrapingu.xlsx")
    
    # Tworzymy DataFrame z jednego wiersza (naszego pakietu)
    nowy_wiersz = pd.DataFrame([pakiet])

    try:
        if os.path.isfile(sciezka_pliku):
            # Jeśli plik istnieje, dopisujemy dane (append)
            with pd.ExcelWriter(sciezka_pliku, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                # Wczytujemy istniejący arkusz, aby znaleźć ostatni wiersz
                try:
                    istniejace_dane = pd.read_excel(sciezka_pliku)
                    start_row = len(istniejace_dane) + 1
                    # Zapisujemy bez nagłówka, zaczynając od nowego wiersza
                    nowy_wiersz.to_excel(writer, index=False, header=False, startrow=start_row)
                except Exception:
                    # W razie problemów z odczytem, nadpisujemy plik bezpiecznie
                    nowy_wiersz.to_excel(writer, index=False)
        else:
            # Jeśli plik nie istnieje, tworzymy go i zapisujemy nagłówki
            nowy_wiersz.to_excel(sciezka_pliku, index=False, engine='openpyxl')

        print(f"Pomyślnie zapisano firmę do Excela: {pakiet['Nazwa']}")
        
    except Exception as e:
        print(f"Błąd zapisu Excel: {e}")

def zapisz_do_csv(pakiet, sciezka_folderu):
    if not sciezka_folderu:
        print("Błąd: Nie wybrano folderu zapisu!")
        return

    
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

def sprawdz_polaczenie_z_baza():

    db_config = {
        "host": os.getenv("DB_HOST"),
        "database": os.getenv("DB_DATABASE"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "port": os.getenv("DB_PORT")
    }

    conn = None
    print("\n--- TEST DOSTĘPU DO BAZY POSTGRESQL ---")
    
    try:

        conn = psycopg2.connect(**db_config)
               
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()
        
        print("✅ STATUS: POŁĄCZONO!")
        print(f"✅ DOSTĘP: Przyznany dla użytkownika '{db_config['user']}'")
        print(f"✅ INFO O SERWERZE: {db_version[0]}")
        
        cur.close()

    except Exception as e:
        print("❌ STATUS: BRAK DOSTĘPU!")
        print(f"❌ POWÓD BŁĘDU: {e}")

    finally:
        if conn:
            conn.close()
            print("--- Koniec testu, połączenie zamknięte ---\n")

def zapisz_dane_do_bazy(package):

    
    connection_params = {
        "host": os.getenv("DB_HOST"),
        "database": os.getenv("DB_DATABASE"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "port": os.getenv("DB_PORT")
    }


    nazwa = package.get("Nazwa")
    data_dodania = package.get("Data")
    adres = package.get("Adres")
    miasto = package.get("Miasto")
    kraj = package.get("Kraj")
    tel = package.get("Telefon")
    mail = package.get("Email")
    www = package.get("Strona internetowa")


    try:
        # Nawiązanie połączenia
        connection = psycopg2.connect(**connection_params)
        cursor = connection.cursor()

        # Zapytanie SQL - nazwy kolumn muszą być takie jak na screenie!
        insert_query = """
        INSERT INTO "Baza Firm" (nazwa, data_dodania, adres, miasto, kraj, telefon, email, strona_www)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Wyciąganie wartości z obiektu w odpowiedniej kolejności
        values_to_insert = (
            package["Nazwa"],
            package["Data"],
            package["Adres"],
            package["Miasto"],
            package["Kraj"],
            package["Telefon"],
            package["Email"],
            package["Strona internetowa"]
        )

        # Wykonanie zapytania
        cursor.execute(insert_query, values_to_insert)
        
        # ZATWIERDZENIE ZMIAN (bardzo ważne w SQL!)
        connection.commit()
        print("Dane zapisane pomyślnie w tabeli Baza Firm!")

    except Exception as error:
        print(f"Błąd podczas łączenia z bazą: {error}")

    finally:
        if connection:
            cursor.close()
            connection.close()

    

def run(url_entry, check_csv, check_exel, check_dane):

    response = fetch_site(url_entry)
    pakiet = scrap_data(response)
    

    if check_csv == "on":
        print("Zapisano plik do cvs")
        zapisz_do_csv(pakiet, sl.sciezka)
    
    if check_exel == "on":
        print("Zapisano plik do Exela")
        zapisz_do_excel(pakiet, sl.sciezka )

    if check_dane == "on":
        print("Zapisywanie do bazy danych....")
        sprawdz_polaczenie_z_baza()
        zapisz_dane_do_bazy(pakiet)
        

           
    

  
    
    
 
    
 

