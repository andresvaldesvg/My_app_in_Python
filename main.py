import tkinter as tk
from tkinter import messagebox, ttk
import time
import json

# Main Application Class
class TimeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracker App")
        self.root.geometry("600x400")

        # Initialize variables
        self.current_task = tk.StringVar()
        self.timer_running = False
        self.start_time = None
        self.records = []

        # Load past records
        self.load_records()

        # Header Section
        self.create_header()

        # Main Content
        self.create_main_content()

        # Footer Section
        self.create_footer()

    def create_header(self):
        header = tk.Frame(self.root, bg="#4CAF50", height=50)
        header.pack(fill=tk.X)
        
        title = tk.Label(header, text="Time Tracker", bg="#4CAF50", fg="white", font=("Arial", 18))
        title.pack(pady=10)

    def create_main_content(self):
        content = tk.Frame(self.root, bg="white", padx=20, pady=20)
        content.pack(fill=tk.BOTH, expand=True)

        # Task Entry
        tk.Label(content, text="App/Task Name:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(content, textvariable=self.current_task, font=("Arial", 12)).grid(row=0, column=1, pady=5)

        # Timer Display
        self.timer_label = tk.Label(content, text="00:00:00", font=("Arial", 20), fg="blue")
        self.timer_label.grid(row=1, column=0, columnspan=2, pady=20)

        # Start and Stop Buttons
        tk.Button(content, text="Start", command=self.start_timer, bg="#4CAF50", fg="white", font=("Arial", 12)).grid(row=2, column=0, padx=10)
        tk.Button(content, text="Stop", command=self.stop_timer, bg="#f44336", fg="white", font=("Arial", 12)).grid(row=2, column=1, padx=10)

    def create_footer(self):
        footer = tk.Frame(self.root, bg="#f1f1f1", padx=20, pady=10)
        footer.pack(fill=tk.X)

        # Records Display
        tk.Label(footer, text="Recorded Times:", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)
        
        self.record_list = ttk.Treeview(footer, columns=("Task", "Duration"), show="headings", height=5)
        self.record_list.column("Task", width=200)
        self.record_list.column("Duration", width=100)
        self.record_list.heading("Task", text="Task")
        self.record_list.heading("Duration", text="Duration")
        self.record_list.pack(fill=tk.X)

        # Save Button
        tk.Button(footer, text="Save Records", command=self.save_records, bg="#2196F3", fg="white", font=("Arial", 12)).pack(pady=10)

    def start_timer(self):
        if self.current_task.get() == "":
            messagebox.showwarning("Input Error", "Please enter a task name!")
            return
        
        if not self.timer_running:
            self.timer_running = True
            self.start_time = time.time()
            self.update_timer()

    def stop_timer(self):
        if self.timer_running:
            self.timer_running = False
            elapsed_time = time.time() - self.start_time
            formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

            self.records.append({"task": self.current_task.get(), "duration": formatted_time})
            self.update_record_list()
            self.reset_timer()

    def reset_timer(self):
        self.timer_label.config(text="00:00:00")
        self.start_time = None

    def update_timer(self):
        if self.timer_running:
            elapsed_time = time.time() - self.start_time
            formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
            self.timer_label.config(text=formatted_time)
            self.root.after(1000, self.update_timer)

    def update_record_list(self):
        self.record_list.delete(*self.record_list.get_children())
        for record in self.records:
            self.record_list.insert("", "end", values=(record["task"], record["duration"]))

    def save_records(self):
        with open("time_records.json", "w") as file:
            json.dump(self.records, file, indent=4)
        messagebox.showinfo("Save Successful", "Records saved successfully!")

    def load_records(self):
        try:
            with open("time_records.json", "r") as file:
                self.records = json.load(file)
        except FileNotFoundError:
            self.records = []

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackerApp(root)
    app.run()
