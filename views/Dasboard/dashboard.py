import customtkinter as ctk

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
    
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=1, padx=1, fill="both", expand=True)       

        # Konfiguracja wag kolumn, żeby obie rozciągały się tak samo
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        # Lewa podramka (Kolumna 0)
        self.sub_frame = ctk.CTkFrame(self.main_frame, fg_color="gray20")
        self.sub_frame.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

        self.url_entry = ctk.CTkEntry(self.sub_frame, placeholder_text="https://example.com/data")
        self.url_entry.pack(pady=15, padx=30, fill="x")

        self.btn_right = ctk.CTkButton(self.sub_frame, text="Pobierz dane")
        self.btn_right.pack(pady=5, padx=5)

        

        # Prawa podramka (Kolumna 1)
        self.sub_frame2 = ctk.CTkFrame(self.main_frame, fg_color="gray25")
        self.sub_frame2.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")

        self.url_entry = ctk.CTkEntry(self.sub_frame2, placeholder_text="Wybierz folder lub plik...")
        self.url_entry.pack(pady=15, padx=30, fill="x")

        self.btn_right = ctk.CTkButton(self.sub_frame2, text="Wybierz folder")
        self.btn_right.pack(pady=5, padx=5)

       
        
       
        
          