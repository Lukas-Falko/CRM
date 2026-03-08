import customtkinter as ctk
from . import dashboard_logic as dl

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
    
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=1, padx=1, fill="both", expand=True)       

        # Konfiguracja wag kolumn, żeby obie rozciągały się tak samo
        self.main_frame.grid_columnconfigure(0, weight=1)
        #self.main_frame.grid_columnconfigure(1, weight=1)



        # Lewa podramka (Kolumna 0)
        self.sub_frame = ctk.CTkFrame(self.main_frame, fg_color="gray20")
        self.sub_frame.grid(
                            row=0, 
                            column=0, 
                            pady=10, 
                            padx=10, 
                            sticky="nsew"
        )


        online_status = dl.czy_online()
        
        # Tytuł
        self.label = ctk.CTkLabel(self.sub_frame, text="Status strony https://www.gramwzielone.pl", font=("Arial", 18, "bold"))
        self.label.pack(pady=(5, 5))

        self.url_entry = ctk.CTkEntry(self.sub_frame, placeholder_text=f"Status: {online_status}", state="normal")
        self.url_entry.pack(
                            pady=5, 
                            padx=5, 
                            fill="x"
        )

        
        

       
        
       
        
          