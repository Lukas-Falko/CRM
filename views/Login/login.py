import customtkinter as ctk
import views.Login.dane as dane
from tkinter import messagebox




class LoginView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


        
    
        # Główny kontener
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=1, padx=1, fill="both", expand=True)

        # Centrowanie zawartości
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Panel formularza
        self.login_container = ctk.CTkFrame(self.main_frame, fg_color="gray20", corner_radius=15)
        self.login_container.grid(row=0, column=0, padx=20, pady=20)

        self.title_label = ctk.CTkLabel(self.login_container, text="Logowanie CRM", font=("Arial", 22, "bold"))
        self.title_label.pack(pady=(25, 15), padx=40)

        self.login_entry = ctk.CTkEntry(self.login_container, placeholder_text="Użytkownik", width=200)
        self.login_entry.pack(pady=10, padx=40)

        self.pass_entry = ctk.CTkEntry(self.login_container, placeholder_text="Hasło", show="*", width=200)
        self.pass_entry.pack(pady=10, padx=40)

        self.login_btn = ctk.CTkButton(self.login_container, text="Zaloguj", command=self._zaloguj)
        self.login_btn.pack(pady=(20, 25), padx=40)
    zaloguj = 0
    
    

    def _zaloguj(self):
                
        password = self.getPassword()

        login = self.getLogin()

        
         
        # IF | odpowiedzialny za logike logowania

        if dane.probyLogowania > 5:
            self.login_btn.configure(state="disabled", text="Blokada (3 min)")
            self.master.after(5000, self.odblokuj_przycisk) # 1000 = 1s
        else:
            pass


        # IF | czy haslo i login istnieja w okienkach

        if not login and not password: 
            self.pokaz_alert("Brak hasla i loginu")
            return
        if not login:
            self.pokaz_alert("Brak loginu")
        if not password:
            self.pokaz_alert("Brak hasla")


        # FOR IF | sprawdzanie czy login i haslo sie zgadzaja z danymi w bazie

        
        znalezionyUser = None

        for user in dane.baza_uzytkownikow:
            if user["login"] == login:
                znalezionyUser = user
                break
        

        if znalezionyUser is None:
            self.pokaz_alert("Błędny login lub hasło")
            dane.probyLogowania = dane.probyLogowania + 1

        else:
            if znalezionyUser["haslo"] == password:
                self.master.buduj_sidebar() 
                self.master.action_dashboard()
                self.pokaz_alert("Gratulacje zalogowano")
            else:
                self.pokaz_alert("Błędny login lub hasło")
                dane.probyLogowania = dane.probyLogowania + 1
        
    def getPassword(self):

        password = self.pass_entry.get()
        return password 
    
    def getLogin(self):

        login = self.login_entry.get()
        return login
    

    def pokaz_alert(self, alert):
    
        messagebox.showinfo(title="Alert", message=alert)
        
    def odblokuj_przycisk(self):
    
        self.login_btn.configure(state="normal", text="Zaloguj")
        self.pokaz_alert("Możesz spróbować ponownie")
        dane.probyLogowania = 0




        