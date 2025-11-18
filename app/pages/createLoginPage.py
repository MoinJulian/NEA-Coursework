from tkinter import messagebox


def createLoginPage(tk, root, session):
    """Create login page supporting email or username"""
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("400x300")
    
    tk.Label(login_window, text="Email or Username:").pack(pady=5)
    identifier_entry = tk.Entry(login_window, width=30)
    identifier_entry.pack(pady=5)
    
    tk.Label(login_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*", width=30)
    password_entry.pack(pady=5)
    
    result = None
    
    def login():
        nonlocal result
        identifier = identifier_entry.get().strip()
        password = password_entry.get()
        
        try:
            # Login via API
            response = session.api_client.login(identifier, password)
            
            # Set user data in session
            session.set_user(response.get("user"))
            
            messagebox.showinfo("Success", "Login successful!")
            result = session
            login_window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}")
    
    tk.Button(login_window, text="Login", command=login, width=20).pack(pady=20)
    
    login_window.wait_window()
    return result
