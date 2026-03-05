import customtkinter as ctk

class KlienciView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = ctk.CTkLabel(self, text="Baza Klientów", font=("Arial", 24))
        self.label.pack(pady=20)

        # Pasek wyszukiwania
        self.search = ctk.CTkEntry(self, placeholder_text="Szukaj klienta...")
        self.search.pack(pady=10, padx=20, fill="x")

        # Przycisk
        self.btn_add = ctk.CTkButton(self, text="Dodaj Klienta", fg_color="green")
        self.btn_add.pack(pady=10)