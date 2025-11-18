def createLeaderboardPage(tk, root, requests, session):
    """
    Create a leaderboard page showing all users sorted by XP.
    """
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="Leaderboard", font=("Arial", 16, "bold")).pack(pady=10)
    
    # Fetch leaderboard data
    response = requests.get("http://127.0.0.1:8000/v1/leaderboard?page=1&per_page=20", headers={
        "Authorization": f"Bearer {session.access_token}"
    })
    
    if response.status_code != 200:
        tk.Label(root, text="Failed to load leaderboard data.").pack(pady=20)
        return
    
    data = response.json()
    leaderboard = data.get("leaderboard", [])
    
    # Create a frame with scrollbar
    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Display leaderboard entries
    for i, entry in enumerate(leaderboard):
        rank_text = f"{i+1}. {entry.get('username', 'Unknown')} - {entry.get('xp', 0)} XP | Streak: {entry.get('streak', 0)}"
        tk.Label(scrollable_frame, text=rank_text, font=("Arial", 10)).pack(pady=2)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    def back_to_dashboard():
        from pages.createDashboardPage import createDashboardPage
        createDashboardPage(tk, root, requests, session)
    
    tk.Button(root, text="Back to Dashboard", command=back_to_dashboard).pack(pady=10)
