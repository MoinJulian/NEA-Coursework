"""
Dashboard page showing user stats, next lesson, and leaderboard preview
"""
from tkinter import messagebox


def createDashboardPage(tk, root, session, on_logout, on_settings, on_start_lesson, on_view_leaderboard):
    """
    Create dashboard page
    
    Args:
        tk: Tkinter module
        root: Root window
        session: Session object
        on_logout: Callback for logout
        on_settings: Callback for settings
        on_start_lesson: Callback for starting a lesson
        on_view_leaderboard: Callback for viewing leaderboard
    """
    # Clear the root window
    for widget in root.winfo_children():
        widget.destroy()
    
    try:
        # Get dashboard data
        data = session.api_client.get_dashboard()
        
        # Title
        title_frame = tk.Frame(root)
        title_frame.pack(pady=10)
        tk.Label(title_frame, text="RuleShot™ Dashboard", font=("Arial", 18, "bold")).pack()
        
        # User info frame
        user_frame = tk.Frame(root, relief=tk.RAISED, borderwidth=2)
        user_frame.pack(pady=10, padx=20, fill=tk.X)
        
        user = session.user
        tk.Label(user_frame, text=f"Welcome, {user.get('username')}!", font=("Arial", 14)).pack(pady=5)
        tk.Label(user_frame, text=f"Email: {user.get('email')}").pack()
        tk.Label(user_frame, text=f"Handicap: {user.get('handicap')}").pack()
        
        # Stats frame
        stats_frame = tk.Frame(root, relief=tk.RAISED, borderwidth=2)
        stats_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(stats_frame, text="Your Stats", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Create columns for stats
        stats_row = tk.Frame(stats_frame)
        stats_row.pack(pady=5)
        
        # XP
        xp_frame = tk.Frame(stats_row)
        xp_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(xp_frame, text="Total XP", font=("Arial", 10, "bold")).pack()
        tk.Label(xp_frame, text=str(data.get("xp", 0)), font=("Arial", 16)).pack()
        
        # Streak
        streak_frame = tk.Frame(stats_row)
        streak_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(streak_frame, text="Current Streak", font=("Arial", 10, "bold")).pack()
        tk.Label(streak_frame, text=f"{data.get('streak', 0)} days 🔥", font=("Arial", 16)).pack()
        
        # Hearts
        hearts_frame = tk.Frame(stats_row)
        hearts_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(hearts_frame, text="Hearts", font=("Arial", 10, "bold")).pack()
        hearts_count = data.get("hearts", 5)
        hearts_display = "❤️ " * hearts_count + "🤍 " * (5 - hearts_count)
        tk.Label(hearts_frame, text=hearts_display, font=("Arial", 14)).pack()
        
        # Rules completed
        completed_frame = tk.Frame(stats_row)
        completed_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(completed_frame, text="Rules Completed", font=("Arial", 10, "bold")).pack()
        tk.Label(completed_frame, text=str(data.get("rules_completed", 0)), font=("Arial", 16)).pack()
        
        # Next lesson frame
        lesson_frame = tk.Frame(root, relief=tk.RAISED, borderwidth=2)
        lesson_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(lesson_frame, text="Next Lesson", font=("Arial", 12, "bold")).pack(pady=5)
        
        next_lesson = data.get("next_lesson")
        if next_lesson:
            tk.Label(lesson_frame, text=f"Rule {next_lesson.get('rule_number')}: {next_lesson.get('title')}", 
                    font=("Arial", 11)).pack(pady=5)
            tk.Button(lesson_frame, text="Start Lesson", 
                     command=lambda: on_start_lesson(next_lesson.get('id')),
                     bg="#4CAF50", fg="white", font=("Arial", 11), width=15).pack(pady=10)
        else:
            tk.Label(lesson_frame, text="🎉 Congratulations! You've completed all lessons!", 
                    font=("Arial", 11)).pack(pady=10)
        
        # Leaderboard preview frame
        leaderboard_frame = tk.Frame(root, relief=tk.RAISED, borderwidth=2)
        leaderboard_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        tk.Label(leaderboard_frame, text="Leaderboard Top 5", font=("Arial", 12, "bold")).pack(pady=5)
        
        leaderboard_preview = data.get("leaderboard_preview", [])
        for idx, player in enumerate(leaderboard_preview, 1):
            player_text = f"{idx}. {player.get('username')} - {player.get('xp')} XP"
            tk.Label(leaderboard_frame, text=player_text).pack()
        
        tk.Button(leaderboard_frame, text="View Full Leaderboard", 
                 command=on_view_leaderboard,
                 font=("Arial", 10), width=20).pack(pady=10)
        
        # Bottom buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Settings", command=on_settings, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Logout", command=on_logout, width=15).pack(side=tk.LEFT, padx=5)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load dashboard: {str(e)}")
        on_logout()
