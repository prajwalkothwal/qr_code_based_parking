import sys
from utils import clear_screen
from user_manager import UserManager
from task_manager import TaskManager
from report_generator import ReportGenerator

def print_menu(user_manager: UserManager):
    """Prints the interactive CLI menu based on user role."""
    print("\n" + "="*40)
    print("      SMART TASK MANAGER")
    print("="*40)
    
    current_user = user_manager.get_current_user()
    if not current_user:
        print(" 1. Login (Simulated)")
        print(" 2. Exit")
        print("="*40)
        return

    print(f" Logged in as: {current_user.username} (Role: {current_user.role})")
    print("-" * 40)
    print(" 1. View all tasks")
    print(" 2. View my tasks")
    print(" 3. Add a task")
    print(" 4. Complete a task")
    print(" 5. Delete a task")
    print(" 6. Generate System Report")
    print(" 7. Logout")
    print(" 8. Exit")
    print("="*40)

def handle_unauthenticated_flow(user_manager: UserManager, choice: str) -> bool:
    """Handles inputs when no user is logged in. Returns False to exit the app."""
    if choice == "1":
        username = input("Enter username (AdminUser, Alice, Bob): ")
        if user_manager.login(username):
            print(f"Successfully logged in as {username}.")
        else:
            print("Invalid user. Try again.")
    elif choice == "2":
        return False
    else:
        print("Invalid choice.")
    return True

def handle_authenticated_flow(
    choice: str, 
    user_manager: UserManager, 
    task_manager: TaskManager, 
    report_generator: ReportGenerator
) -> bool:
    """Handles inputs when a user is logged in. Returns False to exit the app."""
    user = user_manager.get_current_user()
    
    if choice == "1":
        tasks = task_manager.get_all_tasks()
        print("\n--- ALL TASKS ---")
        for t in tasks:
            print(f"[{t.status}] {t.title} (ID: {t.task_id}) - Assigned to: {t.assignee}")
    
    elif choice == "2":
        tasks = task_manager.get_tasks_by_assignee(user.username)
        print(f"\n--- TASKS FOR {user.username.upper()} ---")
        if not tasks:
            print("No tasks assigned to you.")
        for t in tasks:
            print(f"[{t.status}] {t.title} (ID: {t.task_id})")

    elif choice == "3":
        title = input("Enter task title: ")
        desc = input("Enter description: ")
        assignee = input("Assign to (Username or 'Unassigned'): ")
        try:
            new_task = task_manager.add_task(title, desc, assignee)
            print(f"Task created successfully: ID {new_task.task_id}")
        except Exception as e:
            print(f"Failed to create task: {e}")

    elif choice == "4":
        task_id = input("Enter Task ID to complete: ")
        if task_manager.complete_task(task_id):
            print("Task marked as completed.")
        else:
            print("Task ID not found.")

    elif choice == "5":
        task_id = input("Enter Task ID to delete: ")
        if not user_manager.is_admin():
            print("Action Denied: Only admins can delete tasks.")
        else:
            if task_manager.delete_task(task_id):
                print("Task deleted successfully.")
            else:
                print("Task ID not found.")

    elif choice == "6":
        print("\nGenerating System Report...\n")
        report_generator.print_report()
        export = input("\Export to Markdown file? (y/n): ")
        if export.lower() == 'y':
            if report_generator.export_to_markdown_file():
                print("Exported to report.md")

    elif choice == "7":
        user_manager.logout()
        print("Logged out.")

    elif choice == "8":
        return False
        
    else:
        print("Invalid choice. Please try again.")

    return True

def main():
    """
    Main application loop.
    """
    print("Welcome to Smart Task Manager Initialization...")
    user_manager = UserManager()
    task_manager = TaskManager()
    report_generator = ReportGenerator(task_manager, user_manager)

    running = True
    while running:
        print_menu(user_manager)
        choice = input("Select an option: ")
        
        # clear_screen() # Commented out for smoother debugging in virtual terminals.

        if not user_manager.get_current_user():
            running = handle_unauthenticated_flow(user_manager, choice)
        else:
            running = handle_authenticated_flow(choice, user_manager, task_manager, report_generator)

    print("Goodbye!")
    sys.exit(0)

if __name__ == "__main__":
    main()
// this file ends here