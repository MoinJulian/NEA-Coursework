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
    dashboard()
    return session

def dashboard():
    global session
    # Delete the current window's contents
    for widget in root.winfo_children():
        widget.destroy()
    # Create the dashboard page
    result = None

    def load():
        nonlocal result
        response = requests.get("http://127.0.0.1:8000/v1/user", headers={
            "Authorization": f"Bearer {session.access_token}"
        })

        if response.status_code == 200:
            user_data = response.json()
            tk.Label(root, text=f"Welcome, {user_data['user']['email']}!").pack(pady=20)

            tk.Button(root, text="Logout", command=logout).pack(pady=20)
            result = session
        else:
            tk.Label(root, text="Failed to load user data. Please log in again.").pack(pady=20)
            result = None

    load()
    return result

def logout():
    global session
    session = Session()
    for widget in root.winfo_children():
        widget.destroy()
    tk.Label(root, text="Logged out successfully.").pack(pady=20)
    root.after(10000, root.quit)

root = tk.Tk()
root.title("RuleShot™")
root.geometry("400x300")

register_button = tk.Button(root, text="Register", command=register)
register_button.pack(pady=20)

login_button = tk.Button(root, text="Login", command=login)
login_button.pack(pady=20)

test_button = tk.Button(root, text="Test Session", command=lambda: print_session(session))
test_button.pack(pady=20)

def print_session(session):
    try:
        print(session.__dict__)  # Debug print to check session state
    except AttributeError:
        print("session is not a Session instance:", session)

root.mainloop()