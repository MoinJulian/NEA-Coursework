import tkinter as tk
import requests
from pages.createLoginPage import createLoginPage
from session import Session
from pages.createRegisterPage import createRegisterPage
from pages.createDashboardPage import createDashboardPage

root = tk.Tk()
root.title("RuleShot™")
root.geometry("400x500")

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
        session = session or Session()  # Ensure session is not None
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
        session = session or Session()  # Ensure session is not None
    except AttributeError:
        print("session is not a Session instance:", session)
    if session.access_token:
        createDashboardPage(tk, root, requests, session)
    return session

def logout():
    global session
    session = Session()
    for widget in root.winfo_children():
        widget.destroy()
    tk.Label(root, text="Logged out successfully.").pack(pady=20)
    root.after(5000, main)  # Return to main after 5 seconds

def main():
    global root

    register_button = tk.Button(root, text="Register", command=register)
    register_button.pack(pady=20)

    login_button = tk.Button(root, text="Login", command=login)
    login_button.pack(pady=20)

main()

root.mainloop()