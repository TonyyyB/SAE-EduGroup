import tkinter as tk
from tkinter import ttk
from constantes import *
class PageAccueil(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Page d'accueil", font = GRANDE_POLICE)
        label.grid(row = 0, column = 4) 