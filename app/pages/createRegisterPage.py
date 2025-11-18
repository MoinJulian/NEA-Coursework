from tkinter import messagebox


def createRegisterPage(tk, root, session):
    """Create registration page with all required fields"""
    register_window = tk.Toplevel(root)
    register_window.title("Register")
    register_window.geometry("400x400")
    
    # Email
    tk.Label(register_window, text="Email:").pack(pady=5)
    email_entry = tk.Entry(register_window, width=30)
    email_entry.pack(pady=5)
    
    # Username
    tk.Label(register_window, text="Username:").pack(pady=5)
    username_entry = tk.Entry(register_window, width=30)
    username_entry.pack(pady=5)
    
    # Password
    tk.Label(register_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(register_window, show="*", width=30)
    password_entry.pack(pady=5)
    
    # Password requirements
    tk.Label(register_window, text="(Min 8 chars, 1 upper, 1 lower, 1 special)", 
             font=("Arial", 8), fg="gray").pack()
    
    # Handicap
    tk.Label(register_window, text="Golf Handicap (optional):").pack(pady=5)
    handicap_entry = tk.Entry(register_window, width=30)
    handicap_entry.insert(0, "0")
    handicap_entry.pack(pady=5)
    
    result = None
    
    def register():
        nonlocal result
        email = email_entry.get().strip()
        username = username_entry.get().strip()
        password = password_entry.get()
        
        try:
            handicap = int(handicap_entry.get())
        except ValueError:
            handicap = 0
        
        try:
            # Register via API
            response = session.api_client.register(email, username, password, handicap)
            
            # Set user data in session
            session.set_user(response.get("user"))
            
            messagebox.showinfo("Success", "Registration successful! You can now sign in.")
            result = session
            register_window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {str(e)}")
    
    tk.Button(register_window, text="Register", command=register, width=20).pack(pady=20)
    
    register_window.wait_window()
    return result
