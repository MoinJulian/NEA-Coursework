"""
Lesson page with questions, answers, hearts, and progress tracking
"""
from tkinter import messagebox
import time


def createLessonPage(tk, root, session, lesson_id, on_complete):
    """
    Create lesson page
    
    Args:
        tk: Tkinter module
        root: Root window
        session: Session object
        lesson_id: ID of the lesson to take
        on_complete: Callback when lesson is complete
    """
    # Clear the root window
    for widget in root.winfo_children():
        widget.destroy()
    
    try:
        # Get lesson data
        lesson_data = session.api_client.get_lesson(lesson_id)
        lesson = lesson_data.get("lesson")
        
        questions = lesson.get("questions", [])
        
        # Lesson state
        current_question_idx = 0
        answers = []
        incorrect_indices = []
        hearts = session.user.get("hearts", 5)
        start_time = time.time()
        mistakes_count = 0
        in_retry_mode = False
        
        def show_question():
            """Display the current question"""
            nonlocal current_question_idx, in_retry_mode
            
            # Clear window
            for widget in root.winfo_children():
                widget.destroy()
            
            # If in retry mode, use incorrect_indices
            if in_retry_mode:
                if current_question_idx >= len(incorrect_indices):
                    # All incorrect questions answered correctly
                    show_results()
                    return
                q_idx = incorrect_indices[current_question_idx]
            else:
                if current_question_idx >= len(questions):
                    # First pass done, check if there are incorrect answers
                    check_for_retry()
                    return
                q_idx = current_question_idx
            
            question = questions[q_idx]
            
            # Title
            tk.Label(root, text=f"Rule {lesson.get('rule_number')}: {lesson.get('title')}", 
                    font=("Arial", 14, "bold")).pack(pady=10)
            
            # Progress bar
            progress_frame = tk.Frame(root)
            progress_frame.pack(pady=5)
            
            if in_retry_mode:
                progress_text = f"Retry {current_question_idx + 1} of {len(incorrect_indices)}"
            else:
                progress_text = f"Question {current_question_idx + 1} of {len(questions)}"
            tk.Label(progress_frame, text=progress_text).pack()
            
            # Hearts display
            hearts_display = "❤️ " * hearts + "🤍 " * (5 - hearts)
            tk.Label(root, text=f"Hearts: {hearts_display}", font=("Arial", 12)).pack(pady=5)
            
            # Question text
            question_frame = tk.Frame(root, relief=tk.RAISED, borderwidth=2)
            question_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
            
            tk.Label(question_frame, text=question.get("question"), 
                    font=("Arial", 12), wraplength=500, justify=tk.LEFT).pack(pady=20, padx=20)
            
            # Answer options (radio buttons)
            selected_answer = tk.IntVar()
            selected_answer.set(-1)
            
            options = question.get("options", [])
            for idx, option in enumerate(options):
                tk.Radiobutton(question_frame, text=option, variable=selected_answer, 
                              value=idx, font=("Arial", 11)).pack(anchor=tk.W, padx=40, pady=5)
            
            # Submit button
            def submit_answer():
                nonlocal current_question_idx, hearts, mistakes_count, in_retry_mode
                
                answer_idx = selected_answer.get()
                
                if answer_idx == -1:
                    messagebox.showwarning("No Answer", "Please select an answer")
                    return
                
                correct_answer_idx = question.get("correct_answer")
                
                if answer_idx == correct_answer_idx:
                    # Correct answer
                    messagebox.showinfo("Correct! ✓", "Great job!")
                    
                    if in_retry_mode:
                        # Remove from incorrect list (mark as correct)
                        pass
                    else:
                        answers.append(True)
                    
                    current_question_idx += 1
                    show_question()
                else:
                    # Wrong answer
                    correct_option = options[correct_answer_idx]
                    messagebox.showinfo("Incorrect ✗", 
                                      f"The correct answer is:\n\n{correct_option}")
                    
                    if not in_retry_mode:
                        answers.append(False)
                        incorrect_indices.append(q_idx)
                    
                    # Deduct heart
                    try:
                        result = session.api_client.deduct_heart()
                        hearts = result.get("hearts", hearts - 1)
                        session.user["hearts"] = hearts
                        
                        if hearts <= 0:
                            messagebox.showerror("No Hearts Left", 
                                               "You've run out of hearts! Your streak has been reset.\n"
                                               "Come back tomorrow for more hearts.")
                            on_complete()
                            return
                        
                    except Exception as e:
                        messagebox.showerror("Error", str(e))
                        on_complete()
                        return
                    
                    current_question_idx += 1
                    show_question()
            
            tk.Button(root, text="Submit Answer", command=submit_answer, 
                     bg="#2196F3", fg="white", font=("Arial", 12), width=20).pack(pady=20)
        
        def check_for_retry():
            """Check if there are incorrect answers to retry"""
            nonlocal current_question_idx, in_retry_mode, mistakes_count
            
            if incorrect_indices:
                # There are incorrect answers, enter retry mode
                in_retry_mode = True
                current_question_idx = 0
                mistakes_count += 1
                
                messagebox.showinfo("Retry Incorrect Answers", 
                                  f"You got {len(incorrect_indices)} questions wrong.\n"
                                  f"Let's retry them until you get them all correct!")
                
                # Clear incorrect_indices for this retry round
                temp_incorrect = incorrect_indices.copy()
                incorrect_indices.clear()
                
                # Update incorrect_indices with the ones to retry
                incorrect_indices.extend(temp_incorrect)
                
                show_question()
            else:
                # All correct, show results
                show_results()
        
        def show_results():
            """Show lesson completion results"""
            # Clear window
            for widget in root.winfo_children():
                widget.destroy()
            
            # Calculate metrics
            end_time = time.time()
            time_taken = int(end_time - start_time)
            correct_count = sum(answers)
            total_questions = len(questions)
            accuracy = (correct_count / total_questions) * 100 if total_questions > 0 else 0
            
            # Submit results to API
            try:
                result = session.api_client.submit_lesson(
                    lesson_id, 
                    accuracy, 
                    mistakes_count,
                    time_taken
                )
                
                xp_gained = result.get("xp_gained", 0)
                updated_user = result.get("user")
                session.set_user(updated_user)
                
                # Display results
                tk.Label(root, text="Lesson Complete! 🎉", font=("Arial", 18, "bold")).pack(pady=20)
                
                results_frame = tk.Frame(root, relief=tk.RAISED, borderwidth=2)
                results_frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
                
                tk.Label(results_frame, text=f"Accuracy: {accuracy:.1f}%", 
                        font=("Arial", 14)).pack(pady=10)
                tk.Label(results_frame, text=f"XP Earned: {xp_gained}", 
                        font=("Arial", 14)).pack(pady=10)
                tk.Label(results_frame, text=f"Time Taken: {time_taken} seconds", 
                        font=("Arial", 14)).pack(pady=10)
                tk.Label(results_frame, text=f"Mistakes Rounds: {mistakes_count}", 
                        font=("Arial", 14)).pack(pady=10)
                
                # Updated stats
                stats_frame = tk.Frame(root)
                stats_frame.pack(pady=20)
                
                tk.Label(stats_frame, text="Updated Stats:", font=("Arial", 12, "bold")).pack()
                tk.Label(stats_frame, text=f"Total XP: {updated_user.get('xp')}").pack()
                tk.Label(stats_frame, text=f"Streak: {updated_user.get('streak')} days 🔥").pack()
                tk.Label(stats_frame, text=f"Hearts: {updated_user.get('hearts')} ❤️").pack()
                
                tk.Button(root, text="Back to Dashboard", command=on_complete, 
                         bg="#4CAF50", fg="white", font=("Arial", 12), width=20).pack(pady=20)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to submit lesson: {str(e)}")
                on_complete()
        
        # Start the lesson
        show_question()
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load lesson: {str(e)}")
        on_complete()
