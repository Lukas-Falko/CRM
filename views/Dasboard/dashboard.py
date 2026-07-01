import customtkinter as ctk
import threading
from . import dashboard_logic as dl


class DashboardView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # ======= FRAME GŁÓWNY ======= #
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=1, padx=1, fill="both", expand=True)

        self.main_frame.grid_columnconfigure(0, weight=1)

        # Lewa podramka (Kolumna 0)
        self.sub_frame = ctk.CTkFrame(self.main_frame, fg_color="gray20")
        self.sub_frame.grid(
            row=0,
            column=0,
            pady=10,
            padx=10,
            sticky="nsew",
        )

        
        self.label = ctk.CTkLabel(self.sub_frame, text="Status strony https://www.gramwzielone.pl", font=("Arial", 18, "bold"))
        self.label.pack(pady=(5, 5))

        
        self.url_entry = ctk.CTkEntry(self.sub_frame, placeholder_text="Status: sprawdzanie...", state="normal")
        self.url_entry.pack(pady=5, padx=5, fill="x")

        
        t = threading.Thread(target=self._check_online, daemon=True)
        t.start()

    def _check_online(self):
        
        try:
            status = dl.czy_online()
        except Exception:
            status = 0

       
        def _update():
            try:
                
                self.url_entry.delete(0, "end")
                self.url_entry.insert(0, f"Status: {status}")
            except Exception:
                pass

        try:
            self.after(0, _update)
        except Exception:
            pass
       
        
          





