import tkinter as tk
import requests
from pages.createLoginPage import createLoginPage
from session import Session
from pages.createRegisterPage import createRegisterPage

session = Session()

def register():
    global session
    result = createRegisterPage(tk, root, requests, session)
    if result is None:
        # createRegisterPage probably mutated the passed session in-place
        print("createRegisterPage returned None; keeping existing session")
    else:
        session = result
    try:
        print(session.__dict__)  # Debug print to check session state
    except AttributeError:
        print("session is not a Session instance:", session)
    return session

def login():
    global session
    result = createLoginPage(tk, root, requests, session)
    if result is None:
        print("createLoginPage returned None; keeping existing session")
    else:
        session = result
    try:
        print(session.__dict__)  # Debug print to check session state
    except AttributeError:
        print("session is not a Session instance:", session)
    return session

root = tk.Tk()
root.title("RuleShot™")
root.geometry("400x300")

register_button = tk.Button(root, text="Register", command=register)
register_button.pack(pady=20)

login_button = tk.Button(root, text="Login", command=login)
login_button.pack(pady=20)

print(session.__dict__)  # Debug print to check session state

root.mainloop()