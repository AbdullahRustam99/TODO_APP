"""
Integration test for menu flow
"""

import unittest
from src.services.task_manager import TaskManager
from src.lib.console_interface import ConsoleInterface
from src.cli.menu_navigator import MenuNavigator


class TestMenuFlow(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.task_manager = TaskManager()
        self.console_interface = ConsoleInterface()
        self.menu_navigator = MenuNavigator(self.task_manager, self.console_interface)

    def test_complete_workflow(self):
        """Test a complete workflow through the application"""
        # Add a task
        task = self.task_manager.add_task("Test Task", "Test Description")
        self.assertIsNotNone(task)
        self.assertEqual(task.title, "Test Task")

        # Verify task exists
        retrieved_task = self.task_manager.get_task(task.id)
        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task.title, "Test Task")

        # List all tasks
        all_tasks = self.task_manager.list_tasks()
        self.assertEqual(len(all_tasks), 1)

        # Update the task
        updated_task = self.task_manager.update_task(task.id, "Updated Task", "Updated Description")
        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task.title, "Updated Task")

        # Toggle completion status
        completed_task = self.task_manager.toggle_task_completion(task.id)
        self.assertIsNotNone(completed_task)
        self.assertTrue(completed_task.completed)

        # List completed tasks
        completed_tasks = self.task_manager.list_completed_tasks()
        self.assertEqual(len(completed_tasks), 1)

        # List pending tasks
        pending_tasks = self.task_manager.list_pending_tasks()
        self.assertEqual(len(pending_tasks), 0)

        # Delete the task
        result = self.task_manager.delete_task(task.id)
        self.assertTrue(result)

        # Verify task is gone
        deleted_task = self.task_manager.get_task(task.id)
        self.assertIsNone(deleted_task)

    def test_menu_options_accessibility(self):
        """Test that all menu options are accessible"""
        menu_options = self.menu_navigator.menu_options
        expected_options = [
            "Add Task",
            "View Tasks",
            "Update Task",
            "Delete Task",
            "Mark Task Complete / Incomplete",
            "Exit"
        ]

        self.assertEqual(len(menu_options), len(expected_options))
        for expected_option in expected_options:
            self.assertIn(expected_option, menu_options)

    def test_task_manager_consistency(self):
        """Test that task manager maintains consistent state"""
        # Add multiple tasks
        task1 = self.task_manager.add_task("Task 1", "Description 1")
        task2 = self.task_manager.add_task("Task 2", "Description 2")
        task3 = self.task_manager.add_task("Task 3", "Description 3")

        # Verify all tasks exist
        all_tasks = self.task_manager.list_tasks()
        self.assertEqual(len(all_tasks), 3)

        # Verify individual retrieval works
        retrieved_task1 = self.task_manager.get_task(task1.id)
        retrieved_task2 = self.task_manager.get_task(task2.id)
        retrieved_task3 = self.task_manager.get_task(task3.id)

        self.assertIsNotNone(retrieved_task1)
        self.assertIsNotNone(retrieved_task2)
        self.assertIsNotNone(retrieved_task3)

        self.assertEqual(retrieved_task1.title, "Task 1")
        self.assertEqual(retrieved_task2.title, "Task 2")
        self.assertEqual(retrieved_task3.title, "Task 3")

        # Toggle completion of one task
        completed_task = self.task_manager.toggle_task_completion(task2.id)
        self.assertTrue(completed_task.completed)

        # Verify the state of all tasks
        completed_tasks = self.task_manager.list_completed_tasks()
        pending_tasks = self.task_manager.list_pending_tasks()

        self.assertEqual(len(completed_tasks), 1)
        self.assertEqual(len(pending_tasks), 2)

        # Delete one task
        delete_result = self.task_manager.delete_task(task1.id)
        self.assertTrue(delete_result)

        # Verify state after deletion
        all_tasks_after_delete = self.task_manager.list_tasks()
        self.assertEqual(len(all_tasks_after_delete), 2)


if __name__ == '__main__':
    unittest.main()