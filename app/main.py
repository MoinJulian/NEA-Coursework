import tkinter as tk
import requests
from pages.createRegisterPage import createRegisterPage

root = tk.Tk()
root.title("RuleShot™")
root.geometry("400x300")

register_button = tk.Button(root, text="Register", command=lambda: createRegisterPage(tk, root, requests))
register_button.pack(pady=20)

root.mainloop()

