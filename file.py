import tkinter as tk
import time
from tkinter import ttk
from datetime import date
from tkinter import font
from tkinter import messagebox
from datetime import datetime
from tkcalendar import DateEntry
from tkcalendar import Calendar
import re
from tkinter import font
import queue


root = tk.Tk() #main window
root.title("To-Do List") #Title
root.geometry("350x350") #size of the window
root.config(background="#d3e2f0") #background color, low bottom part


# Create the frame using the custom style
border_frame = ttk.Frame(root, padding=80, relief="groove", width=50, height=50)
border_frame.pack(fill="both", expand=True,side='top')

# Add a label for the total number of tasks
# total_tasks_label = tk.Label(root, text="Total Tasks: 0/0")
# total_tasks_label.pack(pady=(0,0))

total_tasks_label = ttk.Label(root, text="Total Tasks: 0 (0%)")
total_tasks_label.pack(pady=(0,0))



#  progress bar
progress_frame = ttk.Frame(root)
progress_frame.pack(pady=(5, 0))
progress_label = ttk.Label(progress_frame, text="Progress")
progress_label.pack(side="left")

progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(side="left", padx=10)

title_frame = ttk.Frame(border_frame, padding=20,width=25)
title_frame.pack(fill="x")

# Initialize the progress bar value and the total task count label text
total_tasks_label.config(text="Total Tasks: 0",foreground="black", background="#d3e2f0") #Total task
progress_bar["value"] = 0



# Add the sword icon and "My Day" title

title_label = ttk.Label(title_frame)
title_label.pack(side="top", fill="both", pady=50, padx=(0,250), anchor="center")

sword_icon = tk.PhotoImage(file="logo.png").subsample(7,7)
sword_label = ttk.Label(title_label, image=sword_icon, text="TO-DO LIST", font=('Arial',25,'bold'), compound="left")
sword_label.pack(side="left", pady=10, anchor='nw')


def priority_sort_alpha(tasks):
    pq = queue.PriorityQueue()
    for task in tasks:
        pq.put(task.lower())
    sorted_tasks = []
    while not pq.empty():
        sorted_tasks.append(pq.get())
    return sorted_tasks


def sort_by_deadline(task_list):
    pq = queue.PriorityQueue()
    for task, deadline in task_list.items():
        pq.put((deadline, task))
    sorted_tasks = []
    while not pq.empty():
        sorted_tasks.append(pq.get()[1])
    return sorted_tasks


#Time/greeting
now = datetime.now()
greeting = ""
if now.hour < 12:
    greeting = "Good morning User!"
elif 12 <= now.hour < 18:
    greeting = "Good afternoon User!"
else:
    greeting = "Good evening User!"
greeting_label = ttk.Label(title_frame, text=greeting, font=("Arial", 25, "bold"), foreground="black", background="#d3e2f0") #greeting message
greeting_label.pack(side='left', anchor='nw',expand=False)



# Add the sorting symbol and options
sorting_frame = ttk.Frame(border_frame, padding=5)
sorting_frame.pack(fill="x")

sorting_options = ["Default", "Creation Date", "Alphabetically",'Deadline']
sorting_var = tk.StringVar(value="Default")
sorting_menu = ttk.OptionMenu(sorting_frame, sorting_var, *sorting_options)
sorting_menu.pack(side="right", padx=10)

sorting_label = ttk.Label(sorting_frame, text="Prioritise By:", font=("Arial",25))
sorting_label.pack(side="right")

# Add the current date
today = date.today()
date_label = ttk.Label(sorting_frame, text=today.strftime("%A, %B %d"), font=("Arial", 20))
date_label.pack(side="left")

# Create a box with a plus sign and a placeholder for adding tasks
#place where task in being input


add_task_frame = ttk.Frame(border_frame, padding=(5,10),width=12)
add_task_frame.pack(fill="x", pady=5)

add_task_label = ttk.Label(add_task_frame, text="Add Task: ", font=("Arial", 20))

add_task_label.pack(side="left")

add_task_entry = ttk.Entry(add_task_frame, font=("Arial", 20))
add_task_entry.pack(side="left", padx=10)


