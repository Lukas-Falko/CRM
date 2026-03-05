import customtkinter as ctk

class UstawieniaView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = ctk.CTkLabel(self, text="Ustawienia", font=("Arial", 24))
        self.label.pack(pady=20)

        self.switch = ctk.CTkSwitch(self, text="Powiadomienia e-mail")
        self.switch.pack(pady=10)