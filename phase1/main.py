"""
Main entry point for the TODO Console Application
Implements arrow-key navigation and menu selection functionality
"""

from src.services.task_manager import TaskManager
from src.lib.console_interface import ConsoleInterface
from src.cli.menu_navigator import MenuNavigator


def main():
    """
    Main function to run the TODO Console Application
    """
    # Initialize core components
    task_manager = TaskManager()
    console_interface = ConsoleInterface()
    menu_navigator = MenuNavigator(task_manager, console_interface)

    try:
        # Run the main menu
        menu_navigator.run_menu()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please restart the application.")


if __name__ == "__main__":
    main()