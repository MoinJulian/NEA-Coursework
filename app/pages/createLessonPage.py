import time
from tkinter import messagebox
from pages.createDashboardPage import createDashboardPage


def createLessonPage(tk, root, requests, session, lesson_id):
    """
    Create a lesson page where users answer questions.
    """
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()
    
    # Fetch lesson data
    response = requests.get(f"http://127.0.0.1:8000/v1/lessons/{lesson_id}", headers={
        "Authorization": f"Bearer {session.access_token}"
    })
    
    if response.status_code != 200:
        error_detail = response.json().get('detail', 'Failed to load lesson')
        messagebox.showerror("Error", error_detail)
        createDashboardPage(tk, root, requests, session)
        return
    
    data = response.json()
    lesson = data.get("lesson", {})
    hearts = data.get("hearts", 0)
    questions = lesson.get("questions", [])
    
    if not questions:
        messagebox.showerror("Error", "No questions found for this lesson")
        createDashboardPage(tk, root, requests, session)
        return
    
    # Track state
    state = {
        "current_index": 0,
        "incorrect_questions": [],
        "mistakes": 0,
        "start_time": time.time(),
        "hearts": hearts,
        "total_questions": len(questions),
        "answers_given": set()
    }
    
    def display_question():
        # Clear current widgets
        for widget in root.winfo_children():
            widget.destroy()
        
        # Check if we've completed all questions
        if state["current_index"] >= len(questions):
            # If there are incorrect questions, retry them
            if state["incorrect_questions"]:
                questions.clear()
                questions.extend(state["incorrect_questions"])
                state["incorrect_questions"] = []
                state["current_index"] = 0
                state["mistakes"] += 1
            else:
                # All questions answered correctly
                show_completion_screen()
                return
        
        question = questions[state["current_index"]]
        
        # Display hearts
        tk.Label(root, text=f"Hearts: {'❤️' * state['hearts']}", font=("Arial", 12)).pack(pady=5)
        
        # Display progress
        tk.Label(root, text=f"Question {state['current_index'] + 1} of {len(questions)}", font=("Arial", 10)).pack(pady=5)
        
        # Display question
        tk.Label(root, text=question["question_text"], font=("Arial", 14, "bold"), wraplength=350).pack(pady=20)
        
        # Display options
        selected_option = tk.StringVar()
        
        for option in question.get("options", []):
            tk.Radiobutton(
                root,
                text=option["option_text"],
                variable=selected_option,
                value=option["id"],
                font=("Arial", 11)
            ).pack(anchor="w", padx=50, pady=5)
        
        def submit_answer():
            if not selected_option.get():
                messagebox.showwarning("Warning", "Please select an answer")
                return
            
            # Submit answer to backend
            response = requests.post(
                f"http://127.0.0.1:8000/v1/lessons/{lesson_id}/questions/{question['id']}/answer",
                headers={"Authorization": f"Bearer {session.access_token}"},
                json={"selected_option_id": selected_option.get()}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("correct"):
                    messagebox.showinfo("Correct!", "Well done!")
                    state["current_index"] += 1
                    display_question()
                else:
                    # Wrong answer
                    state["hearts"] = result.get("hearts_remaining", state["hearts"])
                    correct_answer = result.get("correct_answer", {}).get("option_text", "Unknown")
                    messagebox.showerror("Incorrect", f"The correct answer is: {correct_answer}")
                    
                    # Check if hearts depleted
                    if state["hearts"] <= 0:
                        messagebox.showerror("Game Over", "You've run out of hearts! Lesson ended.")
                        createDashboardPage(tk, root, requests, session)
                        return
                    
                    # Add to incorrect questions if not already there
                    if question["id"] not in state["answers_given"]:
                        state["incorrect_questions"].append(question)
                        state["answers_given"].add(question["id"])
                    
                    state["current_index"] += 1
                    display_question()
            else:
                messagebox.showerror("Error", "Failed to submit answer")
        
        tk.Button(root, text="Submit Answer", command=submit_answer, bg="blue", fg="white").pack(pady=20)
    
    def show_completion_screen():
        # Clear window
        for widget in root.winfo_children():
            widget.destroy()
        
        # Calculate stats
        time_taken = int(time.time() - state["start_time"])
        accuracy = ((state["total_questions"] - len(state["incorrect_questions"])) / state["total_questions"]) * 100
        
        # Submit completion to backend
        response = requests.post(
            f"http://127.0.0.1:8000/v1/lessons/{lesson_id}/complete",
            headers={"Authorization": f"Bearer {session.access_token}"},
            json={
                "accuracy": accuracy,
                "time_taken": time_taken,
                "mistakes": state["mistakes"]
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            
            tk.Label(root, text="🎉 Lesson Complete!", font=("Arial", 16, "bold")).pack(pady=20)
            tk.Label(root, text=f"Accuracy: {accuracy:.1f}%", font=("Arial", 12)).pack(pady=5)
            tk.Label(root, text=f"XP Earned: {result.get('xp_earned', 0)}", font=("Arial", 12)).pack(pady=5)
            tk.Label(root, text=f"Time Taken: {time_taken}s", font=("Arial", 12)).pack(pady=5)
            tk.Label(root, text=f"New Streak: {result.get('new_streak', 0)} 🔥", font=("Arial", 12)).pack(pady=5)
            tk.Label(root, text=f"Total XP: {result.get('total_xp', 0)}", font=("Arial", 12)).pack(pady=5)
        else:
            tk.Label(root, text="Lesson complete, but failed to save results", font=("Arial", 12)).pack(pady=20)
        
        def back_to_dashboard():
            createDashboardPage(tk, root, requests, session)
        
        tk.Button(root, text="Back to Dashboard", command=back_to_dashboard, bg="green", fg="white").pack(pady=20)
    
    # Start displaying questions
    display_question()