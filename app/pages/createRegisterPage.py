from tkinter import messagebox

def createRegisterPage(tk, root, requests, session):
    register_window = tk.Toplevel(root)
    register_window.title("Register")
    register_window.geometry("300x350")

    tk.Label(register_window, text="Email:").pack(pady=5)
    email_entry = tk.Entry(register_window)
    email_entry.pack(pady=5)
    
    tk.Label(register_window, text="Username:").pack(pady=5)
    username_entry = tk.Entry(register_window)
    username_entry.pack(pady=5)
    
    tk.Label(register_window, text="Handicap:").pack(pady=5)
    handicap_entry = tk.Entry(register_window)
    handicap_entry.pack(pady=5)

    tk.Label(register_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(register_window, show="*")
    password_entry.pack(pady=5)

    result = None
    
    def register():
        nonlocal result
        email = email_entry.get()
        username = username_entry.get()
        handicap_str = handicap_entry.get()
        password = password_entry.get()
        
        if not email or not username or not handicap_str or not password:
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            handicap = int(handicap_str)
        except ValueError:
            messagebox.showerror("Error", "Handicap must be a number")
            return
        
        response = requests.post("http://127.0.0.1:8000/v1/signup", json={
            "email": email,
            "username": username,
            "handicap": handicap,
            "password": password
        })

        if response.status_code == 200:
            messagebox.showinfo("Success", "Registration successful! You can now sign in.")
            session.email = email
            result = session
            register_window.destroy()
        else:
            error_detail = response.json().get('detail', 'Unknown error')
            messagebox.showerror("Error", f"Registration failed: {error_detail}")

    tk.Button(register_window, text="Register", command=register).pack(pady=20)

    register_window.wait_window()
    return result