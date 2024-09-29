import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QListWidget, QLineEdit, QMessageBox
)

class TaskManager(QWidget):
    def __init__(self, filename='tasks.json'):
        super().__init__()
        self.tasks = []
        self.filename = filename
        self.initUI()
        self.load_tasks()

    def initUI(self):
        """Initialize the GUI components."""
        self.setWindowTitle('Task Manager')

        # Layouts
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Task Input
        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("Enter a new task")
        layout.addWidget(self.task_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Task", self)
        self.add_button.clicked.connect(self.add_task)
        button_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Edit Task", self)
        self.edit_button.clicked.connect(self.edit_task)
        button_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete Task", self)
        self.delete_button.clicked.connect(self.delete_task)
        button_layout.addWidget(self.delete_button)

        self.complete_button = QPushButton("Mark Complete", self)
        self.complete_button.clicked.connect(self.mark_complete)
        button_layout.addWidget(self.complete_button)

        layout.addLayout(button_layout)

        # Task List
        self.task_list = QListWidget(self)
        layout.addWidget(self.task_list)

        # Load and save tasks on close
        self.setFixedSize(300, 400)

    def load_tasks(self):
        """Load tasks from a file."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.tasks = json.load(file)
                self.update_task_list()

    def save_tasks(self):
        """Save tasks to a file."""
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file)

    def update_task_list(self):
        """Update the display of tasks in the QListWidget."""
        self.task_list.clear()
        for task in self.tasks:
            status = "[✓] " if task['completed'] else "[✗] "
            self.task_list.addItem(status + task['title'])

    def add_task(self):
        """Add a new task."""
        title = self.task_input.text().strip()
        if title:
            self.tasks.append({'title': title, 'completed': False})
            self.save_tasks()
            self.update_task_list()
            self.task_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Task title cannot be empty.")

    def edit_task(self):
        """Edit the selected task."""
        current_row = self.task_list.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Selection Error", "No task selected to edit.")
            return

        new_title = self.task_input.text().strip()
        if new_title:
            self.tasks[current_row]['title'] = new_title
            self.save_tasks()
            self.update_task_list()
            self.task_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Task title cannot be empty.")

    def delete_task(self):
        """Delete the selected task."""
        current_row = self.task_list.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Selection Error", "No task selected to delete.")
            return

        del self.tasks[current_row]
        self.save_tasks()
        self.update_task_list()

    def mark_complete(self):
        """Mark the selected task as complete."""
        current_row = self.task_list.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Selection Error", "No task selected to mark as complete.")
            return

        self.tasks[current_row]['completed'] = True
        self.save_tasks()
        self.update_task_list()

def main():
    app = QApplication(sys.argv)
    manager = TaskManager()
    manager.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
