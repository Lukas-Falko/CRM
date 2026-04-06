
import requests
import csv
import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv


from . import daneScrap as ds
from . import scraper_logika as sl
from . import dane as d
load_dotenv()


def log_message(output_widget, message):
    """Directly update the output widget with a message"""
    if output_widget and message:
        output_widget.insert("end", f"{message.strip()}\n")
        output_widget.see("end")
        output_widget.update()


class data:
    headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124'}



class TGE:

    def fetch_site(self, url_entry, output_widget=None): 

        try:
            
            response = requests.get(url_entry, headers=data.headers, timeout=10)
            
            if response.status_code == 200:
                log_message(output_widget, "Connecting | Sukces! Strona pobrana.")
                return response
            elif response.status_code == 404:
                log_message(output_widget, "Connecting | Nie znaleziono strony (404).")
            elif response.status_code == 403:
                log_message(output_widget, "Connecting | Brak dostępu (403 - blokada).")
                
        except requests.exceptions.MissingSchema:
            
            log_message(output_widget, f"Błąd | Nieprawidłowy format URL: '{url_entry}'. Zapomniałeś o http://?")
        except requests.exceptions.ConnectionError:
            log_message(output_widget, f"Błąd | Nie można połączyć się z serwerem: {url_entry}")
        except Exception as e:
            log_message(output_widget, f"Wystąpił nieoczekiwany błąd: {e}")

        return None  # Zwracamy None, jeśli cokolwiek poszło nie tak
    
    def scrap_data(self, response, output_widget=None):
        
        firma_nazwa = ds.pobierz_firme(response, output_widget)
        
        data = ds.pobierz_date(response, output_widget)
        adres = ds.pobierz_adres(response, output_widget)
        miasto = ds.pobierz_miasto(response, output_widget)
        kraj = ds.pobierz_kraj(response, output_widget)
        telefon = ds.pobierz_telefon(response, output_widget)
        email = ds.pobierz_email(response, output_widget)
        strona = ds.pobierz_strona(response, output_widget)

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
    
    def zapisz_do_excel(self, pakiet, sciezka_folderu, output_widget=None):
        
        if not sciezka_folderu:

            log_message(output_widget, "Błąd: Nie wybrano folderu zapisu!")
            return

        sciezka_pliku = os.path.join(sciezka_folderu, "wyniki_scrapingu.xlsx")
        
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

            log_message(output_widget, f"Pomyślnie zapisano firmę do Excela: {pakiet['Nazwa']}")
            
        except Exception as e:
            log_message(output_widget, f"Błąd zapisu Excel: {e}")

    def zapisz_do_csv(self, pakiet, sciezka_folderu, output_widget=None):
        
        if not sciezka_folderu:
            log_message(output_widget, "Błąd: Nie wybrano folderu zapisu!")
            return

        
        sciezka_pliku = os.path.join(sciezka_folderu, "wyniki_scrapingu.csv")
        plik_istnieje = os.path.isfile(sciezka_pliku)

        try:
        
            with open(sciezka_pliku, mode='a', newline='', encoding='utf-8-sig') as plik:
                writer = csv.DictWriter(plik, fieldnames=pakiet.keys(), delimiter=';')

                # Nagłówek zapisujemy tylko raz na początku pliku
                if not plik_istnieje:
                    writer.writeheader()

                writer.writerow(pakiet)
                log_message(output_widget, f"Pomyślnie zapisano firmę: {pakiet['Nazwa']}")
        except Exception as e:
            log_message(output_widget, f"Błąd zapisu CSV: {e}")

    def sprawdz_polaczenie_z_baza(self, output_widget=None):

        db_config = {
            "host": os.getenv("DB_HOST"),
            "database": os.getenv("DB_DATABASE"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "port": os.getenv("DB_PORT")
        }

        conn = None
        log_message(output_widget, "\n--- TEST DOSTĘPU DO BAZY POSTGRESQL ---")
        
        try:

            conn = psycopg2.connect(**db_config)
                
            cur = conn.cursor()
            cur.execute('SELECT version();')
            db_version = cur.fetchone()
            
            log_message(output_widget, "✅ STATUS: POŁĄCZONO!")
            log_message(output_widget, f"✅ DOSTĘP: Przyznany dla użytkownika '{db_config['user']}'")
            log_message(output_widget, f"✅ INFO O SERWERZE: {db_version[0]}")
            
            cur.close()

        except Exception as e:
            log_message(output_widget, "❌ STATUS: BRAK DOSTĘPU!")
            log_message(output_widget, f"❌ POWÓD BŁĘDU: {e}")

        finally:
            if conn:
                conn.close()
                log_message(output_widget, "--- Koniec testu, połączenie zamknięte ---\n")

    def zapisz_dane_do_bazy(self, package, output_widget=None):

        
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
            log_message(output_widget, "Dane zapisane pomyślnie w tabeli Baza Firm!")

        except Exception as error:
            log_message(output_widget, f"Błąd podczas łączenia z bazą: {error}")

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

        

    def run(self, url_entry, check_csv, check_exel, check_dane, output_widget=None):


        # ------ [Pobierz stronę] ------ #
        response = self.fetch_site(url_entry, output_widget)
        if response is None:
            log_message(output_widget, "Błąd: Nie udało się pobrać strony. Przerwanie operacji.")
            return
        
        # ------ [Wyciągnij dane ze strony] ------ #
        pakiet = self.scrap_data(response, output_widget)
        if pakiet is None or all(v is None for v in pakiet.values()):
            log_message(output_widget, "Błąd: Nie udało się wyciągnąć danych ze strony.")
            return

        # ----- [Sprawdzanie czy dane mają być zapisane] ------ #
        def sprawdzanie():
            if check_csv == "on":
                log_message(output_widget, "Zapisano plik do cvs")
                self.zapisz_do_csv(pakiet, d.scrapingPath, output_widget)

            if check_exel == "on":
                log_message(output_widget, "Zapisano plik do Exela")
                self.zapisz_do_excel(pakiet, d.scrapingPath, output_widget)

            if check_dane == "on":
                log_message(output_widget, "Zapisywanie do bazy danych....")
                self.sprawdz_polaczenie_z_baza(output_widget)
                self.zapisz_dane_do_bazy(pakiet, output_widget)
        
        sprawdzanie()