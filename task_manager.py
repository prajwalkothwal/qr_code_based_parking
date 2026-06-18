import os
from typing import List, Dict, Optional
from utils import load_json_data, save_json_data, generate_id, format_timestamp, validate_non_empty_string

# Define the path to our local storage
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "tasks.json")

class Task:
    """
    Represents an actionable item within the Task Manager.
    """
    def __init__(self, title: str, description: str = "", assignee: str = "Unassigned", 
                 status: str = "Pending", task_id: str = None, 
                 created_at: str = None, completed_at: str = None):
        self.task_id = task_id if task_id else generate_id("task")
        self.title = validate_non_empty_string(title, "Title")
        self.description = description
        self.assignee = assignee
        self.status = status
        self.created_at = created_at if created_at else format_timestamp()
        self.completed_at = completed_at

    def mark_completed(self) -> None:
        """Marks the task as completed and sets the completion timestamp."""
        self.status = "Completed"
        self.completed_at = format_timestamp()

    def update_assignee(self, user_id: str) -> None:
        """Updates the person responsible for this task."""
        self.assignee = validate_non_empty_string(user_id, "Assignee")

    def to_dict(self) -> Dict:
        """Serializes the Task object into a dictionary for JSON storage."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "assignee": self.assignee,
            "status": self.status,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Task":
        """Instantiates a Task object from a serialized dictionary."""
        return cls(
            title=data.get("title", "Untitled Task"),
            description=data.get("description", ""),
            assignee=data.get("assignee", "Unassigned"),
            status=data.get("status", "Pending"),
            task_id=data.get("task_id"),
            created_at=data.get("created_at"),
            completed_at=data.get("completed_at")
        )

class TaskManager:
    """
    The orchestrator for managing the lifecycle, storage, and retrieval of Task instances.
    """
    def __init__(self, storage_path: str = DATA_FILE):
        self.storage_path = storage_path
        self.tasks: List[Task] = []
        self.load_tasks()

    def load_tasks(self) -> None:
        """Loads tasks from local JSON storage using utility methods."""
        default_structure = {"tasks": []}
        data = load_json_data(self.storage_path, default_data=default_structure)
        self.tasks = [Task.from_dict(t) for t in data.get("tasks", [])]

    def save_tasks(self) -> None:
        """Persists the current state of tasks via the JSON utility function."""
        data_to_save = {"tasks": [task.to_dict() for task in self.tasks]}
        save_json_data(self.storage_path, data_to_save)

    def add_task(self, title: str, description: str, assignee: str) -> Task:
        """
        Creates a new task, adds it to the internal list, and saves to file.
        """
        new_task = Task(title=title, description=description, assignee=assignee)
        self.tasks.append(new_task)
        self.save_tasks()
        return new_task

    def delete_task(self, task_id: str) -> bool:
        """
        Removes a task by its ID.
        Returns True if successful, False if the task was not found.
        """
        initial_count = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.task_id != task_id]
        if len(self.tasks) < initial_count:
            self.save_tasks()
            return True
        return False

    def complete_task(self, task_id: str) -> bool:
        """
        Marks a specific task as completed.
        Returns True if found and updated, False otherwise.
        """
        for task in self.tasks:
            if task.task_id == task_id:
                task.mark_completed()
                self.save_tasks()
                return True
        return False

    def get_all_tasks(self) -> List[Task]:
        """Returns all managed tasks."""
        return self.tasks

    def get_tasks_by_assignee(self, assignee: str) -> List[Task]:
        """Filters tasks designated to a specific individual."""
        return [t for t in self.tasks if t.assignee.lower() == assignee.lower()]

    def get_tasks_by_status(self, status: str) -> List[Task]:
        """Filters tasks by their completion state."""
        return [t for t in self.tasks if t.status.lower() == status.lower()]
