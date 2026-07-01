import customtkinter as ctk
from datetime import datetime
from tkinter import filedialog
from . import logika


class   TgeView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


    
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=5, padx=5, fill="both", expand=True)     

        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self.main_frame, width=200, corner_radius=5)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Add padding to the sidebar frame itself
        self.sidebar.grid_configure(padx=(10, 5), pady=(10, 5))

        self.logo_label = ctk.CTkLabel(self.sidebar, text="TGE Scraper", font=("Helvetica", 20, "bold"))
        self.logo_label.pack(pady=20)

        self.start_label = ctk.CTkLabel(self.sidebar, text="Data początkowa:")
        self.start_label.pack(pady=(10, 4))

        self.entry_start = ctk.CTkEntry(self.sidebar, placeholder_text="DD-MM-YYYY")
        self.entry_start.pack(pady=5)
        self.entry_start.insert(0, datetime.now().strftime("%d-%m-%Y"))

        self.end_label = ctk.CTkLabel(self.sidebar, text="Data końcowa:")
        self.end_label.pack(pady=(10, 4))

        self.entry_end = ctk.CTkEntry(self.sidebar, placeholder_text="DD-MM-YYYY")
        self.entry_end.pack(pady=5)
        self.entry_end.insert(0, datetime.now().strftime("%d-%m-%Y"))
        # Pole i przycisk wyboru folderu zapisu wyników
        self.save_path_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Folder zapisu (opcjonalnie)")
        self.save_path_entry.pack(pady=5)

        self.browse_save_butt = ctk.CTkButton(self.sidebar, text="Wybierz folder zapisu", width=180,
                               command=lambda: logika.choose_save_path(self))
        self.browse_save_butt.pack(pady=(5, 15))

        self.btn_run = ctk.CTkButton(self.sidebar, text="Pobierz Dane", command=lambda: logika.start_scraping_thread(self))
        self.btn_run.pack(pady=30)

        self.status_label = ctk.CTkLabel(self.sidebar, text="Status: Gotowy", text_color="gray")
        self.status_label.pack(side="bottom", pady=20)

        # Main Area (Logi)
        self.log_frame = ctk.CTkFrame(self.main_frame)
        self.log_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.log_frame.grid_rowconfigure(0, weight=1)
        self.log_frame.grid_columnconfigure(0, weight=1)

        self.log_text = ctk.CTkTextbox(self.log_frame, font=("Consolas", 12))
        self.log_text.grid(row=0, column=0, sticky="nsew")
        self.log_text.configure(state="disabled")