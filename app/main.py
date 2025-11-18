import tkinter as tk
from session import Session
from pages.createRegisterPage import createRegisterPage
from pages.createLoginPage import createLoginPage
from pages.createDashboardPage import createDashboardPage
from pages.createLessonPage import createLessonPage
from pages.createLeaderboardPage import createLeaderboardPage
from pages.createSettingsPage import createSettingsPage

# Create root window
root = tk.Tk()
root.title("RuleShot™")
root.geometry("800x600")

# Create session
session = Session()


def show_main_menu():
    """Show the main menu (login/register)"""
    # Clear window
    for widget in root.winfo_children():
        widget.destroy()
    
    # Title
    title_frame = tk.Frame(root)
    title_frame.pack(expand=True)
    
    tk.Label(title_frame, text="RuleShot™", font=("Arial", 24, "bold")).pack(pady=20)
    tk.Label(title_frame, text="Learn Golf Rules Through Practice", 
             font=("Arial", 12)).pack(pady=10)
    
    button_frame = tk.Frame(title_frame)
    button_frame.pack(pady=30)
    
    tk.Button(button_frame, text="Login", command=login, 
             width=20, height=2, font=("Arial", 12)).pack(pady=10)
    tk.Button(button_frame, text="Register", command=register, 
             width=20, height=2, font=("Arial", 12)).pack(pady=10)


def register():
    """Handle registration"""
    global session
    result = createRegisterPage(tk, root, session)
    if result and result.is_authenticated():
        session = result
        # After registration, user should login
        tk.messagebox.showinfo("Success", "Please login with your new account")
        show_main_menu()


def login():
    """Handle login"""
    global session
    result = createLoginPage(tk, root, session)
    if result and result.is_authenticated():
        session = result
        show_dashboard()


def show_dashboard():
    """Show the dashboard"""
    createDashboardPage(
        tk, root, session,
        on_logout=logout,
        on_settings=show_settings,
        on_start_lesson=start_lesson,
        on_view_leaderboard=show_leaderboard
    )


def start_lesson(lesson_id):
    """Start a lesson"""
    createLessonPage(
        tk, root, session, lesson_id,
        on_complete=show_dashboard
    )


def show_leaderboard():
    """Show the leaderboard"""
    createLeaderboardPage(tk, root, session, on_back=show_dashboard)


def show_settings():
    """Show settings page"""
    createSettingsPage(tk, root, session, on_back=show_dashboard)


def logout():
    """Handle logout"""
    global session
    session.logout()
    show_main_menu()


# Start with main menu
show_main_menu()

# Run the application
root.mainloop()
