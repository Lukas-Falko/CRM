import threading
from . import gramZielone as gz
from . import scraper as sc
from tkinter import filedialog  # Dodane do obsługi okien wyboru plików
from . import dane


def log_message(output_widget, message):
    """Directly update the output widget with a message"""
    if output_widget and message:
        output_widget.insert("end", f"{message.strip()}\n")
        output_widget.see("end")
        output_widget.update()


def pobierzDane(url_entry, check_csv, chcek_exel, check_dane, output_widget=None):

    nowy_watek = threading.Thread(
    target=gz.run, 
    args=(url_entry, check_csv, chcek_exel, check_dane, output_widget) 
    )

    nowy_watek.start()
    
    if output_widget:
        log_message(output_widget, "Scraper wystartowal w tle")

def wybierz_lokalizacje(output_widget=None):
    

    wybor = filedialog.askdirectory()
    
    if wybor:
        dane.scrapingPath = wybor
                            
        if output_widget:
            log_message(output_widget, f"Globalna sciezka to teraz: {dane.scrapingPath}")
    else:
        if output_widget:
            log_message(output_widget, "brak ścieżki")

def wyczysc_konsole(textbox):
    textbox.delete("1.0", "end")