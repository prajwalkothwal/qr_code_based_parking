# Smart Task Manager

Smart Task Manager is a Python-based CLI application to help you keep track of tasks, user roles, and generate work reports. 
This project serves as a showcase of collaborative team development, displaying a modular structure where concerns are separated into discrete, manageable files.

## Project Structure

The project code is divided amongst following modules, making it easy for up to 4 team members to work on it simultaneously:

- `main.py`: Interactive CLI entry point mapping out the UX.
- `task_manager.py`: Core logic for task manipulations and abstractions.
- `user_manager.py`: User authorization and session tracking mechanics.
- `report_generator.py`: Generates project analytics.
- `utils.py`: Re-usable I/O functions and common utilities.

## Requirements

The project relies purely on Python's Standard Library to be maximally portable, however we have included a `requirements.txt` for simulation purposes.
- Python 3.8+

## How to Run

Navigate to the project root and execute the main entry file:

```bash
python main.py
```

## Features
- Add, Edit, Complete, and Remove tasks
- Multi-user simulated sessions
- Markdown report generation
- Persistent storage via JSON (Local)
