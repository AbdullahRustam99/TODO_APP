#!/usr/bin/env python3
"""
Test script to verify MCP server can communicate with backend in Docker.
Run this inside the ai-service container.
"""
import asyncio
import httpx
import os
import sys

SERVICE_SECRET = os.getenv("BETTER_AUTH_SECRET", "abfe95adc6a3d85f1d8533a0fbf151b18240d817b471dda39a925555d886549c32c667dbeb184b9e9c73da3227c0dae5f83a")
BUSINESS_SERVICE_URL = os.getenv("BUSINESS_SERVICE_URL", "http://localhost:8000")

print(f"🔍 Testing MCP → Backend Connection")
print(f"   BUSINESS_SERVICE_URL: {BUSINESS_SERVICE_URL}")
print(f"   SERVICE_SECRET: {'✓ SET' if SERVICE_SECRET else '✗ NOT SET'}")
print()

async def test_backend_health():
    """Test if backend is reachable."""
    print("1️⃣  Testing backend health endpoint...")
    try:
        async with httpx.AsyncClient(trust_env=False, timeout=5.0) as client:
            response = await client.get(f"{BUSINESS_SERVICE_URL}/health")
            if response.status_code == 200:
                print(f"   ✅ Backend is reachable: {response.json()}")
                return True
            else:
                print(f"   ❌ Backend returned status {response.status_code}")
                return False
    except Exception as e:
        print(f"   ❌ Cannot reach backend: {e}")
        return False

async def test_authenticated_request():
    """Test authenticated request to backend."""
    print("\n2️⃣  Testing authenticated request...")
    try:
        headers = {"Authorization": f"Bearer {SERVICE_SECRET}"}
        async with httpx.AsyncClient(trust_env=False, timeout=5.0) as client:
            # Try to get tasks for user 1
            response = await client.get(
                f"{BUSINESS_SERVICE_URL}/api/1/tasks",
                headers=headers
            )
            if response.status_code == 200:
                tasks = response.json()
                print(f"   ✅ Authenticated request successful")
                print(f"   📝 User has {len(tasks)} tasks")
                return True
            elif response.status_code == 401:
                print(f"   ❌ Authentication failed: Invalid SERVICE_SECRET")
                return False
            else:
                print(f"   ⚠️  Unexpected status {response.status_code}: {response.text}")
                return False
    except Exception as e:
        print(f"   ❌ Request failed: {e}")
        return False

async def test_create_task():
    """Test creating a task."""
    print("\n3️⃣  Testing task creation...")
    try:
        headers = {
            "Authorization": f"Bearer {SERVICE_SECRET}",
            "Content-Type": "application/json"
        }
        payload = {
            "title": "Test Task from MCP Verification",
            "description": "This is a test task",
            "priority": "medium",
            "completed": False
        }
        async with httpx.AsyncClient(trust_env=False, timeout=5.0) as client:
            response = await client.post(
                f"{BUSINESS_SERVICE_URL}/api/1/tasks",
                json=payload,
                headers=headers
            )
            if response.status_code in [200, 201]:
                task = response.json()
                print(f"   ✅ Task created successfully")
                print(f"   📝 Task ID: {task.get('id')}, Title: {task.get('title')}")
                return task.get('id')
            else:
                print(f"   ❌ Failed to create task: {response.status_code}")
                print(f"   Response: {response.text}")
                return None
    except Exception as e:
        print(f"   ❌ Request failed: {e}")
        return None

async def test_delete_task(task_id):
    """Test deleting a task."""
    if not task_id:
        print("\n4️⃣  Skipping cleanup (no task created)")
        return
        
    print(f"\n4️⃣  Cleaning up test task {task_id}...")
    try:
        headers = {"Authorization": f"Bearer {SERVICE_SECRET}"}
        async with httpx.AsyncClient(trust_env=False, timeout=5.0) as client:
            response = await client.delete(
                f"{BUSINESS_SERVICE_URL}/api/1/tasks/{task_id}",
                headers=headers
            )
            if response.status_code in [200, 204]:
                print(f"   ✅ Test task deleted")
            else:
                print(f"   ⚠️  Failed to delete task: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Cleanup failed: {e}")

async def main():
    print("=" * 60)
    
    # Test 1: Backend health
    if not await test_backend_health():
        print("\n❌ Backend is not reachable. Check:")
        print("   - Is backend container running? (docker ps)")
        print("   - Is BUSINESS_SERVICE_URL correct?")
        print(f"   - Current value: {BUSINESS_SERVICE_URL}")
        sys.exit(1)
    
    # Test 2: Authentication
    if not await test_authenticated_request():
        print("\n❌ Authentication failed. Check:")
        print("   - Is BETTER_AUTH_SECRET the same in both services?")
        print("   - Check backend logs: docker logs todo-backend")
        sys.exit(1)
    
    # Test 3: Create task
    task_id = await test_create_task()
    
    # Test 4: Cleanup
    await test_delete_task(task_id)
    
    print("\n" + "=" * 60)
    print("🎉 All tests passed! MCP can communicate with backend.")
    print("\nThe issue should now be fixed. Try:")
    print("   1. Open http://localhost:3000 in your browser")
    print("   2. Log in")
    print("   3. Use chat to add a task")
    print("   4. Watch logs: docker logs todo-ai-service -f")

if __name__ == "__main__":
    asyncio.run(main())
