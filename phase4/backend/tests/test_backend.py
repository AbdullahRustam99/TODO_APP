"""
Backend API Test Suite for Todo List App Phase II

This test suite verifies all backend functionality including:
- Authentication endpoints (register, login, logout)
- Task management endpoints (CRUD operations)
- User management endpoints
- JWT authentication and authorization
- Database connectivity
"""

import requests
import json
from datetime import datetime

# Base URL for the backend API
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Health check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_register_user():
    """Test user registration"""
    print("Testing user registration...")
    try:
        # Generate unique email for testing
        timestamp = str(int(datetime.now().timestamp()))
        user_data = {
            "email": f"testuser_{timestamp}@example.com",
            "password": "securepassword123",
            "name": f"Test User {timestamp}"
        }

        response = requests.post(f"{BASE_URL}/api/auth/register",
                               json=user_data,
                               headers={"Content-Type": "application/json"})

        print(f"Registration: {response.status_code}")
        if response.status_code == 201:
            result = response.json()
            print(f"User registered successfully: {result['user']['email']}")
            return result['token'], result['user']['id']
        else:
            print(f"Registration failed: {response.status_code} - {response.text}")
            return None, None
    except Exception as e:
        print(f"Registration test failed: {e}")
        return None, None

def test_login_user():
    """Test user login"""
    print("Testing user login...")
    try:
        # First register a user to login with
        timestamp = str(int(datetime.now().timestamp()))
        register_data = {
            "email": f"login_test_{timestamp}@example.com",
            "password": "securepassword123",
            "name": f"Login Test {timestamp}"
        }

        register_response = requests.post(f"{BASE_URL}/api/auth/register",
                                       json=register_data,
                                       headers={"Content-Type": "application/json"})

        if register_response.status_code != 201:
            print(f"Failed to create test user for login: {register_response.status_code}")
            return None

        # Now try to login with the same credentials
        login_data = {
            "email": register_data["email"],
            "password": register_data["password"]
        }

        response = requests.post(f"{BASE_URL}/api/auth/login",
                               json=login_data,
                               headers={"Content-Type": "application/json"})

        print(f"Login: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"User logged in successfully: {result['user']['email']}")
            return result['token']
        else:
            print(f"Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Login test failed: {e}")
        return None

def test_task_crud_operations(token, user_id):
    """Test all task CRUD operations with authentication"""
    print("Testing task CRUD operations...")

    if not token:
        print("No valid token provided for task operations")
        return False

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Test 1: Create a task
    print("  Creating task...")
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False
    }

    try:
        response = requests.post(f"{BASE_URL}/api/{user_id}/tasks",
                               json=task_data,
                               headers=headers)

        print(f"  Create task: {response.status_code}")
        if response.status_code != 201:
            print(f"  Create task failed: {response.text}")
            return False

        created_task = response.json()
        task_id = created_task['id']
        print(f"  Task created with ID: {task_id}")

        # Test 2: Get all tasks for user
        print("  Getting all tasks...")
        response = requests.get(f"{BASE_URL}/api/{user_id}/tasks", headers=headers)
        print(f"  Get tasks: {response.status_code}")
        if response.status_code != 200:
            print(f"  Get tasks failed: {response.text}")
            return False

        tasks = response.json()
        print(f"  Retrieved {len(tasks)} tasks")

        # Test 3: Get specific task
        print("  Getting specific task...")
        response = requests.get(f"{BASE_URL}/api/{user_id}/tasks/{task_id}", headers=headers)
        print(f"  Get specific task: {response.status_code}")
        if response.status_code != 200:
            print(f"  Get specific task failed: {response.text}")
            return False

        retrieved_task = response.json()
        print(f"  Retrieved task: {retrieved_task['title']}")

        # Test 4: Update task
        print("  Updating task...")
        update_data = {
            "title": "Updated Test Task",
            "description": "This is an updated test task",
            "completed": True
        }

        response = requests.put(f"{BASE_URL}/api/{user_id}/tasks/{task_id}",
                              json=update_data,
                              headers=headers)
        print(f"  Update task: {response.status_code}")
        if response.status_code != 200:
            print(f"  Update task failed: {response.text}")
            return False

        updated_task = response.json()
        print(f"  Task updated: {updated_task['title']}")

        # Test 5: Update task completion status
        print("  Updating task completion status...")
        completion_data = {"completed": False}

        response = requests.patch(f"{BASE_URL}/api/{user_id}/tasks/{task_id}/complete",
                                json=completion_data,
                                headers=headers)
        print(f"  Update completion: {response.status_code}")
        if response.status_code != 200:
            print(f"  Update completion failed: {response.text}")
            return False

        completed_task = response.json()
        print(f"  Completion updated: {completed_task['completed']}")

        # Test 6: Delete task
        print("  Deleting task...")
        response = requests.delete(f"{BASE_URL}/api/{user_id}/tasks/{task_id}", headers=headers)
        print(f"  Delete task: {response.status_code}")
        if response.status_code != 204:
            print(f"  Delete task failed: {response.text}")
            return False

        print("  Task deleted successfully")
        return True

    except Exception as e:
        print(f"Task CRUD operations test failed: {e}")
        return False

def test_logout_user(token):
    """Test user logout"""
    print("Testing user logout...")
    if not token:
        print("No valid token provided for logout")
        return False

    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.post(f"{BASE_URL}/api/auth/logout", headers=headers)
        print(f"Logout: {response.status_code}")
        if response.status_code == 200:
            print("User logged out successfully")
            return True
        else:
            print(f"Logout failed: {response.text}")
            return False
    except Exception as e:
        print(f"Logout test failed: {e}")
        return False

def test_invalid_token():
    """Test API with invalid token"""
    print("Testing API with invalid token...")
    try:
        headers = {
            "Authorization": "Bearer invalid_token_here"
        }

        # Try to access a protected endpoint
        response = requests.get(f"{BASE_URL}/api/1/tasks", headers=headers)
        print(f"Invalid token test: {response.status_code}")
        # Should return 401 for invalid token
        return response.status_code == 401
    except Exception as e:
        print(f"Invalid token test failed: {e}")
        return False

def run_all_tests():
    """Run all backend tests"""
    print("=" * 60)
    print("Starting Backend API Tests")
    print("=" * 60)

    results = {}

    # Test 1: Health check
    results['health_check'] = test_health_check()

    # Test 2: User registration
    token, user_id = test_register_user()
    results['registration'] = token is not None

    # Test 3: User login
    login_token = test_login_user()
    results['login'] = login_token is not None

    # Test 4: Task CRUD operations (if we have a valid token from registration)
    if token and user_id:
        results['task_crud'] = test_task_crud_operations(token, user_id)
    else:
        results['task_crud'] = False
        print("Skipping task CRUD tests - no valid token from registration")

    # Test 5: Logout (if we have a valid login token)
    if login_token:
        results['logout'] = test_logout_user(login_token)
    else:
        results['logout'] = False
        print("Skipping logout test - no valid login token")

    # Test 6: Invalid token handling
    results['invalid_token'] = test_invalid_token()

    print("=" * 60)
    print("Test Results Summary:")
    print("=" * 60)

    all_passed = True
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"{test_name:20}: {status}")
        if not result:
            all_passed = False

    print("=" * 60)
    print(f"Overall Result: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    print("=" * 60)

    return all_passed

if __name__ == "__main__":
    run_all_tests()