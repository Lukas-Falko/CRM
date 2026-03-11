import customtkinter as ctk
from . import gramZielone as gz  # Zakładam, że są w tym samym folderze
from . import scraper_logika as sl

class ScraperView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Tytuł
        self.label = ctk.CTkLabel(self, text="Web Scraper Tool", font=("Arial", 24, "bold"))
        self.label.pack(pady=(20, 10))


       # Main frame 1
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(
        pady=5, 
        padx=5, 
        fill="both", 
        )       

        
        self.main_frame.grid_columnconfigure((0, 1), weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Lewa Kolumna - Parametry
        self.left_frame = ctk.CTkFrame(self.main_frame, fg_color="gray20")
        self.left_frame.grid(row=0, column=0, pady=10, padx=(10, 5), sticky="nsew")

        self.url_entry = ctk.CTkEntry(self.left_frame, placeholder_text="https://example.com/data")
        self.url_entry.pack(pady=(20, 10), padx=20, fill="x")

        self.btn_download = ctk.CTkButton(
        self.left_frame, 
        text="Pobierz dane", 
        fg_color="#2c73d2",
        command=lambda: sl.pobierzDane(
                                    self.url_entry.get(), 
                                    self.check_var_csv.get(), 
                                    self.check_var_exel.get(), 
                                    self.check_var_baza.get()
                                )
        )

        self.btn_download.pack(pady=10, padx=20)

        # Prawa kolumna - Lokalizacja
        self.right_frame = ctk.CTkFrame(self.main_frame, fg_color="gray25")
        self.right_frame.grid(row=0, column=1, pady=10, padx=(5, 10), sticky="nsew")

        self.path_entry = ctk.CTkEntry(self.right_frame, placeholder_text="Wybierz folder lub plik...")
        self.path_entry.pack(pady=(20, 10), padx=20, fill="x")

        self.browse_butt = ctk.CTkButton(
            self.right_frame, 
            text="Przeglądaj", 
            width=100, 
            command=lambda: sl.wybierz_lokalizacje(self.path_entry.get())
        )
        self.browse_butt.pack(pady=10, padx=20)

        # Main frame 2
        self.main_frame2 = ctk.CTkFrame(self)
        self.main_frame2.pack(
                            pady=5, 
                            padx=5, 
                            fill="both" 
        )   


        self.check_var_csv = ctk.StringVar(value="off")
        self.check_var_exel = ctk.StringVar(value="off")
        self.check_var_baza = ctk.StringVar(value="off")
 
        self.checkbox_exel = ctk.CTkCheckBox(self.main_frame2, 
                                        text="Exel",
                                        variable=self.check_var_exel,
                                        onvalue="on", 
                                        offvalue="off")
        self.checkbox_exel.pack(pady=10, padx=15, side = "left")

        self.checkbox_csv = ctk.CTkCheckBox(self.main_frame2, 
                                        text="CSV",
                                        variable=self.check_var_csv,
                                        onvalue="on", 
                                        offvalue="off")
        self.checkbox_csv.pack(pady=10, padx=15, side = "left")

        self.checkbox_baza = ctk.CTkCheckBox(self.main_frame2, 
                                        text="Baza danych",
                                        variable=self.check_var_baza,
                                        onvalue="on", 
                                        offvalue="off")
        self.checkbox_baza.pack(pady=10, padx=15, side = "left")


        self.check_connection_butt = ctk.CTkButton(
            self.main_frame2, 
            text="Sprawdz połączenie", 
            width=100, 
            command=lambda: gz.sprawdz_polaczenie_z_baza()
        )
        self.check_connection_butt.pack(pady=10, padx=15, side = "right")

        self.check_clear = ctk.CTkButton(
            self.main_frame2, 
            text="Wyczyść konsole", 
            width=100, 
            command= lambda: sl.wyczysc_konsole(self.output_text)
        )
        self.check_clear.pack(pady=10, padx=15, side = "right")


        
        
        # Main frame 3
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.pack(pady= 5, padx=5, fill="both", expand=True)



        self.output_label = ctk.CTkLabel(self.output_frame, text="Logi / Pobrane dane:", font=("Arial", 12, "italic"))
        self.output_label.pack(pady=(5, 0), padx=10, anchor="w")

        self.output_text = ctk.CTkTextbox(self.output_frame, height=200, text_color="lightgreen")
        self.output_text.pack(pady=10, padx=10, fill="both", expand=True)