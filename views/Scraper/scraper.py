import customtkinter as ctk
from . import gramZielone as gz
from . import scraper_logika as sl


class ScraperView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        

        self.label = ctk.CTkLabel(self, text="Web Scraper Tool", font=("Arial", 24, "bold"))
        self.label.pack(pady=(20, 10))

        
        # --- SEKCJA WEJŚCIOWA (Input Frame) ---

        
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10, padx=20, fill="x")
    
        self.url_label = ctk.CTkLabel(self.input_frame, text="Adres URL do pobrania:")
        self.url_label.pack(pady=5, padx=10, anchor="w")

        self.url_entry = ctk.CTkEntry(self.input_frame, placeholder_text="https://example.com/data")
        self.url_entry.pack(pady=5, padx=10, fill="x")

        self.pobierz_butt = ctk.CTkButton(self.input_frame, text="Pobierz dane", 
        command=lambda: sl.pobierzDane(self.url_entry.get())) # lambda
        self.pobierz_butt.pack(pady=10, padx=10)


        # --- PRZYCISK WYBIERZ LOKALIZACJE ---
        self.path_container = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        self.path_container.pack(pady=5, padx=10, fill="x")

        self.path_entry = ctk.CTkEntry(self.path_container, placeholder_text="Wybierz folder lub plik...")
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.browse_butt = ctk.CTkButton(self.path_container, text="Przeglądaj", width=100, 
        command=lambda: sl.wybierz_lokalizacje(self.url_entry.get())) # lambda
        self.browse_butt.pack(pady=10, padx=10)
        
        # --- SEKCJA WYŚWIETLANIA DANYCH (Output Frame) ---

        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.output_label = ctk.CTkLabel(self.output_frame, text="Logi / Pobrane dane:")
        self.output_label.pack(pady=5, padx=10, anchor="w")

        
        self.output_text = ctk.CTkTextbox(self.output_frame, height=200)
        self.output_text.pack(pady=10, padx=10, fill="both", expand=True)



    