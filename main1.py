import tkinter as tk
from tkinter import messagebox
import os

# File to store tasks
TASKS_FILE = "tasks.txt"

# Create main window
root = tk.Tk()
root.title("To-Do List")
root.geometry("400x500")
root.config(bg="#B570FF")

# Add a title label with some styling
title_label = tk.Label(root, text="To-Do List", font=("Helvetica", 18, "bold"), bg="#B570FF",fg="white")
title_label.pack(pady=20)

tasks = []  # Store task text and variable references

def add_task():
    task_text = task_entry.get().strip()
    if task_text:
        var = tk.BooleanVar()  # Checkbox variable
        task = (var, task_text)
        tasks.append(task)

        cb = tk.Checkbutton(task_frame_inner, text=task_text, variable=var, bg="#E5D4FF", anchor="w")
        cb.pack(fill="x", padx=5, pady=2, anchor="w")

        task_entry.delete(0, tk.END)
        update_scroll_region()
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

def remove_task():
    global tasks
    for widget in task_frame_inner.winfo_children():
        widget.destroy()  # Clear UI

    tasks = [(var, text) for var, text in tasks if not var.get()]  # Keep only unchecked tasks

    for var, text in tasks:
        cb = tk.Checkbutton(task_frame_inner, text=text, variable=var, bg="#E5D4FF", anchor="w")
        cb.pack(fill="x", padx=5, pady=2, anchor="w")

    update_scroll_region()

def clear_tasks():
    global tasks
    tasks.clear()
    for widget in task_frame_inner.winfo_children():
        widget.destroy()
    update_scroll_region()

def save_tasks():
    with open(TASKS_FILE, "w") as file:
        for var, text in tasks:
            file.write(f"{var.get()},{text}\n")  # Save task state (checked or not)
    messagebox.showinfo("Success", "Tasks saved successfully!")

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            for line in file:
                checked, text = line.strip().split(",", 1)
                var = tk.BooleanVar(value=checked == "1")  # Restore checked state
                tasks.append((var, text))

                cb = tk.Checkbutton(task_frame_inner, text=text, variable=var, bg="#E5D4FF", anchor="w")
                cb.pack(fill="x", padx=5, pady=2, anchor="w")

    update_scroll_region()

def update_scroll_region():
    task_frame_canvas.update_idletasks()
    task_frame_canvas.config(scrollregion=task_frame_canvas.bbox("all"))

# Input field
task_entry = tk.Entry(root, width=110)
task_entry.pack(pady=20)

# Buttons
button_frame=tk.Frame(root,bg="#B570FF")
button_frame.pack(pady=5)

add_button = tk.Button(button_frame, text="Add Task", command=add_task, bg="#39107B", fg="white", width=20)
add_button.pack(padx=10, side="left")

remove_button = tk.Button(button_frame, text="Remove Completed", command=remove_task,bg="#39107B", fg="white", width=20)
remove_button.pack(padx=10, side="left")

clear_button = tk.Button(button_frame, text="Clear All", command=clear_tasks,bg="#39107B", fg="white", width=20)
clear_button.pack(padx=10, side="left")

save_button = tk.Button(button_frame, text="Save Tasks", command=save_tasks, bg="#39107B", fg="white", width=20)
save_button.pack(padx=10, side="left")

# Task List with Scrollbar
task_frame_border = tk.Frame(root, bg="#7621FF", bd=3, relief="ridge")  # Border around tasks
task_frame_border.pack(pady=10, padx=10, fill="both", expand=True)

task_frame_canvas = tk.Canvas(task_frame_border, bg="#E5D4FF", height=200)
task_frame_canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(task_frame_border, orient="vertical", command=task_frame_canvas.yview)
scrollbar.pack(side="right", fill="y")

task_frame_canvas.configure(yscrollcommand=scrollbar.set)

task_frame_inner = tk.Frame(task_frame_canvas, bg="#E5D4FF")
task_frame_canvas.create_window((0, 0), window=task_frame_inner, anchor="nw")

# Load tasks when the app starts
load_tasks()

# Run the application
root.mainloop()