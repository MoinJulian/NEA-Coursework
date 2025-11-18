"""
Leaderboard page showing top players and user rank
"""
from tkinter import messagebox, ttk


def createLeaderboardPage(tk, root, session, on_back):
    """
    Create leaderboard page
    
    Args:
        tk: Tkinter module
        root: Root window
        session: Session object
        on_back: Callback to go back to dashboard
    """
    # Clear the root window
    for widget in root.winfo_children():
        widget.destroy()
    
    try:
        # Get leaderboard data
        data = session.api_client.get_leaderboard(skip=0, limit=50)
        leaderboard = data.get("leaderboard", [])
        user_rank = data.get("user_rank")
        
        # Title
        tk.Label(root, text="🏆 Leaderboard 🏆", font=("Arial", 18, "bold")).pack(pady=10)
        
        # User rank
        if user_rank:
            rank_frame = tk.Frame(root, relief=tk.RAISED, borderwidth=2, bg="#FFD700")
            rank_frame.pack(pady=10, padx=20, fill=tk.X)
            tk.Label(rank_frame, text=f"Your Rank: #{user_rank}", 
                    font=("Arial", 14, "bold"), bg="#FFD700").pack(pady=10)
        
        # Leaderboard table
        table_frame = tk.Frame(root)
        table_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Create Treeview for table
        columns = ("Rank", "Username", "XP")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Define headings
        tree.heading("Rank", text="Rank")
        tree.heading("Username", text="Username")
        tree.heading("XP", text="XP")
        
        # Define column widths
        tree.column("Rank", width=80, anchor=tk.CENTER)
        tree.column("Username", width=200, anchor=tk.W)
        tree.column("XP", width=100, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Populate table
        for idx, player in enumerate(leaderboard, 1):
            username = player.get("username", "Unknown")
            xp = player.get("xp", 0)
            
            # Highlight current user
            if player.get("id") == session.user.get("id"):
                tree.insert("", tk.END, values=(idx, username + " (You)", xp), tags=("current_user",))
            else:
                tree.insert("", tk.END, values=(idx, username, xp))
        
        # Tag configuration for current user
        tree.tag_configure("current_user", background="#E3F2FD")
        
        # Back button
        tk.Button(root, text="Back to Dashboard", command=on_back, 
                 font=("Arial", 12), width=20).pack(pady=20)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load leaderboard: {str(e)}")
        on_back()