items={} #total number of task displayed
remainingTask=[] #for the progress bar
completedTask=[] #progress bar



#Progress bar 


def update_progress():
    total_tasks = len(task_frames)
    completed_tasks = sum(int(task_var.get()) for task_var in task_vars)
    percentage = int((completed_tasks / total_tasks + 1) * 100)
    total_tasks_label["text"] = f"Total Tasks: {completed_tasks}/{total_tasks} ({percentage}%)"

    progress_bar.config(maximum=total_tasks, value=completed_tasks)



# Create a label for the clock
def update_time():
    now = datetime.now()
    current_time = now.strftime("%I:%M:%S %p")
    clock_label.config(text="TIME:"+current_time)
    root.after(1000, update_time)

clock_label = ttk.Label(title_label, font=("Arial", 20, "bold"))
clock_label.pack(side="right", anchor="e", padx=10, pady=10)
update_time()

#clear button function
def delete_tasks():
    global task_frames, task_vars, task_list
    new_task_frames = []
    new_task_vars = []
    new_task_list = []
    for i in range(len(task_frames)):
        if not task_vars[i].get():
            new_task_frames.append(task_frames[i])
            new_task_vars.append(task_vars[i])
            new_task_list.append(task_list[i])
        else:
            task_frames[i].destroy()
    task_frames = new_task_frames
    task_vars = new_task_vars
    task_list = new_task_list
    update_progress()


deadline_label = ttk.Label(add_task_frame, text="Deadline:")
deadline_label.pack(side="left", padx=5, pady=5)

deadline_entry = ttk.Entry(add_task_frame, width=20)
deadline_entry.pack(side="left", padx=5, pady=5)


task_frames = []
task_vars = []
task_list = []
task_labels = []
task_deadline_vars=[]
task_no_deadline_vars=[]
#scrollbar
clear_button = ttk.Button(border_frame, text="Clear Tasks", command=delete_tasks)
clear_button.pack(side="left", padx=10)

# Add a new task, update the progress bar and completed task
# Create a canvas with a scrollbar for the tasks
canvas_frame = ttk.Frame(border_frame, height=80, width=100)
canvas_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(canvas_frame, height=75, width=100)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Add a frame inside the canvas to hold the tasks
tasks_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=tasks_frame, anchor="nw")

task_list = {}

def add_new_task(event=None):
    global task_frames, task_vars
    task_text = add_task_entry.get().strip()
    task_deadline = deadline_entry.get().strip()
    if not task_text:
        messagebox.showerror("Error", "Please enter a valid task.")
    elif task_text[0].isalpha():
        task_list[task_text] = task_deadline

        # Sort the task list based on the selected sorting option
        if sorting_var.get() == "Alphabetically":
            task_list_sorted = priority_sort_alpha(task_list.keys())
        elif sorting_var.get() == "Deadline":
            task_list_sorted = sort_by_deadline(task_list)
        elif sorting_var.get() == "Default" or sorting_var.get() == "Creation Date":
            task_list_sorted = [task.lower() for task in task_list]

        # Clear existing task frames and variables
        for frame in task_frames:
            frame.destroy()
        task_frames = []
        task_vars = []

        # Create new task frames and variables for all tasks
        for task_text in task_list_sorted:
            new_task_frame = ttk.Frame(tasks_frame, padding=10)
            new_task_frame.pack(fill="x", pady=1)

            task_var = tk.BooleanVar(value=False)
            task_checkbox = ttk.Checkbutton(new_task_frame, variable=task_var, command=update_progress)
            task_checkbox.pack(side="left", padx=10)

            task_label = ttk.Label(new_task_frame, text=task_text+" "+task_list[task_text], font=("Arial", 20))
            task_label.pack(side="left", padx=10)

            clear_button.pack_forget()  # Remove the button from its current position
            clear_button.pack(side="left", padx=0)

            task_frames.append(new_task_frame)
            task_vars.append(task_var)
            task_labels.append(task_label)

        add_task_entry.delete(0, "end")
    else:
        messagebox.showerror("Error", "Please enter a valid task.")

    # Update the scroll region of the canvas
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

    update_progress()

