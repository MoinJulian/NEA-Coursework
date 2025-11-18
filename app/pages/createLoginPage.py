from tkinter import messagebox


def createLoginPage(tk, root, requests, session):
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("300x200")

    tk.Label(login_window, text="Email:").pack(pady=5)
    email_entry = tk.Entry(login_window)
    email_entry.pack(pady=5)

    tk.Label(login_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    result = None

    def login():
        nonlocal result
        email = email_entry.get()
        password = password_entry.get()

        response = requests.post("http://127.0.0.1:8000/v1/signin", json={
            "email": email,
            "password": password
        })

        if response.status_code == 200:
            messagebox.showinfo("Success", "Login successful!")
            data = response.json()
            session.email = email
            session.access_token = data.get("session", {}).get("access_token")
            session.refresh_token = data.get("session", {}).get("refresh_token")
            session.user_id = data.get("user", {}).get("id")
            session.profile = data.get("profile")
            result = session
            login_window.destroy()
        else:
            messagebox.showerror("Error", f"Login failed: {response.json().get('detail', 'Unknown error')}")

    tk.Button(login_window, text="Login", command=login).pack(pady=20)

    login_window.wait_window()
    return result