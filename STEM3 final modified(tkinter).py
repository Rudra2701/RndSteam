import tkinter as tk
from tkinter import messagebox
import time

class ScreenTimeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keldino SCREEN SAGE")  # Updated the window title
        
        self.screen_time_limit = 0
        self.break_time_limit = 0
        self.screen_time_left = 0
        self.break_time_left = 0
        self.break_time_active = False
        self.default_stop = False  # Whether to stop after a break
        
        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Screen time setup
        self.screen_time_label = tk.Label(self.root, text="Set Screen Time Limit (minutes):")
        self.screen_time_label.pack(pady=5)

        self.screen_time_entry = tk.Entry(self.root)
        self.screen_time_entry.pack(pady=5)
        
        # Break time setup
        self.break_time_label = tk.Label(self.root, text="Set Break Time (minutes):")
        self.break_time_label.pack(pady=5)

        self.break_time_entry = tk.Entry(self.root)
        self.break_time_entry.pack(pady=5)

        # Default stop option
        self.default_stop_var = tk.BooleanVar()
        self.default_stop_check = tk.Checkbutton(self.root, text="Stop after break", variable=self.default_stop_var)
        self.default_stop_check.pack(pady=5)
        
        # Start button
        self.start_button = tk.Button(self.root, text="Start", command=self.start)
        self.start_button.pack(pady=10)

        # Timer label
        self.timer_label = tk.Label(self.root, text="Timer: 00:00", font=("Helvetica", 16))
        self.timer_label.pack(pady=10)

        # Footer label with the name "KELDINO org"
        self.footer_label = tk.Label(self.root, text="KELDINO org", font=("Helvetica", 10, "italic"), fg="black")
        self.footer_label.pack(side="bottom", pady=30)

    def start(self):
        # Get screen time and break time values from the user
        try:
            self.screen_time_limit = int(self.screen_time_entry.get()) * 60  # Convert minutes to seconds
            self.break_time_limit = int(self.break_time_entry.get()) * 60  # Convert minutes to seconds
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for time limits.")
            return

        # Check whether the "Default Stop" option is selected
        self.default_stop = self.default_stop_var.get()

        self.screen_time_left = self.screen_time_limit
        self.break_time_left = self.break_time_limit
        self.break_time_active = False
        
        self.update_timer()

    def update_timer(self):
        if self.screen_time_left > 0 and not self.break_time_active:
            # Display screen time countdown
            minutes, seconds = divmod(self.screen_time_left, 60)
            self.timer_label.config(text=f"Screen Time: {minutes:02}:{seconds:02}")
            self.screen_time_left -= 1
            self.root.after(1000, self.update_timer)  # Update every second
        elif self.screen_time_left == 0 and not self.break_time_active:
            # Time for a break!
            self.break_time_active = True
            self.start_break_time()

    def start_break_time(self):
        messagebox.showinfo("Break Time", "It's time for a break! Take a 5-minute break.")
        self.break_time_left = self.break_time_limit
        self.break_timer()

    def break_timer(self):
        if self.break_time_left > 0:
            # Display break time countdown
            minutes, seconds = divmod(self.break_time_left, 60)
            self.timer_label.config(text=f"Break Time: {minutes:02}:{seconds:02}")
            self.break_time_left -= 1
            self.root.after(1000, self.break_timer)  # Update every second
        else:
            # Break is over
            if self.default_stop:
                messagebox.showinfo("Break Over", "Break is over! The timer has stopped.")
                self.timer_label.config(text="Timer Stopped")
            else:
                messagebox.showinfo("Break Over", "Break is over! Back to work.")
                self.break_time_active = False
                self.screen_time_left = self.screen_time_limit  # Reset screen time
                self.update_timer()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenTimeApp(root)
    root.mainloop()
