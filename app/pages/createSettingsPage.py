"""
Settings page for updating email, password, and deleting account
"""
from tkinter import messagebox, simpledialog


def createSettingsPage(tk, root, session, on_back):
    """
    Create settings page
    
    Args:
        tk: Tkinter module
        root: Root window
        session: Session object
        on_back: Callback to go back to dashboard
    """
    # Clear the root window
    for widget in root.winfo_children():
        widget.destroy()
    
    # Title
    tk.Label(root, text="⚙️ Settings", font=("Arial", 18, "bold")).pack(pady=10)
    
    # User info
    user = session.user
    info_frame = tk.Frame(root, relief=tk.RAISED, borderwidth=2)
    info_frame.pack(pady=10, padx=40, fill=tk.X)
    
    tk.Label(info_frame, text="Current Information", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Label(info_frame, text=f"Username: {user.get('username')}").pack()
    tk.Label(info_frame, text=f"Email: {user.get('email')}").pack()
    tk.Label(info_frame, text=f"Handicap: {user.get('handicap')}").pack(pady=(0, 10))
    
    # Update email section
    email_frame = tk.Frame(root, relief=tk.RAISED, borderwidth=2)
    email_frame.pack(pady=10, padx=40, fill=tk.X)
    
    tk.Label(email_frame, text="Update Email", font=("Arial", 12, "bold")).pack(pady=10)
    
    tk.Label(email_frame, text="New Email:").pack()
    email_entry = tk.Entry(email_frame, width=30)
    email_entry.pack(pady=5)
    
    def update_email():
        new_email = email_entry.get().strip()
        
        if not new_email:
            messagebox.showwarning("Empty Field", "Please enter a new email")
            return
        
        try:
            result = session.api_client.update_settings(email=new_email)
            session.set_user(result.get("user"))
            messagebox.showinfo("Success", "Email updated successfully!")
            # Refresh the page
            createSettingsPage(tk, root, session, on_back)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update email: {str(e)}")
    
    tk.Button(email_frame, text="Update Email", command=update_email, width=15).pack(pady=10)
    
    # Update password section
    password_frame = tk.Frame(root, relief=tk.RAISED, borderwidth=2)
    password_frame.pack(pady=10, padx=40, fill=tk.X)
    
    tk.Label(password_frame, text="Update Password", font=("Arial", 12, "bold")).pack(pady=10)
    
    tk.Label(password_frame, text="New Password:").pack()
    password_entry = tk.Entry(password_frame, show="*", width=30)
    password_entry.pack(pady=5)
    
    tk.Label(password_frame, text="(Min 8 chars, 1 upper, 1 lower, 1 special)", 
             font=("Arial", 8), fg="gray").pack()
    
    def update_password():
        new_password = password_entry.get()
        
        if not new_password:
            messagebox.showwarning("Empty Field", "Please enter a new password")
            return
        
        try:
            result = session.api_client.update_settings(password=new_password)
            session.set_user(result.get("user"))
            messagebox.showinfo("Success", "Password updated successfully!")
            password_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update password: {str(e)}")
    
    tk.Button(password_frame, text="Update Password", command=update_password, width=15).pack(pady=10)
    
    # Delete account section
    delete_frame = tk.Frame(root, relief=tk.RAISED, borderwidth=2, bg="#FFEBEE")
    delete_frame.pack(pady=10, padx=40, fill=tk.X)
    
    tk.Label(delete_frame, text="⚠️ Danger Zone", font=("Arial", 12, "bold"), 
             bg="#FFEBEE", fg="#D32F2F").pack(pady=10)
    
    def delete_account():
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            "Are you sure you want to delete your account?\n\n"
            "This action cannot be undone!"
        )
        
        if not confirm:
            return
        
        # Ask for password confirmation
        password = simpledialog.askstring(
            "Password Confirmation",
            "Enter your password to confirm deletion:",
            show="*"
        )
        
        if not password:
            return
        
        try:
            session.api_client.delete_account(password)
            messagebox.showinfo("Account Deleted", "Your account has been deleted successfully.")
            session.logout()
            on_back()  # This should redirect to login/register screen
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete account: {str(e)}")
    
    tk.Button(delete_frame, text="Delete Account", command=delete_account, 
             bg="#D32F2F", fg="white", width=15).pack(pady=10)
    
    # Back button
    tk.Button(root, text="Back to Dashboard", command=on_back, 
             font=("Arial", 12), width=20).pack(pady=20)
