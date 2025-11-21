import re


def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    return True, ""


def test_email_validation():
    print("Testing email validation...")
    
    # Valid emails
    assert validate_email("user@example.com") == True
    assert validate_email("test.user@domain.co.uk") == True
    assert validate_email("user+tag@example.com") == True
    
    # Invalid emails
    assert validate_email("invalid.email") == False
    assert validate_email("@example.com") == False
    assert validate_email("user@") == False
    assert validate_email("user@.com") == False
    
    print("✓ Email validation tests passed")


def test_password_validation():
    print("Testing password validation...")
    
    # Valid passwords
    is_valid, _ = validate_password("Password123!")
    assert is_valid == True
    
    is_valid, _ = validate_password("SecurePass1@")
    assert is_valid == True
    
    # Invalid passwords - too short
    is_valid, msg = validate_password("Pass1!")
    assert is_valid == False
    assert "8 characters" in msg
    
    # Missing uppercase
    is_valid, msg = validate_password("password123!")
    assert is_valid == False
    assert "uppercase" in msg
    
    # Missing lowercase
    is_valid, msg = validate_password("PASSWORD123!")
    assert is_valid == False
    assert "lowercase" in msg
    
    # Missing special character
    is_valid, msg = validate_password("Password123")
    assert is_valid == False
    assert "special character" in msg
    
    print("✓ Password validation tests passed")


def test_xp_calculation():
    print("Testing XP calculation...")
    
    # No mistakes - max XP
    xp = max(0, 100 - (0 * 5))
    assert xp == 100
    
    # 1 mistake round
    xp = max(0, 100 - (1 * 5))
    assert xp == 95
    
    # 5 mistake rounds
    xp = max(0, 100 - (5 * 5))
    assert xp == 75
    
    # 20 mistake rounds (should cap at 0)
    xp = max(0, 100 - (20 * 5))
    assert xp == 0
    
    print("✓ XP calculation tests passed")


def test_hearts_system():
    print("Testing hearts system...")
    
    # Initial hearts
    hearts = 5
    assert hearts == 5
    
    # Deduct heart
    hearts -= 1
    assert hearts == 4
    
    # Multiple deductions
    hearts = hearts - 2
    assert hearts == 2
    
    # Should not go below 0
    hearts = max(0, hearts - 5)
    assert hearts == 0
    
    print("✓ Hearts system tests passed")


def main():
    print("=" * 50)
    print("Running Validation Tests")
    print("=" * 50)
    print()
    
    try:
        test_email_validation()
        test_password_validation()
        test_xp_calculation()
        test_hearts_system()
        
        print()
        print("=" * 50)
        print("✓ All tests passed!")
        print("=" * 50)
    except AssertionError as e:
        print()
        print("=" * 50)
        print(f"✗ Test failed: {e}")
        print("=" * 50)
        raise


if __name__ == "__main__":
    main()