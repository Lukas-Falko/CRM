# Plik: app_logic.py
from views.dashboard import DashboardView
from views.klienci import KlienciView
from views.ustawienia import UstawieniaView
from views.Scraper.scraper import ScraperView
import sys

class NavigationMixin:
    def przygotuj_widoki(self):
        
        self.views = {}
        
        self.views["dashboard"] = DashboardView(self, corner_radius=0, fg_color="transparent")
        self.views["klienci"] = KlienciView(self, corner_radius=0, fg_color="transparent")
        self.views["ustawienia"] = UstawieniaView(self, corner_radius=0, fg_color="transparent")
        self.views["scraper"] = ScraperView(self, corner_radius=0, fg_color="transparent")

    def show_view(self, name):
        for view in self.views.values():
            view.grid_forget()
        self.views[name].grid(row=0, column=1, sticky="nsew")

    def action_dashboard(self): self.show_view("dashboard")
    def action_clients(self):   self.show_view("klienci")
    def action_settings(self):  self.show_view("ustawienia")
    def action_scraper(self):   self.show_view("scraper")