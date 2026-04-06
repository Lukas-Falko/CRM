# Plik: app_logic.py
from views.Dasboard.dashboard import DashboardView


from views.Scraper.scraper import ScraperView
import sys

class NavigationMixin:
    
    def przygotuj_widoki(self):
        
        self.views = {}
        
        self.views["dashboard"] = DashboardView(self, corner_radius=0, fg_color="transparent")
        self.views["scraper"] = ScraperView(self, corner_radius=0, fg_color="transparent")

    def show_view(self, name):
        for view in self.views.values():
            view.grid_forget()
        self.views[name].grid(row=0, column=1, sticky="nsew")

    def action_dashboard(self): self.show_view("dashboard")
    def action_scraper(self):   self.show_view("scraper")