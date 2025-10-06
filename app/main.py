import tkinter as tk
import requests
from session import Session
from pages.createRegisterPage import createRegisterPage

session = Session()

def register():
    session = createRegisterPage(tk, root, requests, session)
    print(session.__dict__)  # Debug print to check session state
    return session

root = tk.Tk()
root.title("RuleShot™")
root.geometry("400x300")

register_button = tk.Button(root, text="Register", command=register)
register_button.pack(pady=20)

print(session.__dict__)  # Debug print to check session state

root.mainloop()