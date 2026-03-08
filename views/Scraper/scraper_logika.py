import threading
from . import gramZielone as gz
from . import scraper as sc
from tkinter import filedialog  # Dodane do obsługi okien wyboru plików

sciezka = None

def pobierzDane(url_entry, check_csv, chcek_exel):

    nowy_watek = threading.Thread(target=gz.run, args=(url_entry, check_csv, chcek_exel))
    nowy_watek.start()
    print("Scraper wystartowal w tle")


def wybierz_lokalizacje(entry_field):

    global sciezka
    
    
    wybor = filedialog.askdirectory()
    if wybor:
        sciezka = wybor
        print(f"Globalna sciezka to teraz: {sciezka}")

