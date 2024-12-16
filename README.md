Task Manager Application
Overview
This Task Manager Application is designed to help users efficiently manage their tasks by adding, deleting, and sorting them. It features a user-friendly interface built with Python's Tkinter library. Users can input their tasks with deadlines, and the application allows them to sort tasks alphabetically or by deadline.

Features
Add Tasks: Users can input a task name, deadline, and set its status (e.g., completed or pending).
Delete Tasks: Tasks can be removed once they are completed or no longer needed.
Sort Tasks: Tasks can be sorted alphabetically or by deadline.
Progress Bar: Displays a progress bar to indicate the number of tasks completed.
Data Storage: Keeps track of tasks even after closing the application by saving task data.

Requirements
Python 3.x
Tkinter (for the graphical user interface)
Other dependencies can be installed via requirements.txt

Installation
To set up the project, follow these steps:

Clone the repository:
git clone https://github.com/yourusername/task-manager.git

Navigate into the project directory:
cd task-manager

Install the required dependencies:
pip install -r requirements.txt

Run the application:
python task_manager.py

Usage
1. Add a task: Enter the task name and deadline in the provided fields and click "Add Task".
2. Delete a task: Select a task from the list and click "Delete Task".
3. Sort tasks: Use the "Sort Alphabetically" and "Sort By Deadline" buttons to organize tasks.
4. Track progress: The progress bar will show the percentage of tasks marked as completed.