# Add a binding for the Enter key to add a new task
add_task_entry.bind("<Return>", add_new_task)
# deadline_entry.bind("<Return>", add_new_task)




#timer
def timeToString(time):
    diffInHrs = time / 3600000
    hh = int(diffInHrs)

    diffInMin = (diffInHrs - hh) * 60
    mm = int(diffInMin)

    diffInSec = (diffInMin - mm) * 60
    ss = int(diffInSec)

    diffInMs = (diffInSec - ss) * 100
    ms = int(diffInMs)

    formattedMM = str(mm).zfill(2)
    formattedSS = str(ss).zfill(2)
    formattedMS = str(ms).zfill(2)

    return f"{formattedMM}:{formattedSS}:{formattedMS}"



# Timer funtion
def countdowntimer():
    try:
        # user input
        user_input = int(hour.get()) * 3600 + int(minutes.get()) * 60 + int(seconds.get())
    except:
        # when the entered timer is not valid
        messagebox.showwarning('', 'Invalid Input!')
        return
    
    # Disable the entry fields while the timer is running
    hourEntry.config(state=tk.DISABLED)
    minuteEntry.config(state=tk.DISABLED)
    secondEntry.config(state=tk.DISABLED)
    
    # Start the timer
    startTime = time.time()
    while user_input > -1:
        # Calculate the remaining time
        elapsed_time = time.time() - startTime
        remaining_time = user_input - int(elapsed_time)

        # Convert the remaining time to a string and update the label
        time_str = timeToString(remaining_time * 1000)
        timeLabel.config(text=time_str)

        # Update the GUI
        root.update()
        time.sleep(0.01)

        # Stop the timer if the time is up
        if remaining_time == 0:
            messagebox.showinfo("Time Countdown", "Time Over")
            break

    # Enable the entry fields and reset the values
    hourEntry.config(state=tk.NORMAL)
    minuteEntry.config(state=tk.NORMAL)
    secondEntry.config(state=tk.NORMAL)
    hour.set('00')
    minutes.set('00')
    seconds.set('00')

# Create the user interface for the timer:
headerLabel = tk.Label(root, text="FOCUS TIMER", font=('Arial', 16, 'bold'))
headerLabel.pack(pady=10)

inputFrame = tk.Frame(root)
inputFrame.pack()

hourLabel = tk.Label(inputFrame, text="Hour", font=('Arial', 14, ""), foreground="blue")
hourLabel.grid(row=0, column=0, padx=2, pady=2)
hour = tk.StringVar(value='00')
hourEntry = tk.Entry(inputFrame, textvariable=hour, font=('Arial', 14, ""), width=3)
hourEntry.grid(row=0, column=1, padx=2, pady=2)

minuteLabel = tk.Label(inputFrame, text="Minute", font=('Arial', 14, ""), foreground="blue")
minuteLabel.grid(row=0, column=2, padx=2, pady=2)
minutes = tk.StringVar(value='00')
minuteEntry = tk.Entry(inputFrame, textvariable=minutes, font=('Arial', 14, ""), width=3)
minuteEntry.grid(row=0, column=3, padx=2, pady=2)



secondLabel = tk.Label(inputFrame, text="Second", font=('Arial', 14, ""), foreground="blue")
secondLabel.grid(row=0, column=4, padx=2, pady=2)
seconds = tk.StringVar(value='00')
secondEntry = tk.Entry(inputFrame, textvariable=seconds, font=('Arial', 14, ""), width=3)
secondEntry.grid(row=0, column=5, padx=2, pady=2)

startButton = tk.Button(root, text="Start", font=('Arial', 14, ""), command=countdowntimer)
startButton.pack(pady=10)

timeLabel = tk.Label(root, text="00:00:00", font=('Arial', 20, 'bold'))
timeLabel.pack()

root.mainloop()

#BUTTONS, BAR


error_label = ttk.Label(add_task_frame, text="", font=("Arial", 12), foreground="black", background="#d3e2f0")
error_label.pack(side="left", padx=10)

root.mainloop()