import threading
from . import gramZielone as gz
from . import scraper as sc
from tkinter import filedialog  # Dodane do obsługi okien wyboru plików
from . import dane



def pobierzDane(url_entry, check_csv, chcek_exel, check_dane):

    nowy_watek = threading.Thread(
    target=gz.run, 
    args=(url_entry,check_csv,chcek_exel,check_dane) 
    )

    nowy_watek.start()
    
    print("Scraper wystartowal w tle")

def wybierz_lokalizacje():
    

    wybor = filedialog.askdirectory()
    
    if wybor:
        dane.scrapingPath = wybor
                            
        print(f"Globalna sciezka to teraz: {dane.scrapingPath}")
    else:
        print(f"brak ścieżki")

def wyczysc_konsole(textbox):
    textbox.delete("1.0", "end")