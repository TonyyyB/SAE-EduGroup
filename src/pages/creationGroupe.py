import tkinter as tk
from tkinter import ttk
from constantes import *
from pages.page import Page
from pages.page import Table

class CreationGroupe(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_label("instruction_text", 0.5, 0.1, "Création du groupe", font=GRANDE_POLICE)
        tableau = Table(self, controller, 500,4,["Nom","Type","Minimal","Maximal"])
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        tableau.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.5, relheight=0.5)