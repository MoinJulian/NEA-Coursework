def createDashboardPage(tk, root, requests, session):
    """
    Create an enhanced dashboard page showing user stats, next lesson, and leaderboard preview.
    """
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()
    
    # Fetch dashboard data
    response = requests.get("http://127.0.0.1:8000/v1/dashboard", headers={
        "Authorization": f"Bearer {session.access_token}"
    })
    
    if response.status_code != 200:
        tk.Label(root, text="Failed to load dashboard data.").pack(pady=20)
        return
    
    data = response.json()
    profile = data.get("profile", {})
    next_lesson = data.get("next_lesson")
    leaderboard_preview = data.get("leaderboard_preview", [])
    lessons_completed = data.get("lessons_completed", 0)
    
    # Title
    tk.Label(root, text=f"Welcome, {profile.get('username', 'User')}!", font=("Arial", 16, "bold")).pack(pady=10)
    
    # Stats frame
    stats_frame = tk.Frame(root)
    stats_frame.pack(pady=10)
    
    tk.Label(stats_frame, text=f"XP: {profile.get('xp', 0)}", font=("Arial", 12)).grid(row=0, column=0, padx=10)
    tk.Label(stats_frame, text=f"Streak: {profile.get('streak', 0)} 🔥", font=("Arial", 12)).grid(row=0, column=1, padx=10)
    tk.Label(stats_frame, text=f"Hearts: {'❤️' * profile.get('hearts', 0)}", font=("Arial", 12)).grid(row=0, column=2, padx=10)
    tk.Label(stats_frame, text=f"Lessons: {lessons_completed}", font=("Arial", 12)).grid(row=0, column=3, padx=10)
    
    # Next lesson
    if next_lesson:
        tk.Label(root, text="Next Lesson:", font=("Arial", 12, "bold")).pack(pady=(10, 5))
        tk.Label(root, text=next_lesson.get('title', 'Untitled')).pack()
        
        def start_lesson():
            from pages.createLessonPage import createLessonPage
            createLessonPage(tk, root, requests, session, next_lesson['id'])
        
        tk.Button(root, text="Start Lesson", command=start_lesson, bg="green", fg="white").pack(pady=10)
    else:
        tk.Label(root, text="🎉 All lessons completed!", font=("Arial", 12, "bold")).pack(pady=10)
    
    # Leaderboard preview
    tk.Label(root, text="Leaderboard Top 5:", font=("Arial", 12, "bold")).pack(pady=(10, 5))
    leaderboard_frame = tk.Frame(root)
    leaderboard_frame.pack()
    
    for i, entry in enumerate(leaderboard_preview[:5]):
        rank_text = f"{i+1}. {entry.get('username', 'Unknown')} - {entry.get('xp', 0)} XP"
        tk.Label(leaderboard_frame, text=rank_text).pack()
    
    def view_full_leaderboard():
        from pages.createLeaderboardPage import createLeaderboardPage
        createLeaderboardPage(tk, root, requests, session)
    
    tk.Button(root, text="View Full Leaderboard", command=view_full_leaderboard).pack(pady=10)
    
    # Logout button
    def logout():
        from session import Session
        global session
        session = Session()
        for widget in root.winfo_children():
            widget.destroy()
        # Return to main menu
        import main
        main.main()
    
    tk.Button(root, text="Logout", command=logout).pack(pady=10)
