"""
Final Comprehensive API Test

This test verifies the complete workflow of the Todo List API.
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_complete_workflow():
    print("Testing Complete API Workflow")
    print("=" * 50)

    # 1. Register a new user
    print("1. Registering new user...")
    timestamp = str(int(datetime.now().timestamp()))
    user_data = {
        "email": f"workflow_test_{timestamp}@example.com",
        "password": "securepassword123",
        "name": f"Workflow Test {timestamp}"
    }

    response = requests.post(f"{BASE_URL}/api/auth/register",
                           json=user_data,
                           headers={"Content-Type": "application/json"})

    if response.status_code != 201:
        print(f"   FAILED: Registration failed with status {response.status_code}")
        return False

    result = response.json()
    token = result['token']
    user_id = result['user']['id']
    print(f"   SUCCESS: User {result['user']['email']} registered with ID {user_id}")

    # 2. Login with the same user
    print("2. Logging in user...")
    login_data = {
        "email": user_data['email'],
        "password": user_data['password']
    }

    response = requests.post(f"{BASE_URL}/api/auth/login",
                           json=login_data,
                           headers={"Content-Type": "application/json"})

    if response.status_code != 200:
        print(f"   FAILED: Login failed with status {response.status_code}")
        return False

    result = response.json()
    new_token = result['token']
    print(f"   SUCCESS: User logged in successfully")

    # 3. Create multiple tasks
    print("3. Creating tasks...")
    headers = {
        "Authorization": f"Bearer {new_token}",
        "Content-Type": "application/json"
    }

    tasks_to_create = [
        {"title": "First Task", "description": "This is the first task", "completed": False},
        {"title": "Second Task", "description": "This is the second task", "completed": True},
        {"title": "Third Task", "description": "This is the third task", "completed": False}
    ]

    created_tasks = []
    for i, task_data in enumerate(tasks_to_create):
        response = requests.post(f"{BASE_URL}/api/{user_id}/tasks",
                               json=task_data,
                               headers=headers)

        if response.status_code != 201:
            print(f"   FAILED: Creating task {i+1} failed with status {response.status_code}")
            return False

        task = response.json()
        created_tasks.append(task)
        print(f"   SUCCESS: Task '{task['title']}' created with ID {task['id']}")

    # 4. Get all tasks
    print("4. Retrieving all tasks...")
    response = requests.get(f"{BASE_URL}/api/{user_id}/tasks", headers=headers)

    if response.status_code != 200:
        print(f"   FAILED: Getting tasks failed with status {response.status_code}")
        return False

    tasks = response.json()
    print(f"   SUCCESS: Retrieved {len(tasks)} tasks")

    # 5. Get specific task
    print("5. Retrieving specific task...")
    first_task_id = created_tasks[0]['id']
    response = requests.get(f"{BASE_URL}/api/{user_id}/tasks/{first_task_id}", headers=headers)

    if response.status_code != 200:
        print(f"   FAILED: Getting specific task failed with status {response.status_code}")
        return False

    task = response.json()
    print(f"   SUCCESS: Retrieved task '{task['title']}'")

    # 6. Update a task
    print("6. Updating a task...")
    update_data = {
        "title": "Updated First Task",
        "description": "This is the updated first task",
        "completed": True
    }

    response = requests.put(f"{BASE_URL}/api/{user_id}/tasks/{first_task_id}",
                          json=update_data,
                          headers=headers)

    if response.status_code != 200:
        print(f"   FAILED: Updating task failed with status {response.status_code}")
        return False

    updated_task = response.json()
    print(f"   SUCCESS: Task updated to '{updated_task['title']}'")

    # 7. Update task completion status
    print("7. Updating task completion status...")
    completion_data = {"completed": False}

    response = requests.patch(f"{BASE_URL}/api/{user_id}/tasks/{first_task_id}/complete",
                            json=completion_data,
                            headers=headers)

    if response.status_code != 200:
        print(f"   FAILED: Updating completion status failed with status {response.status_code}")
        return False

    completed_task = response.json()
    print(f"   SUCCESS: Task completion updated to {completed_task['completed']}")

    # 8. Delete a task
    print("8. Deleting a task...")
    response = requests.delete(f"{BASE_URL}/api/{user_id}/tasks/{first_task_id}", headers=headers)

    if response.status_code != 204:
        print(f"   FAILED: Deleting task failed with status {response.status_code}")
        return False

    print(f"   SUCCESS: Task deleted")

    # 9. Logout
    print("9. Logging out user...")
    response = requests.post(f"{BASE_URL}/api/auth/logout", headers=headers)

    if response.status_code != 200:
        print(f"   FAILED: Logout failed with status {response.status_code}")
        return False

    print(f"   SUCCESS: User logged out")

    # 10. Test unauthorized access
    print("10. Testing unauthorized access...")
    response = requests.get(f"{BASE_URL}/api/{user_id}/tasks")

    if response.status_code != 401:
        print(f"   FAILED: Unauthorized access should return 401, got {response.status_code}")
        return False

    print(f"   SUCCESS: Unauthorized access properly blocked ({response.status_code})")

    print("\n" + "=" * 50)
    print("✅ ALL WORKFLOW TESTS PASSED!")
    print("✅ API is fully functional!")
    print("=" * 50)

    return True

if __name__ == "__main__":
    success = test_complete_workflow()
    if success:
        print("\n🎉 The Todo List API is working perfectly! 🎉")
    else:
        print("\n❌ Some tests failed")