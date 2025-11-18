import tkinter as tk
import requests
from pages.createLoginPage import createLoginPage
from session import Session
from pages.createRegisterPage import createRegisterPage

root = tk.Tk()
root.title("RuleShot™")
root.geometry("400x300")

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

        print(response.status_code, response.text)  # Debugging line

        if response.status_code == 200:
            user_data = response.json()
            tk.Label(root, text=f"Welcome, {user_data['user']['email']}!").pack(pady=20)

            tk.Button(root, text="Logout", command=logout).pack(pady=20)

            tk.Button(root, text="Settings", command=settings).pack(pady=20)
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
    root.after(5000, main)  # Return to main after 5 seconds

def settings():
    global session
    for widget in root.winfo_children():
        widget.destroy()

    result = None

    def load():
        nonlocal result
        response = requests.get("http://127.0.0.1:8000/v1/user", headers={
            "Authorization": f"Bearer {session.access_token}"
        })

        if response.status_code == 200:
            user_data = response.json()
            tk.Label(root, text="Email:").pack(pady=5)
            email_entry = tk.Entry(root)
            email_entry.insert(0, user_data['user']['email'])
            email_entry.pack(pady=5)

            tk.Label(root, text="Password:").pack(pady=5)
            password_entry = tk.Entry(root, show="*")
            password_entry.pack(pady=5)

            def update_settings():
                new_email = email_entry.get()
                new_password = password_entry.get()
                update_data = {}
                if new_email != user_data['user']['email']:
                    update_data['email'] = new_email
                if new_password:
                    update_data['password'] = new_password

                if update_data:
                    update_response = requests.put("http://127.0.0.1:8000/v1/user", headers={
                        "Authorization": f"Bearer {session.access_token}",
                    }, json=update_data)

                    print(update_response.json())

                    if update_response.status_code == 200:
                        tk.Label(root, text="Settings updated successfully!").pack(pady=20)
                    else:
                        tk.Label(root, text="Failed to update settings.").pack(pady=20)

            tk.Button(root, text="Update Settings", command=update_settings).pack(pady=20)

            result = session
        else:
            tk.Label(root, text="Failed to load user data. Please log in again.").pack(pady=20)
            result = None

    tk.Label(root, text="Settings Page").pack(pady=5)
    tk.Button(root, text="Back to Dashboard", command=dashboard).pack(pady=5)

    load()
    return result

def main():
    global root

    register_button = tk.Button(root, text="Register", command=register)
    register_button.pack(pady=20)

    login_button = tk.Button(root, text="Login", command=login)
    login_button.pack(pady=20)

main()

root.mainloop()