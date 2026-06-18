import os
from typing import List, Dict
from datetime import datetime
from task_manager import TaskManager, Task
from user_manager import UserManager

class ReportGenerator:
    """
    Analyzes project data and formats it into comprehensive reports.
    Designed to provide high-level visibility to team leads and administrators.
    """
    def __init__(self, task_manager: TaskManager, user_manager: UserManager):
        self.task_manager = task_manager
        self.user_manager = user_manager

    def generate_summary_stats(self) -> Dict[str, int]:
        """
        Calculates basic statistical summaries.
        """
        tasks = self.task_manager.get_all_tasks()
        stats = {
            "total_tasks": len(tasks),
            "completed_tasks": 0,
            "pending_tasks": 0,
            "unassigned_tasks": 0
        }
        
        for task in tasks:
            if task.status.lower() == "completed":
                stats["completed_tasks"] += 1
            else:
                stats["pending_tasks"] += 1
                
            if task.assignee.lower() == "unassigned":
                stats["unassigned_tasks"] += 1
                
        return stats

    def create_text_report(self) -> str:
        """
        Generates a human-readable performance text report suitable for CLI viewing.
        """
        stats = self.generate_summary_stats()
        users = self.user_manager.get_all_users()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report_lines = []
        report_lines.append("="*50)
        report_lines.append(f" SMART TASK MANAGER - SYSTEM REPORT ")
        report_lines.append(f" Generated At: {current_time}")
        report_lines.append("="*50)
        report_lines.append("")
        report_lines.append("--- Overall Task Statistics ---")
        report_lines.append(f" Total Tasks:      {stats['total_tasks']}")
        report_lines.append(f" Completed:        {stats['completed_tasks']}")
        report_lines.append(f" Pending:          {stats['pending_tasks']}")
        report_lines.append(f" Unassigned Tasks: {stats['unassigned_tasks']}")
        report_lines.append("")
        
        report_lines.append("--- User Workload ---")
        for user in users:
            user_tasks = self.task_manager.get_tasks_by_assignee(user.username)
            completed_user = sum(1 for t in user_tasks if t.status.lower() == "completed")
            pending_user = sum(1 for t in user_tasks if t.status.lower() != "completed")
            
            report_lines.append(f" User: {user.username} (Role: {user.role})")
            report_lines.append(f"  - Tasks Assigned: {len(user_tasks)}")
            report_lines.append(f"  - Completed:      {completed_user}")
            report_lines.append(f"  - Incomplete:     {pending_user}")
        
        report_lines.append("="*50)
        
        return "\n".join(report_lines)

    def print_report(self) -> None:
        """
        Helper method to immediately print the text report to the terminal.
        """
        print(self.create_text_report())

    def export_to_markdown_file(self, filename: str = "report.md") -> bool:
        """
        Takes the generated stats and outputs them as a markdown file for documentation.
        """
        try:
            content = self.create_text_report()
            # simple text to markdown wrapper
            md_content = f"# System Report\n\n```text\n{content}\n```\n"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(md_content)
            return True
        except Exception as e:
            print(f"Error exporting report: {e}")
            return False
