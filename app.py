import customtkinter as ctk
import sys
sys.dont_write_bytecode = True
import views.Dasboard.dashboard_logic as dl
import views.Login.login as Login


from app_logic import NavigationMixin 

class Sidebar: 
    def buduj_sidebar(self):
        
        self.sidebar_frame = ctk.CTkFrame(self, width=100, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar_frame, text="CRM PRO", font=("Arial", 20, "bold"))
        self.logo.pack(pady=30)

        
        ctk.CTkButton(self.sidebar_frame, text="Dashboard", command=self.action_dashboard).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar_frame, text="Scraper", command=self.action_scraper).pack(pady=10, padx=20)

class App(ctk.CTk, Sidebar, NavigationMixin):
    
    def __init__(self):
        super().__init__()

        self.title("Mój System CRM")
        self.geometry("900x600")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        
        
        self.przygotuj_widoki() 
        #self.action_login() logika wywolujaca logowanie 
        self.buduj_sidebar() # zakomentuj jezeli uzywasz logiki login
        self.action_dashboard() 

if __name__ == "__main__":
    app = App()
    app.mainloop()