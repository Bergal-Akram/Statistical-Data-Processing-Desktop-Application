import tkinter as tk
import pandas as pd
import numpy as np
from tkinter import ttk
from view.pages.univariee_page import UnivarieePage
from view.pages.bivariee_page import BivarieePage
from view.pages.acp_page import AcpPage
from view.pages.som_page import SOMPage


class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DSP APP")
        self.geometry("900x600")

        self.controller = None
        self.pages = {}

        self._create_menu()
        self._create_container()


    def set_controller(self, controller):
        self.controller = controller

    def _create_menu(self):
        menubar = tk.Menu(self)

        # File
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New File", command=lambda: self.controller.new_file())
        file_menu.add_command(label="Open CSV", command=lambda: self.controller.open_csv())
        file_menu.add_command(label="Save CSV", command=lambda: self.controller.save_csv())
        file_menu.add_command(label="Print PDF", command=lambda: self.controller.print_pdf())
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=lambda: self.controller.exit_app())
        menubar.add_cascade(label="Fichier", menu=file_menu)

        # Statistique univariée
        menubar.add_command(label="Statistique univariée", command=lambda: self.show_univariee_page())


        # Statistique bivariée
        menubar.add_command(label="Statistique bivariée", command=lambda: self.show_bivariee_page())


        # Statistique multivariée
        menubar.add_command(label="Statistique multivariée", command=lambda: self.show_acp_page())

        menubar.add_command(label="SOM Demo", command=lambda: self.show_som())


    
        self.config(menu=menubar)

    def _create_container(self):
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

    def show_univariee_page(self, data=None):
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # Use controller data if data is None
        if data is None and self.controller is not None and not self.controller.data.empty:
            data = self.controller.data
        
        page = UnivarieePage(self.container, self.controller, data)
        self.pages["univariee"] = page
        page.pack(fill="both", expand=True)
    

    def show_bivariee_page(self, data=None):
        for widget in self.container.winfo_children():
            widget.destroy()
        page = BivarieePage(self.container, self.controller, data=data)
        page.set_data(self.pages.get("univariee").data if "univariee" in self.pages else pd.DataFrame())
        self.pages["bivariee"] = page
        page.pack(fill="both", expand=True)

    def show_acp_page(self, data=None):
        """Show the ACP (PCA) page and automatically use data from Univariee page"""
        for widget in self.container.winfo_children():
            widget.destroy()
    
        # Get data from UnivarieePage if available
        if data is None and "univariee" in self.pages:
            data = self.pages["univariee"].data
    
        # Also update the controller’s main data reference
        if data is not None and not data.empty:
            self.controller.data = data
    
        # Create and show ACP page
        page = AcpPage(self.container, self.controller, data=data)
        page.set_data(data if data is not None else pd.DataFrame())
        self.pages["acp"] = page
        page.pack(fill="both", expand=True)
 

    
    def show_som(self):
        faces = {
            'Akram': np.array([0.1,0.2]),
            'ali': np.array([0.2,0.1]),
            'Houdhaifa': np.array([0.8,0.9]),
            'Anas': np.array([0.9,0.8])
        }

        # مسح كل محتويات container
        for widget in self.container.winfo_children():
            widget.destroy()

        som_page = SOMPage(self.container, faces)
        som_page.pack(fill="both", expand=True)
        self.pages["som"] = som_page
