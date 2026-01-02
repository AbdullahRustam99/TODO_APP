"""
MenuNavigator for the TODO Console Application
Handles menu selection using number-based input as fallback when curses is not available
"""

import sys
from src.services.task_manager import TaskManager
from src.lib.console_interface import ConsoleInterface
from typing import List, Callable, Dict, Any


class MenuNavigator:
    def __init__(self, task_manager: TaskManager, console_interface: ConsoleInterface):
        """
        Initialize the MenuNavigator

        Args:
            task_manager (TaskManager): The task manager instance
            console_interface (ConsoleInterface): The console interface instance
        """
        self.task_manager = task_manager
        self.console_interface = console_interface
        self.menu_options = [
            "Add Task",
            "View Tasks",
            "Update Task",
            "Delete Task",
            "Mark Task Complete / Incomplete",
            "Exit"
        ]
        self.current_selection = 0

    def display_menu(self):
        """
        Display the main menu with numbered options
        """
        print("\n" + "="*50)
        print("           TODO APPLICATION")
        print("="*50)

        for i, option in enumerate(self.menu_options, 1):
            if i == self.current_selection + 1:
                # Highlight the selected option
                print(f"> {i}. {option} <")
            else:
                print(f"  {i}. {option}")

        print("="*50)
        print("Use number keys to select an option")

    def handle_selection(self) -> str:
        """
        Handle menu selection using number input

        Returns:
            str: The action to perform based on the selection
        """
        while True:
            try:
                self.display_menu()
                choice = input("\nEnter your choice (1-6): ").strip()

                if not choice:
                    print("Please enter a number between 1 and 6.")
                    continue

                choice_num = int(choice)

                if 1 <= choice_num <= len(self.menu_options):
                    self.current_selection = choice_num - 1
                    return self.execute_selection()
                else:
                    print(f"Please enter a number between 1 and {len(self.menu_options)}.")
            except ValueError:
                print("Please enter a valid number.")
            except KeyboardInterrupt:
                return "exit"

    def execute_selection(self) -> str:
        """
        Execute the action for the currently selected menu option

        Returns:
            str: The action to perform based on the selection
        """
        selected_option = self.menu_options[self.current_selection]

        if selected_option == "Add Task":
            return "add_task"
        elif selected_option == "View Tasks":
            return "view_tasks"
        elif selected_option == "Update Task":
            return "update_task"
        elif selected_option == "Delete Task":
            return "delete_task"
        elif selected_option == "Mark Task Complete / Incomplete":
            return "toggle_task"
        elif selected_option == "Exit":
            return "exit"
        else:
            return "unknown"

    def run_add_task(self):
        """Run the add task functionality"""
        print("\n--- Add Task ---")
        title, description = self.console_interface.get_task_input()

        if not title:
            self.console_interface.display_error("Task title cannot be empty")
            return

        try:
            task = self.task_manager.add_task(title, description)
            print(f"Task added with ID: {task.id}")
        except ValueError as e:
            self.console_interface.display_error(str(e))

    def run_view_tasks(self):
        """Run the view tasks functionality"""
        print("\n--- View Tasks ---")
        tasks = self.task_manager.list_tasks()

        if not tasks:
            print("No tasks available.")
            return

        for task in tasks:
            status_symbol = "✓" if task.completed else "✗"
            status_text = "Completed" if task.completed else "Pending"
            print(f"{task.id}. {task.title} [{status_text}]")
            if task.description:
                print(f"    Description: {task.description}")
        print(f"\nTotal tasks: {len(tasks)}")

    def run_update_task(self):
        """Run the update task functionality"""
        print("\n--- Update Task ---")
        task_id = self.console_interface.get_task_id()

        if task_id is None:
            self.console_interface.display_error("Invalid task ID")
            return

        task = self.task_manager.get_task(task_id)
        if not task:
            self.console_interface.display_error(f"No task found with ID: {task_id}")
            return

        print(f"Current task: {task.title}")
        if task.description:
            print(f"Current description: {task.description}")

        new_title = input(f"Enter new title (current: '{task.title}'): ").strip()
        if not new_title:
            new_title = None

        new_description = input(f"Enter new description (current: '{task.description}'): ").strip()
        if not new_description and task.description != "":
            new_description = None

        try:
            updated_task = self.task_manager.update_task(task_id, new_title, new_description)
            if updated_task:
                print(f"Task {task_id} updated successfully")
            else:
                self.console_interface.display_error(f"Failed to update task {task_id}")
        except ValueError as e:
            self.console_interface.display_error(str(e))

    def run_delete_task(self):
        """Run the delete task functionality"""
        print("\n--- Delete Task ---")
        task_id = self.console_interface.get_task_id()

        if task_id is None:
            self.console_interface.display_error("Invalid task ID")
            return

        task = self.task_manager.get_task(task_id)
        if not task:
            self.console_interface.display_error(f"No task found with ID: {task_id}")
            return

        print(f"Task to delete: {task.title}")
        if self.console_interface.display_confirmation("Are you sure you want to delete this task?"):
            if self.task_manager.delete_task(task_id):
                print(f"Task {task_id} deleted successfully")
            else:
                self.console_interface.display_error(f"Failed to delete task {task_id}")
        else:
            print("Task deletion cancelled")

    def run_toggle_task(self):
        """Run the toggle task completion functionality"""
        print("\n--- Mark Task Complete / Incomplete ---")
        task_id = self.console_interface.get_task_id()

        if task_id is None:
            self.console_interface.display_error("Invalid task ID")
            return

        task = self.task_manager.get_task(task_id)
        if not task:
            self.console_interface.display_error(f"No task found with ID: {task_id}")
            return

        # Toggle the task completion status
        updated_task = self.task_manager.toggle_task_completion(task_id)
        if updated_task:
            status = "completed" if updated_task.completed else "pending"
            print(f"Task {task_id} marked as {status}")
        else:
            self.console_interface.display_error(f"Failed to update task {task_id}")

    def run_menu(self):
        """
        Run the main menu loop using number-based selection
        Falls back to number input since curses may not be available on all platforms
        """
        print("Starting application...")
        print("Use number keys to navigate, Enter to select")

        try:
            while True:
                action = self.handle_selection()

                if action == "exit":
                    break
                elif action == "add_task":
                    self.run_add_task()
                    self.console_interface.pause()
                elif action == "view_tasks":
                    self.run_view_tasks()
                    self.console_interface.pause()
                elif action == "update_task":
                    self.run_update_task()
                    self.console_interface.pause()
                elif action == "delete_task":
                    self.run_delete_task()
                    self.console_interface.pause()
                elif action == "toggle_task":
                    self.run_toggle_task()
                    self.console_interface.pause()
                else:
                    print("Unknown action selected.")
                    self.console_interface.pause()

            print("\nThank you for using the TODO Console Application!")
        except KeyboardInterrupt:
            print("\n\nApplication interrupted by user.")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            print("Please restart the application.")