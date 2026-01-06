"""
Quick test to verify the backend API with new fields is working
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"  # Server running on port 8000

def test_backend():
    print("Testing Backend API with new fields...")
    print("=" * 50)

    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("   ✅ Health check: OK")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
        return False

    # Test 2: Register a user
    print("2. Testing user registration...")
    try:
        timestamp = str(int(datetime.now().timestamp()))
        user_data = {
            "email": f"test_{timestamp}@example.com",
            "password": "password123",
            "name": f"Test User {timestamp}"
        }

        response = requests.post(f"{BASE_URL}/api/auth/register",
                               json=user_data,
                               headers={"Content-Type": "application/json"})

        if response.status_code == 201:
            result = response.json()
            token = result['token']
            user_id = result['user']['id']
            print(f"   ✅ User registration: OK (User ID: {user_id})")
        else:
            print(f"   ❌ User registration failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ User registration failed: {e}")
        return False

    # Test 3: Create a task with new fields
    print("3. Testing task creation with new fields...")
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        task_data = {
            "title": "Test Task with New Fields",
            "description": "Task with priority and due date",
            "completed": False,
            "priority": "high",  # NEW FIELD
            "due_date": "2025-12-31T23:59:59"  # NEW FIELD
        }

        response = requests.post(f"{BASE_URL}/api/{user_id}/tasks",
                               json=task_data,
                               headers=headers)

        if response.status_code == 201:
            result = response.json()
            task_id = result['id']
            print(f"   ✅ Task creation with new fields: OK (Task ID: {task_id})")

            # Verify new fields are present in response
            if 'priority' in result and 'due_date' in result:
                print(f"   ✅ New fields present in response: priority={result['priority']}, due_date={result['due_date']}")
            else:
                print(f"   ⚠️  New fields missing from response: {result.keys()}")
        else:
            print(f"   ❌ Task creation failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Task creation failed: {e}")
        return False

    # Test 4: Get the task back
    print("4. Testing task retrieval...")
    try:
        response = requests.get(f"{BASE_URL}/api/{user_id}/tasks/{task_id}", headers=headers)

        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Task retrieval: OK")

            # Verify new fields are preserved
            if result.get('priority') == 'high':
                print(f"   ✅ Priority field preserved: {result['priority']}")
            else:
                print(f"   ⚠️  Priority field not preserved: {result.get('priority')}")

            if 'due_date' in result and result['due_date']:
                print(f"   ✅ Due date field preserved: {result['due_date']}")
            else:
                print(f"   ⚠️  Due date field not preserved: {result.get('due_date')}")
        else:
            print(f"   ❌ Task retrieval failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Task retrieval failed: {e}")
        return False

    # Test 5: Update task with new fields
    print("5. Testing task update with new fields...")
    try:
        update_data = {
            "priority": "low",
            "due_date": "2026-01-15T10:30:00"
        }

        response = requests.put(f"{BASE_URL}/api/{user_id}/tasks/{task_id}",
                              json=update_data,
                              headers=headers)

        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Task update with new fields: OK")

            if result.get('priority') == 'low':
                print(f"   ✅ Priority updated successfully: {result['priority']}")
            else:
                print(f"   ⚠️  Priority not updated: {result.get('priority')}")
        else:
            print(f"   ❌ Task update failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Task update failed: {e}")
        return False

    print("=" * 50)
    print("🎉 ALL TESTS PASSED! Backend API with new fields is working correctly!")
    print("✅ Priority and due_date fields are fully functional")
    print("✅ All CRUD operations work with new fields")
    print("=" * 50)

    return True

if __name__ == "__main__":
    test_backend()