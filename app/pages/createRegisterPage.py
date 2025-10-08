from tkinter import messagebox

def createRegisterPage(tk, root, requests, session):
    register_window = tk.Toplevel(root)
    register_window.title("Register")
    register_window.geometry("300x200")

    tk.Label(register_window, text="Email:").pack(pady=5)
    email_entry = tk.Entry(register_window)
    email_entry.pack(pady=5)

    tk.Label(register_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(register_window, show="*")
    password_entry.pack(pady=5)

    result = None

    def register():
        nonlocal result
        email = email_entry.get()
        password = password_entry.get()

        # use synchronous requests here
        response = requests.post("http://127.0.0.1:8000/v1/signup", json={
            "email": email,
            "password": password
        })

        if response.status_code == 200:
            messagebox.showinfo("Success", "Registration successful! You can now sign in.")
            session.email = email
            result = session
            register_window.destroy()
        else:
            messagebox.showerror("Error", f"Registration failed: {response.json().get('detail', 'Unknown error')}")

    tk.Button(register_window, text="Register", command=register).pack(pady=20)

    register_window.wait_window()
    return result