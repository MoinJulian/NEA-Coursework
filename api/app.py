"""
Flask API for NEA Coursework Application
Provides endpoints for user authentication, lessons, leaderboard, and settings
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

# Import utilities
from utils.jwt_auth import generate_token, require_auth
from utils.password import hash_password, verify_password
from utils.validation import (
    validate_email, validate_password, normalize_email, validate_username
)
from utils.game_logic import (
    reset_hearts_if_needed, deduct_heart, update_streak, reset_streak,
    calculate_xp, add_xp
)
from connect import supabase
from scheduler import init_scheduler

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize the scheduler for daily resets
scheduler = init_scheduler()


@app.route("/register", methods=["POST"])
def register():
    """
    Register a new user
    
    Request body:
        - email: User's email
        - username: User's username (unique)
        - password: User's password
        - handicap: User's golf handicap (optional, default 0)
        
    Returns:
        - JWT token and user data on success
        - Error message on failure
    """
    try:
        data = request.get_json()
        
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
        handicap = data.get("handicap", 0)
        
        # Validate inputs
        if not email or not username or not password:
            return jsonify({"error": "Email, username, and password are required"}), 400
        
        # Normalize email
        email = normalize_email(email)
        
        # Validate email
        if not validate_email(email):
            return jsonify({"error": "Invalid email format"}), 400
        
        # Validate username
        is_valid_username, username_error = validate_username(username)
        if not is_valid_username:
            return jsonify({"error": username_error}), 400
        
        # Validate password
        is_valid_password, password_error = validate_password(password)
        if not is_valid_password:
            return jsonify({"error": password_error}), 400
        
        # Check if email already exists
        existing_email = supabase.table("users").select("*").eq("email", email).execute()
        if existing_email.data:
            return jsonify({"error": "Email already exists"}), 400
        
        # Check if username already exists
        existing_username = supabase.table("users").select("*").eq("username", username).execute()
        if existing_username.data:
            return jsonify({"error": "Username already exists"}), 400
        
        # Hash password
        password_hash = hash_password(password)
        
        # Create user
        user_data = {
            "email": email,
            "username": username,
            "password_hash": password_hash,
            "handicap": handicap,
            "xp": 0,
            "streak": 0,
            "hearts": 5,
            "last_heart_reset": datetime.now(timezone.utc).isoformat(),
            "deleted": False
        }
        
        response = supabase.table("users").insert(user_data).execute()
        
        if not response.data:
            return jsonify({"error": "Failed to create user"}), 500
        
        user = response.data[0]
        
        # Generate JWT token
        token = generate_token(user["id"], user["email"])
        
        return jsonify({
            "token": token,
            "user": {
                "id": user["id"],
                "email": user["email"],
                "username": user["username"],
                "handicap": user["handicap"],
                "xp": user["xp"],
                "streak": user["streak"],
                "hearts": user["hearts"]
            }
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/login", methods=["POST"])
def login():
    """
    Login a user with email/username and password
    
    Request body:
        - identifier: Email or username
        - password: User's password
        
    Returns:
        - JWT token and user data on success
        - Error message on failure
    """
    try:
        data = request.get_json()
        
        identifier = data.get("identifier")  # email or username
        password = data.get("password")
        
        if not identifier or not password:
            return jsonify({"error": "Email/username and password are required"}), 400
        
        # Try to find user by email or username
        # First normalize if it looks like an email
        if "@" in identifier:
            identifier = normalize_email(identifier)
            user_response = supabase.table("users").select("*").eq("email", identifier).execute()
        else:
            user_response = supabase.table("users").select("*").eq("username", identifier).execute()
        
        if not user_response.data:
            return jsonify({"error": "Invalid credentials"}), 401
        
        user = user_response.data[0]
        
        # Check if user is deleted
        if user.get("deleted"):
            return jsonify({"error": "Account has been deleted"}), 401
        
        # Verify password
        if not verify_password(password, user["password_hash"]):
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Reset hearts if needed
        user = reset_hearts_if_needed(user["id"])
        
        # Generate JWT token
        token = generate_token(user["id"], user["email"])
        
        return jsonify({
            "token": token,
            "user": {
                "id": user["id"],
                "email": user["email"],
                "username": user["username"],
                "handicap": user["handicap"],
                "xp": user["xp"],
                "streak": user["streak"],
                "hearts": user["hearts"]
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/user", methods=["GET"])
@require_auth
def get_user(current_user):
    """
    Get current user's profile
    
    Headers:
        - Authorization: Bearer <token>
        
    Returns:
        - User data on success
        - Error message on failure
    """
    try:
        user_id = current_user["user_id"]
        
        # Reset hearts if needed
        user = reset_hearts_if_needed(user_id)
        
        return jsonify({
            "user": {
                "id": user["id"],
                "email": user["email"],
                "username": user["username"],
                "handicap": user["handicap"],
                "xp": user["xp"],
                "streak": user["streak"],
                "hearts": user["hearts"]
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/lesson/<lesson_id>", methods=["GET"])
@require_auth
def get_lesson(current_user, lesson_id):
    """
    Get a specific lesson by ID
    
    Headers:
        - Authorization: Bearer <token>
        
    Returns:
        - Lesson data with questions
        - Error message on failure
    """
    try:
        user_id = current_user["user_id"]
        
        # Check user has hearts
        user = reset_hearts_if_needed(user_id)
        if user["hearts"] <= 0:
            return jsonify({"error": "No hearts remaining. Wait for daily reset."}), 403
        
        # Get lesson
        lesson_response = supabase.table("lessons").select("*").eq("id", lesson_id).execute()
        
        if not lesson_response.data:
            return jsonify({"error": "Lesson not found"}), 404
        
        lesson = lesson_response.data[0]
        
        return jsonify({
            "lesson": {
                "id": lesson["id"],
                "rule_number": lesson["rule_number"],
                "title": lesson["title"],
                "questions": lesson["questions"]
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/lesson/<lesson_id>", methods=["POST"])
@require_auth
def submit_lesson(current_user, lesson_id):
    """
    Submit lesson results
    
    Request body:
        - accuracy: Percentage accuracy (0-100)
        - mistakes_count: Number of retry rounds for incorrect answers
        - time_taken: Time taken in seconds
        
    Returns:
        - XP earned and updated user data
        - Error message on failure
    """
    try:
        user_id = current_user["user_id"]
        data = request.get_json()
        
        accuracy = data.get("accuracy")
        mistakes_count = data.get("mistakes_count", 0)
        time_taken = data.get("time_taken")
        
        if accuracy is None or time_taken is None:
            return jsonify({"error": "Accuracy and time_taken are required"}), 400
        
        # Calculate XP
        xp_gained = calculate_xp(10, mistakes_count)
        
        # Add XP to user
        user = add_xp(user_id, xp_gained)
        
        # Update streak
        user = update_streak(user_id)
        
        # Record completed lesson
        completed_data = {
            "user_id": user_id,
            "lesson_id": lesson_id,
            "accuracy": accuracy,
            "xp_gained": xp_gained,
            "time_taken": time_taken
        }
        
        supabase.table("completed_lessons").insert(completed_data).execute()
        
        return jsonify({
            "xp_gained": xp_gained,
            "user": {
                "id": user["id"],
                "email": user["email"],
                "username": user["username"],
                "handicap": user["handicap"],
                "xp": user["xp"],
                "streak": user["streak"],
                "hearts": user["hearts"]
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/lessons", methods=["GET"])
@require_auth
def get_lessons(current_user):
    """
    Get all available lessons
    
    Headers:
        - Authorization: Bearer <token>
        
    Returns:
        - List of lessons
        - Error message on failure
    """
    try:
        # Get all lessons, sorted by rule_number
        lessons_response = supabase.table("lessons").select("id, rule_number, title").order("rule_number").execute()
        
        return jsonify({
            "lessons": lessons_response.data
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/dashboard", methods=["GET"])
@require_auth
def get_dashboard(current_user):
    """
    Get dashboard data
    
    Returns:
        - next_lesson: Next lesson to complete
        - streak: Current streak
        - hearts: Current hearts
        - leaderboard_preview: Top 5 users
        - rules_completed: Number of lessons completed
    """
    try:
        user_id = current_user["user_id"]
        
        # Reset hearts if needed
        user = reset_hearts_if_needed(user_id)
        
        # Get completed lessons count
        completed_response = supabase.table("completed_lessons").select("lesson_id").eq("user_id", user_id).execute()
        completed_lesson_ids = [cl["lesson_id"] for cl in completed_response.data]
        rules_completed = len(set(completed_lesson_ids))
        
        # Get next lesson (first not completed)
        all_lessons = supabase.table("lessons").select("*").order("rule_number").execute()
        next_lesson = None
        for lesson in all_lessons.data:
            if lesson["id"] not in completed_lesson_ids:
                next_lesson = {
                    "id": lesson["id"],
                    "rule_number": lesson["rule_number"],
                    "title": lesson["title"]
                }
                break
        
        # Get leaderboard preview (top 5)
        leaderboard = supabase.table("users").select("username, xp").eq("deleted", False).order("xp", desc=True).limit(5).execute()
        
        return jsonify({
            "next_lesson": next_lesson,
            "streak": user["streak"],
            "hearts": user["hearts"],
            "leaderboard_preview": leaderboard.data,
            "rules_completed": rules_completed,
            "xp": user["xp"]
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/leaderboard", methods=["GET"])
@require_auth
def get_leaderboard(current_user):
    """
    Get leaderboard with pagination
    
    Query params:
        - skip: Number of records to skip (default 0)
        - limit: Number of records to return (default 50)
        
    Returns:
        - List of top users
        - Current user's rank
    """
    try:
        user_id = current_user["user_id"]
        
        skip = int(request.args.get("skip", 0))
        limit = int(request.args.get("limit", 50))
        
        # Get leaderboard
        leaderboard = supabase.table("users").select("id, username, xp").eq("deleted", False).order("xp", desc=True).range(skip, skip + limit - 1).execute()
        
        # Get current user's rank
        all_users = supabase.table("users").select("id, xp").eq("deleted", False).order("xp", desc=True).execute()
        
        user_rank = None
        for idx, u in enumerate(all_users.data):
            if u["id"] == user_id:
                user_rank = idx + 1
                break
        
        return jsonify({
            "leaderboard": leaderboard.data,
            "user_rank": user_rank
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/settings", methods=["PATCH"])
@require_auth
def update_settings(current_user):
    """
    Update user settings
    
    Request body:
        - email: New email (optional)
        - password: New password (optional)
        
    Returns:
        - Updated user data
        - Error message on failure
    """
    try:
        user_id = current_user["user_id"]
        data = request.get_json()
        
        update_data = {}
        
        # Update email if provided
        if "email" in data:
            new_email = normalize_email(data["email"])
            
            if not validate_email(new_email):
                return jsonify({"error": "Invalid email format"}), 400
            
            # Check if email already exists (for another user)
            existing = supabase.table("users").select("*").eq("email", new_email).execute()
            if existing.data and existing.data[0]["id"] != user_id:
                return jsonify({"error": "Email already exists"}), 400
            
            update_data["email"] = new_email
        
        # Update password if provided
        if "password" in data:
            new_password = data["password"]
            
            is_valid, error_msg = validate_password(new_password)
            if not is_valid:
                return jsonify({"error": error_msg}), 400
            
            update_data["password_hash"] = hash_password(new_password)
        
        if not update_data:
            return jsonify({"error": "No fields to update"}), 400
        
        # Update user
        response = supabase.table("users").update(update_data).eq("id", user_id).execute()
        
        if not response.data:
            return jsonify({"error": "Failed to update user"}), 500
        
        user = response.data[0]
        
        return jsonify({
            "user": {
                "id": user["id"],
                "email": user["email"],
                "username": user["username"],
                "handicap": user["handicap"],
                "xp": user["xp"],
                "streak": user["streak"],
                "hearts": user["hearts"]
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/settings", methods=["DELETE"])
@require_auth
def delete_account(current_user):
    """
    Delete user account (soft delete)
    
    Request body:
        - password: User's password for confirmation
        
    Returns:
        - Success message
        - Error message on failure
    """
    try:
        user_id = current_user["user_id"]
        data = request.get_json()
        
        password = data.get("password")
        
        if not password:
            return jsonify({"error": "Password confirmation required"}), 400
        
        # Get user
        user_response = supabase.table("users").select("*").eq("id", user_id).execute()
        
        if not user_response.data:
            return jsonify({"error": "User not found"}), 404
        
        user = user_response.data[0]
        
        # Verify password
        if not verify_password(password, user["password_hash"]):
            return jsonify({"error": "Invalid password"}), 401
        
        # Soft delete user
        supabase.table("users").update({"deleted": True}).eq("id", user_id).execute()
        
        return jsonify({"message": "Account deleted successfully"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/heart/deduct", methods=["POST"])
@require_auth
def deduct_heart_endpoint(current_user):
    """
    Deduct a heart from the user (called when answering wrong)
    
    Returns:
        - Updated hearts count
        - Error if no hearts remaining
    """
    try:
        user_id = current_user["user_id"]
        
        user = deduct_heart(user_id)
        
        return jsonify({
            "hearts": user["hearts"]
        }), 200
        
    except ValueError as e:
        # No hearts remaining - reset streak
        reset_streak(current_user["user_id"])
        return jsonify({"error": str(e), "streak_reset": True}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("FLASK_ENV", "production") == "development"
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
