import sys


class NavigationMixin:

    def przygotuj_widoki(self):
        
        self.views = {}

    def _create_view(self, name):
        
        if name == "dashboard":
            from views.Dasboard.dashboard import DashboardView
            view = DashboardView(self, corner_radius=0, fg_color="transparent")
        elif name == "scraper":
            from views.Scraper.scraper import ScraperView
            view = ScraperView(self, corner_radius=0, fg_color="transparent")
        elif name == "tge":
            from views.TGE.tge import TgeView
            view = TgeView(self, corner_radius=0, fg_color="transparent")
        else:
            raise KeyError(f"Nieznany widok: {name}")

        self.views[name] = view
        return view

    def show_view(self, name):
        
        for view in list(self.views.values()):
            try:
                view.grid_forget()
            except Exception:
                pass

       
        view = self.views.get(name) or self._create_view(name)
        view.grid(row=0, column=1, sticky="nsew")

    def action_dashboard(self): self.show_view("dashboard")
    def action_scraper(self):   self.show_view("scraper")
    def action_tge(self): self.show_view("tge")