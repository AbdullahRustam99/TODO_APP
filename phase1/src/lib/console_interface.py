"""
Console interface utilities for the TODO Console Application
Handles user input/output and error messaging
"""

from typing import Optional


class ConsoleInterface:
    def __init__(self):
        """Initialize the console interface"""
        pass

    def display_message(self, message: str):
        """
        Display a message to the console

        Args:
            message (str): The message to display
        """
        print(message)

    def display_error(self, error_message: str):
        """
        Display an error message to the console

        Args:
            error_message (str): The error message to display
        """
        print(f"Error: {error_message}")

    def display_confirmation(self, message: str) -> bool:
        """
        Display a confirmation message and get user input

        Args:
            message (str): The confirmation message to display

        Returns:
            bool: True if user confirms, False otherwise
        """
        response = input(f"{message} (y/N): ").strip().lower()
        return response in ['y', 'yes']

    def get_input(self, prompt: str) -> str:
        """
        Get input from the user with a prompt

        Args:
            prompt (str): The prompt to display to the user

        Returns:
            str: The user's input
        """
        return input(prompt).strip()

    def get_task_input(self) -> tuple[str, str]:
        """
        Get task title and description from user input

        Returns:
            tuple[str, str]: A tuple containing (title, description)
        """
        title = input("Enter task title: ").strip()
        description = input("Enter task description (optional): ").strip()
        return title, description

    def get_task_id(self) -> Optional[int]:
        """
        Get task ID from user input

        Returns:
            int or None: The task ID if valid, None otherwise
        """
        try:
            task_id_input = input("Enter task ID: ").strip()
            if not task_id_input:
                return None
            return int(task_id_input)
        except ValueError:
            return None

    def clear_screen(self):
        """
        Clear the console screen
        """
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

    def pause(self, message: str = "Press Enter to continue..."):
        """
        Pause execution and wait for user input

        Args:
            message (str): The message to display (default: "Press Enter to continue...")
        """
        input(message)