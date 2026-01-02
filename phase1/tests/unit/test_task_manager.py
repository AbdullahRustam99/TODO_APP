"""
Unit tests for TaskManager service
"""

import unittest
from src.services.task_manager import TaskManager


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.task_manager = TaskManager()

    def test_add_task_success(self):
        """Test adding a task successfully"""
        task = self.task_manager.add_task("Test Title", "Test Description")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Title")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.completed, False)

    def test_add_task_without_description(self):
        """Test adding a task with no description"""
        task = self.task_manager.add_task("Test Title")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Title")
        self.assertEqual(task.description, "")

    def test_add_task_empty_title_fails(self):
        """Test adding a task with empty title raises ValueError"""
        with self.assertRaises(ValueError):
            self.task_manager.add_task("")

        with self.assertRaises(ValueError):
            self.task_manager.add_task("   ")  # whitespace only

    def test_get_task(self):
        """Test retrieving a task by ID"""
        task = self.task_manager.add_task("Test Title")
        retrieved_task = self.task_manager.get_task(task.id)
        self.assertEqual(retrieved_task.id, task.id)
        self.assertEqual(retrieved_task.title, task.title)

    def test_get_nonexistent_task(self):
        """Test retrieving a non-existent task returns None"""
        result = self.task_manager.get_task(999)
        self.assertIsNone(result)

    def test_update_task(self):
        """Test updating a task's title and description"""
        task = self.task_manager.add_task("Original Title", "Original Description")

        updated_task = self.task_manager.update_task(task.id, "New Title", "New Description")

        self.assertEqual(updated_task.title, "New Title")
        self.assertEqual(updated_task.description, "New Description")

    def test_update_task_partial(self):
        """Test updating only title or only description"""
        task = self.task_manager.add_task("Original Title", "Original Description")

        # Update only title
        updated_task = self.task_manager.update_task(task.id, "New Title", None)
        self.assertEqual(updated_task.title, "New Title")
        self.assertEqual(updated_task.description, "Original Description")

        # Update only description
        task2 = self.task_manager.add_task("Title 2", "Desc 2")
        updated_task2 = self.task_manager.update_task(task2.id, None, "New Desc")
        self.assertEqual(updated_task2.title, "Title 2")
        self.assertEqual(updated_task2.description, "New Desc")

    def test_update_nonexistent_task(self):
        """Test updating a non-existent task returns None"""
        result = self.task_manager.update_task(999, "New Title")
        self.assertIsNone(result)

    def test_update_task_empty_title_fails(self):
        """Test updating a task with empty title raises ValueError"""
        task = self.task_manager.add_task("Original Title")

        with self.assertRaises(ValueError):
            self.task_manager.update_task(task.id, "")

    def test_delete_task(self):
        """Test deleting an existing task"""
        task = self.task_manager.add_task("Test Title")
        result = self.task_manager.delete_task(task.id)

        self.assertTrue(result)
        self.assertIsNone(self.task_manager.get_task(task.id))

    def test_delete_nonexistent_task(self):
        """Test deleting a non-existent task returns False"""
        result = self.task_manager.delete_task(999)
        self.assertFalse(result)

    def test_toggle_task_completion(self):
        """Test toggling task completion status"""
        task = self.task_manager.add_task("Test Title")
        self.assertFalse(task.completed)

        toggled_task = self.task_manager.toggle_task_completion(task.id)
        self.assertTrue(toggled_task.completed)

        toggled_task2 = self.task_manager.toggle_task_completion(task.id)
        self.assertFalse(toggled_task2.completed)

    def test_toggle_nonexistent_task(self):
        """Test toggling completion of non-existent task returns None"""
        result = self.task_manager.toggle_task_completion(999)
        self.assertIsNone(result)

    def test_list_tasks(self):
        """Test listing all tasks"""
        task1 = self.task_manager.add_task("Title 1")
        task2 = self.task_manager.add_task("Title 2")

        tasks = self.task_manager.list_tasks()
        self.assertEqual(len(tasks), 2)

        task_ids = [task.id for task in tasks]
        self.assertIn(task1.id, task_ids)
        self.assertIn(task2.id, task_ids)

    def test_list_completed_tasks(self):
        """Test listing completed tasks"""
        task1 = self.task_manager.add_task("Title 1")
        task2 = self.task_manager.add_task("Title 2")

        # Complete task1 only
        self.task_manager.toggle_task_completion(task1.id)

        completed_tasks = self.task_manager.list_completed_tasks()
        self.assertEqual(len(completed_tasks), 1)
        self.assertEqual(completed_tasks[0].id, task1.id)

    def test_list_pending_tasks(self):
        """Test listing pending tasks"""
        task1 = self.task_manager.add_task("Title 1")
        task2 = self.task_manager.add_task("Title 2")

        # Complete task1 only
        self.task_manager.toggle_task_completion(task1.id)

        pending_tasks = self.task_manager.list_pending_tasks()
        self.assertEqual(len(pending_tasks), 1)
        self.assertEqual(pending_tasks[0].id, task2.id)


if __name__ == '__main__':
    unittest.main()