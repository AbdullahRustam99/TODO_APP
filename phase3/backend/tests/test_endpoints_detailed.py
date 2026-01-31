"""
Detailed API Endpoint Verification Script

This script tests each API endpoint individually to verify functionality.
"""

import requests
import json
from datetime import datetime

# Base URL for the backend API
BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, method="GET", data=None, headers=None, expected_status=200, description=""):
    """Test a specific endpoint"""
    print(f"Testing {description} - {method} {endpoint}")

    try:
        url = f"{BASE_URL}{endpoint}"
        response = requests.request(method, url, json=data, headers=headers)

        print(f"  Status: {response.status_code} (Expected: {expected_status})")
        if response.status_code == expected_status:
            print(f"  Result: PASS")
            if response.content:  # Check if there's response content
                try:
                    print(f"  Response: {response.json()}")
                except:
                    print(f"  Response: {response.text[:100]}...")  # First 100 chars
            return True
        else:
            print(f"  Result: FAIL - {response.text}")
            return False
    except Exception as e:
        print(f"  Result: FAIL - Error: {e}")
        return False

def test_all_endpoints():
    """Test all API endpoints"""
    print("=" * 70)
    print("Detailed API Endpoint Verification")
    print("=" * 70)

    results = {}

    # Test 1: Health check endpoint
    results['health'] = test_endpoint("/", "GET", expected_status=200,
                                   description="Health Check")

    # Test 2: Documentation endpoint
    results['docs'] = test_endpoint("/docs", "GET", expected_status=200,
                                 description="API Documentation")

    # Test 3: Register a user first for authentication tests
    print("\n--- Setting up user for authentication tests ---")
    timestamp = str(int(datetime.now().timestamp()))
    user_data = {
        "email": f"testuser_{timestamp}@example.com",
        "password": "securepassword123",
        "name": f"Test User {timestamp}"
    }

    register_response = requests.post(f"{BASE_URL}/api/auth/register",
                                   json=user_data,
                                   headers={"Content-Type": "application/json"})

    if register_response.status_code == 201:
        register_result = register_response.json()
        token = register_result['token']
        user_id = register_result['user']['id']
        print(f"User registered successfully. Token: {token[:20]}..., User ID: {user_id}")
    else:
        print(f"Failed to register user: {register_response.status_code} - {register_response.text}")
        token = None
        user_id = None

    # Test 4: Authentication endpoints
    if token:
        auth_headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        # Test login with the same credentials
        login_data = {"email": user_data["email"], "password": user_data["password"]}
        results['auth_login'] = test_endpoint("/api/auth/login", "POST",
                                           data=login_data, expected_status=200,
                                           description="User Login")

        # Test logout
        results['auth_logout'] = test_endpoint("/api/auth/logout", "POST",
                                            headers={"Authorization": f"Bearer {token}"},
                                            expected_status=200,
                                            description="User Logout")

    # Test 5: Task endpoints (need to register another user and get a fresh token)
    print("\n--- Setting up user for task tests ---")
    timestamp2 = str(int(datetime.now().timestamp()))
    task_user_data = {
        "email": f"taskuser_{timestamp2}@example.com",
        "password": "securepassword123",
        "name": f"Task User {timestamp2}"
    }

    task_register_response = requests.post(f"{BASE_URL}/api/auth/register",
                                        json=task_user_data,
                                        headers={"Content-Type": "application/json"})

    if task_register_response.status_code == 201:
        task_user_result = task_register_response.json()
        task_token = task_user_result['token']
        task_user_id = task_user_result['user']['id']
        task_headers = {"Authorization": f"Bearer {task_token}", "Content-Type": "application/json"}
        print(f"Task user registered. Token: {task_token[:20]}..., User ID: {task_user_id}")
    else:
        print(f"Failed to register task user: {task_register_response.status_code}")
        task_token = None
        task_user_id = None
        task_headers = None

    # Test 6: Task CRUD operations
    if task_token and task_user_id and task_headers:
        # Create a task
        task_data = {
            "title": "Test Task for Endpoint Verification",
            "description": "This is a test task for endpoint verification",
            "completed": False
        }

        # Create task
        create_task_response = requests.post(f"{BASE_URL}/api/{task_user_id}/tasks",
                                          json=task_data, headers=task_headers)
        if create_task_response.status_code == 201:
            created_task = create_task_response.json()
            task_id = created_task['id']
            print(f"Task created with ID: {task_id}")

            # Test get all tasks
            results['get_all_tasks'] = test_endpoint(f"/api/{task_user_id}/tasks", "GET",
                                                  headers=task_headers, expected_status=200,
                                                  description="Get All Tasks")

            # Test get specific task
            results['get_task'] = test_endpoint(f"/api/{task_user_id}/tasks/{task_id}", "GET",
                                             headers=task_headers, expected_status=200,
                                             description="Get Specific Task")

            # Test update task
            update_data = {
                "title": "Updated Test Task",
                "description": "This is an updated test task",
                "completed": True
            }
            results['update_task'] = test_endpoint(f"/api/{task_user_id}/tasks/{task_id}", "PUT",
                                                data=update_data, headers=task_headers, expected_status=200,
                                                description="Update Task")

            # Test update task completion
            completion_data = {"completed": False}
            results['update_completion'] = test_endpoint(f"/api/{task_user_id}/tasks/{task_id}/complete", "PATCH",
                                                      data=completion_data, headers=task_headers, expected_status=200,
                                                      description="Update Task Completion")

            # Test delete task
            results['delete_task'] = test_endpoint(f"/api/{task_user_id}/tasks/{task_id}", "DELETE",
                                                headers=task_headers, expected_status=204,
                                                description="Delete Task")
        else:
            print(f"Failed to create task: {create_task_response.status_code} - {create_task_response.text}")
            # Mark all task tests as failed
            results['get_all_tasks'] = False
            results['get_task'] = False
            results['update_task'] = False
            results['update_completion'] = False
            results['delete_task'] = False
    else:
        print("Skipping task tests - no valid user/token")
        # Mark all task tests as failed
        results['get_all_tasks'] = False
        results['get_task'] = False
        results['update_task'] = False
        results['update_completion'] = False
        results['delete_task'] = False

    # Test 7: Test protected endpoint without authentication (should fail)
    results['unauthorized_access'] = test_endpoint(f"/api/{task_user_id if task_user_id else 1}/tasks", "GET",
                                                expected_status=401,  # Should be 401 Unauthorized
                                                description="Unauthorized Access (should fail)")

    # Test 8: Test with invalid token (should fail)
    invalid_headers = {"Authorization": "Bearer invalid_token_here", "Content-Type": "application/json"}
    results['invalid_token'] = test_endpoint(f"/api/{task_user_id if task_user_id else 1}/tasks", "GET",
                                          headers=invalid_headers, expected_status=401,
                                          description="Invalid Token (should fail)")

    print("\n" + "=" * 70)
    print("Endpoint Verification Results:")
    print("=" * 70)

    all_passed = True
    for endpoint, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"{endpoint:25}: {status}")
        if not result:
            all_passed = False

    print("=" * 70)
    print(f"Overall Result: {'ALL ENDPOINTS WORKING' if all_passed else 'SOME ENDPOINTS FAILED'}")
    print("=" * 70)

    return all_passed

if __name__ == "__main__":
    test_all_endpoints()