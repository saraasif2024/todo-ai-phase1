#!/usr/bin/env python3
"""
Simple Todo Application
Supports: Add, View, Delete, Update, and Complete tasks
Data is stored in todos.json
"""

import json
import os
import sys
from datetime import datetime


class TodoApp:
    def __init__(self, filename="todos.json"):
        self.filename = filename
        self.todos = self.load_todos()

    def load_todos(self):
        """Load todos from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: {self.filename} is corrupted. Starting fresh.")
                return []
        return []

    def save_todos(self):
        """Save todos to JSON file"""
        with open(self.filename, 'w') as f:
            json.dump(self.todos, f, indent=2)

    def add_todo(self, task):
        """Add a new todo task"""
        if not task.strip():
            print("Error: Task cannot be empty")
            return

        todo = {
            "id": len(self.todos) + 1,
            "task": task.strip(),
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.todos.append(todo)
        self.save_todos()
        print(f"✓ Added task #{todo['id']}: {task}")

    def view_todos(self):
        """Display all todos"""
        if not self.todos:
            print("No todos found. Add one to get started!")
            return

        print("\n" + "="*60)
        print("YOUR TODO LIST")
        print("="*60)
        for todo in self.todos:
            status = "✓" if todo["completed"] else "○"
            task_display = todo["task"]
            if todo["completed"]:
                task_display = f"\033[9m{task_display}\033[0m"  # strikethrough
            print(f"{status} [{todo['id']}] {task_display}")
        print("="*60 + "\n")

    def delete_todo(self, todo_id):
        """Delete a todo by ID"""
        for i, todo in enumerate(self.todos):
            if todo["id"] == todo_id:
                deleted_task = self.todos.pop(i)
                self.save_todos()
                print(f"✓ Deleted task #{todo_id}: {deleted_task['task']}")
                return
        print(f"Error: Task #{todo_id} not found")

    def update_todo(self, todo_id, new_task):
        """Update a todo's task description"""
        if not new_task.strip():
            print("Error: Task cannot be empty")
            return

        for todo in self.todos:
            if todo["id"] == todo_id:
                old_task = todo["task"]
                todo["task"] = new_task.strip()
                self.save_todos()
                print(f"✓ Updated task #{todo_id}")
                print(f"  Old: {old_task}")
                print(f"  New: {new_task}")
                return
        print(f"Error: Task #{todo_id} not found")

    def complete_todo(self, todo_id):
        """Mark a todo as completed"""
        for todo in self.todos:
            if todo["id"] == todo_id:
                if todo["completed"]:
                    print(f"Task #{todo_id} is already completed")
                else:
                    todo["completed"] = True
                    self.save_todos()
                    print(f"✓ Completed task #{todo_id}: {todo['task']}")
                return
        print(f"Error: Task #{todo_id} not found")

    def show_help(self):
        """Display help message"""
        help_text = """
Todo App - Usage:
  python todo.py add <task>           Add a new todo
  python todo.py view                 View all todos
  python todo.py delete <id>          Delete a todo by ID
  python todo.py update <id> <task>   Update a todo's description
  python todo.py complete <id>        Mark a todo as completed
  python todo.py help                 Show this help message

Examples:
  python todo.py add "Buy groceries"
  python todo.py view
  python todo.py complete 1
  python todo.py update 1 "Buy groceries and cook dinner"
  python todo.py delete 1
"""
        print(help_text)


def main():
    app = TodoApp()

    if len(sys.argv) < 2:
        app.show_help()
        return

    command = sys.argv[1].lower()

    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Please provide a task description")
            print("Usage: python todo.py add <task>")
        else:
            task = " ".join(sys.argv[2:])
            app.add_todo(task)

    elif command == "view":
        app.view_todos()

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: Please provide a task ID")
            print("Usage: python todo.py delete <id>")
        else:
            try:
                todo_id = int(sys.argv[2])
                app.delete_todo(todo_id)
            except ValueError:
                print("Error: Task ID must be a number")

    elif command == "update":
        if len(sys.argv) < 4:
            print("Error: Please provide a task ID and new description")
            print("Usage: python todo.py update <id> <task>")
        else:
            try:
                todo_id = int(sys.argv[2])
                new_task = " ".join(sys.argv[3:])
                app.update_todo(todo_id, new_task)
            except ValueError:
                print("Error: Task ID must be a number")

    elif command == "complete":
        if len(sys.argv) < 3:
            print("Error: Please provide a task ID")
            print("Usage: python todo.py complete <id>")
        else:
            try:
                todo_id = int(sys.argv[2])
                app.complete_todo(todo_id)
            except ValueError:
                print("Error: Task ID must be a number")

    elif command == "help":
        app.show_help()

    else:
        print(f"Error: Unknown command '{command}'")
        app.show_help()


if __name__ == "__main__":
    main()
