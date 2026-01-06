"""
Test script to verify the new Task model fields work correctly
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8001"

def test_new_task_fields():
    print("Testing new Task model fields (priority, due_date)...")

    # Register a test user
    timestamp = str(int(datetime.now().timestamp()))
    user_data = {
        "email": f"testuser_{timestamp}@example.com",
        "password": "securepassword123",
        "name": f"Test User {timestamp}"
    }

    response = requests.post(f"{BASE_URL}/api/auth/register",
                           json=user_data,
                           headers={"Content-Type": "application/json"})

    if response.status_code != 201:
        print(f"Failed to register user: {response.status_code}")
        return False

    result = response.json()
    token = result['token']
    user_id = result['user']['id']
    print(f"User registered: {user_id}")

    # Create a task with new fields
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    task_data = {
        "title": "Test Task with Priority",
        "description": "This is a test task with priority and due date",
        "completed": False,
        "priority": "high",
        "due_date": "2025-12-31T23:59:59"
    }

    response = requests.post(f"{BASE_URL}/api/{user_id}/tasks",
                           json=task_data,
                           headers=headers)

    if response.status_code != 201:
        print(f"Failed to create task with new fields: {response.status_code} - {response.text}")
        return False

    task_result = response.json()
    print(f"Task created with new fields: {task_result}")

    # Verify the response contains the new fields
    if 'priority' in task_result and 'due_date' in task_result:
        print("✅ New fields (priority, due_date) are present in response")
    else:
        print("❌ New fields are missing from response")
        return False

    # Get the task back to verify it was stored correctly
    response = requests.get(f"{BASE_URL}/api/{user_id}/tasks/{task_result['id']}", headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve task: {response.status_code}")
        return False

    retrieved_task = response.json()
    print(f"Retrieved task: {retrieved_task}")

    # Verify the new fields are preserved
    if (retrieved_task.get('priority') == 'high' and
        'due_date' in retrieved_task and
        retrieved_task.get('title') == 'Test Task with Priority'):
        print("✅ New fields are correctly stored and retrieved")
    else:
        print("❌ New fields are not correctly stored or retrieved")
        return False

    # Test updating the task with new fields
    update_data = {
        "priority": "low",
        "due_date": "2026-01-15T10:30:00"
    }

    response = requests.put(f"{BASE_URL}/api/{user_id}/tasks/{task_result['id']}",
                          json=update_data,
                          headers=headers)

    if response.status_code != 200:
        print(f"Failed to update task with new fields: {response.status_code}")
        return False

    updated_task = response.json()
    print(f"Updated task: {updated_task}")

    if updated_task.get('priority') == 'low':
        print("✅ Task update with new fields works correctly")
    else:
        print("❌ Task update with new fields failed")
        return False

    print("\n🎉 All tests passed! New Task fields are working correctly!")
    return True

if __name__ == "__main__":
    test_new_task_fields()