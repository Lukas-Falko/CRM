import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import time
import pandas as pd
import threading
import customtkinter as ctk
from tkinter import messagebox
from . import scraping
from tkinter import filedialog


def log(self, message):
    """Bezpieczne dodawanie tekstu do okna logów.

    Aktualizacja jest schedulowana przez `after()` aby wykonać się w wątku GUI.
    """

    def _do():
        try:
            self.log_text.configure(state="normal")
            timestamp = datetime.now().strftime('%H:%M:%S')
            self.log_text.insert("end", f"[{timestamp}] {str(message)}\n")
            self.log_text.see("end")
            self.log_text.configure(state="disabled")
        except Exception:
            pass

    try:
        self.after(0, _do)
    except Exception:
        
        _do()


def start_scraping_thread(self):
    """Uruchamia proces w osobnym wątku"""
    start_date = self.entry_start.get()
    end_date = self.entry_end.get()

    self.btn_run.configure(state="disabled")
    self.status_label.configure(text="Status: Pracuję...", text_color="yellow")

    try:
        from types import MethodType
        if not hasattr(self, 'log') or not callable(getattr(self, 'log')):
            self.log = MethodType(log, self)
        if not hasattr(self, 'reset_ui') or not callable(getattr(self, 'reset_ui')):
            self.reset_ui = MethodType(reset_ui, self)
    except Exception:
    
        pass

   
    save_path = getattr(self, 'save_path', None)
    thread = threading.Thread(target=scraping.run_scraper, args=(self, start_date, end_date, save_path), daemon=True)
    thread.start()


def choose_save_path(self):
    """Otwiera dialog wyboru folderu i zapisuje ścieżkę w instancji oraz w polu entry."""
    try:
        wybor = filedialog.askdirectory()
        if wybor:
            self.save_path = wybor
            try:
                
                if hasattr(self, 'save_path_entry'):
                    self.save_path_entry.delete(0, 'end')
                    self.save_path_entry.insert(0, wybor)
            except Exception:
                pass
            # zaloguj wybór
            try:
                if hasattr(self, 'log') and callable(self.log):
                    self.log(f"Wybrano folder zapisu: {wybor}")
            except Exception:
                pass
        else:
            try:
                if hasattr(self, 'log') and callable(self.log):
                    self.log("Nie wybrano folderu zapisu.")
            except Exception:
                pass
    except Exception as e:
        try:
            if hasattr(self, 'log') and callable(self.log):
                self.log(f"Błąd przy wyborze folderu: {e}")
        except Exception:
            pass


def reset_ui(self):
    # Aktualizujemy UI w wątku głównym
    def _do():
        try:
            self.btn_run.configure(state="normal")
            self.status_label.configure(text="Status: Gotowy", text_color="gray")
        except Exception:
            pass

    try:
        self.after(0, _do)
    except Exception:
        _do()
