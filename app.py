
import customtkinter as ctk
import sys
sys.dont_write_bytecode = True


from app_logic import NavigationMixin 

class Sidebar: 
    def buduj_sidebar(self):
        
        self.sidebar_frame = ctk.CTkFrame(self, width=100, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar_frame, text="CRM PRO", font=("Arial", 20, "bold"))
        self.logo.pack(pady=30)

        
        ctk.CTkButton(self.sidebar_frame, text="Dashboard", command=self.action_dashboard).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar_frame, text="Klienci", command=self.action_clients).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar_frame, text="Ustawienia", command=self.action_settings).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar_frame, text="Scraper", command=self.action_scraper).pack(pady=10, padx=20)

class TkinterLogger:
    def __init__(self, app_instance):
        self.app = app_instance

    def write(self, message):
       
        if message and message.strip():
            
            scraper_view = self.app.views.get("scraper")
            
            if scraper_view and hasattr(scraper_view, "output_text"):
                
                scraper_view.output_text.after(0, 
                    lambda msg=message: self._update_ui(scraper_view.output_text, msg)
                )

    def _update_ui(self, textbox, msg):
        textbox.insert("end", f"{msg.strip()}\n")
        textbox.see("end")

    def flush(self):
        pass

class App(ctk.CTk, Sidebar, NavigationMixin):
    
    def __init__(self):
        super().__init__() 
        sys.stdout = TkinterLogger(self)

        self.title("Mój System CRM")
        self.geometry("900x600")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.przygotuj_widoki() 
        self.buduj_sidebar() 
        self.action_dashboard() 

if __name__ == "__main__":
    app = App()
    app.mainloop()