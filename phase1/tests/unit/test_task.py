"""
Unit tests for Task model
"""

import unittest
from src.models.task import Task


class TestTask(unittest.TestCase):
    def test_task_creation(self):
        """Test creating a task with required fields"""
        task = Task(1, "Test Title", "Test Description", False)
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Title")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.completed, False)

    def test_task_defaults(self):
        """Test creating a task with minimal parameters"""
        task = Task(1, "Test Title")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Title")
        self.assertEqual(task.description, "")
        self.assertEqual(task.completed, False)

    def test_task_str_representation(self):
        """Test string representation of task"""
        task = Task(1, "Test Title", "Test Description", False)
        str_repr = str(task)
        self.assertIn("1.", str_repr)
        self.assertIn("Test Title", str_repr)
        self.assertIn("Pending", str_repr)

        task.completed = True
        str_repr = str(task)
        self.assertIn("Completed", str_repr)

    def test_task_to_dict(self):
        """Test converting task to dictionary"""
        task = Task(1, "Test Title", "Test Description", True)
        task_dict = task.to_dict()

        self.assertEqual(task_dict["id"], 1)
        self.assertEqual(task_dict["title"], "Test Title")
        self.assertEqual(task_dict["description"], "Test Description")
        self.assertEqual(task_dict["completed"], True)

    def test_task_from_dict(self):
        """Test creating task from dictionary"""
        data = {
            "id": 1,
            "title": "Test Title",
            "description": "Test Description",
            "completed": True
        }
        task = Task.from_dict(data)

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Title")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.completed, True)


if __name__ == '__main__':
    unittest.main()