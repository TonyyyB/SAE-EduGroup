import tkinter as tk
from tkinter import ttk
from constantes import *
from pages.page import Page

class CreationGroupe(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_label("instruction_text", 0.5, 0.1, "Création du groupe", font=GRANDE_POLICE)
        