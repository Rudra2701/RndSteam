import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import subprocess, os, time, threading

class KeldinoScreenTimeSage:
    def __init__(self, root):
        self.root = root
        self.root.title("KELDINO SCREENTIME SAGE")
        self.apps = []
        self.limit_secs = 0
        self.start_time = None
        self.running = False
        self.auto_stop = tk.BooleanVar(value=True)
        self.parental_pw = None

        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="KELDINO SCREENTIME SAGE", font=("Arial", 16, "bold")).pack(pady=5)
        tk.Label(self.root, text="Time Limit (minutes):").pack()
        self.limit_entry = tk.Entry(self.root); self.limit_entry.pack()

        tk.Checkbutton(self.root, text="Auto Stop", variable=self.auto_stop).pack()

        tk.Button(self.root, text="Add App", command=self.add_app).pack(pady=5)
        self.app_list = tk.Listbox(self.root, width=50); self.app_list.pack()

        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        tk.Button(frame, text="Start", command=self.start).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Stop", command=self.stop).pack(side=tk.RIGHT, padx=5)

        self.timer_label = tk.Label(self.root, text="Time Left: --:--:--", font=("Arial", 12))
        self.timer_label.pack(pady=5)

        self.canvas = tk.Canvas(self.root, width=200, height=200, bg="white")
        self.canvas.pack(pady=10)

        tk.Label(self.root, text="KELDINO org", font=("Arial", 8, "italic")).pack(pady=5)

    def add_app(self):
        path = filedialog.askopenfilename(title="Select App Executable")
        if path:
            name = os.path.basename(path)
            self.apps.append(name)
            self.app_list.insert(tk.END, name)

    def start(self):
        if not self.parental_pw:
            pw = simpledialog.askstring("Parental password", "Set a 6-digit password:")
            if not (pw and pw.isdigit() and len(pw) == 6):
                messagebox.showerror("Error", "Password must be 6 digits.")
                return
            self.parental_pw = pw

        try:
            mins = int(self.limit_entry.get())
            assert mins > 0
            self.limit_secs = mins * 60
        except:
            messagebox.showerror("Error", "Enter a valid positive integer for minutes.")
            return

        self.start_time = time.time()
        self.running = True
        threading.Thread(target=self.monitor_loop, daemon=True).start()
        threading.Thread(target=self.update_ui, daemon=True).start()
        messagebox.showinfo("Started", "Monitoring started.")

    def stop(self):
        if not self.running:
            return
        pw = simpledialog.askstring("Parental password", "Enter the 6-digit password to stop:")
        if pw == self.parental_pw:
            self.running = False
            messagebox.showinfo("Stopped", "Monitoring stopped.")
        else:
            messagebox.showerror("Error", "Incorrect password.")

    def is_running(self, app):
        try:
            out = subprocess.check_output("tasklist", creationflags=subprocess.CREATE_NO_WINDOW).decode()
            return app.lower() in out.lower()
        except:
            return False

    def kill_app(self, app):
        try:
            subprocess.call(["taskkill", "/f", "/im", app],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass

    def monitor_loop(self):
        while self.running:
            elapsed = time.time() - self.start_time
            if elapsed >= self.limit_secs:
                for app in self.apps:
                    if self.is_running(app):
                        self.kill_app(app)
                messagebox.showinfo("Time's Up", "Time limit reached. Apps were closed.")
                if self.auto_stop.get():
                    self.running = False
                else:
                    self.start_time = time.time()
            time.sleep(1)

    def update_ui(self):
        while self.running:
            elapsed = time.time() - self.start_time
            rem = max(0, self.limit_secs - elapsed)
            h, m = divmod(rem, 3600)
            m, s = divmod(m, 60)
            self.timer_label.config(text=f"Time Left: {int(h):02d}:{int(m):02d}:{int(s):02d}")
            self.draw_donut(elapsed)
            time.sleep(1)
        self.timer_label.config(text="Time Left: --:--:--")
        self.draw_donut(0)

    def draw_donut(self, elapsed):
        used = min(elapsed, self.limit_secs)
        extent = (used / self.limit_secs) * 360 if self.limit_secs else 0

        self.canvas.delete("all")
        self.canvas.create_arc(10, 10, 190, 190,
            start=90, extent=-extent,
            fill="#ff6666", outline="")
        self.canvas.create_oval(60, 60, 140, 140, fill="white", outline="")

if __name__ == "__main__":
    root = tk.Tk()
    app = KeldinoScreenTimeSage(root)
    root.mainloop()

