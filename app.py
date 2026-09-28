import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime
import json
import os


class CalendarReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar & Reminder App")
        self.root.geometry("950x650")
        self.root.minsize(850, 600)

        self.current_date = datetime.now()
        self.selected_date = self.current_date.strftime("%Y-%m-%d")
        self.reminders = self.load_reminders()

        self.setup_style()
        self.create_interface()
        self.show_calendar()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Title.TLabel",
            font=("Arial", 24, "bold")
        )

        style.configure(
            "Month.TLabel",
            font=("Arial", 18, "bold")
        )

        style.configure(
            "Day.TButton",
            font=("Arial", 11),
            padding=10
        )

        style.configure(
            "Action.TButton",
            font=("Arial", 11, "bold"),
            padding=8
        )

    def create_interface(self):
        title = ttk.Label(
            self.root,
            text="Calendar & Reminder",
            style="Title.TLabel"
        )
        title.pack(pady=(20, 10))

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=25, pady=10)

        calendar_frame = ttk.Frame(main_frame)
        calendar_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))

        navigation = ttk.Frame(calendar_frame)
        navigation.pack(fill="x", pady=10)

        previous_button = ttk.Button(
            navigation,
            text="◀ Previous",
            command=self.previous_month,
            style="Action.TButton"
        )
        previous_button.pack(side="left")

        self.month_label = ttk.Label(
            navigation,
            text="",
            style="Month.TLabel"
        )
        self.month_label.pack(side="left", expand=True)

        next_button = ttk.Button(
            navigation,
            text="Next ▶",
            command=self.next_month,
            style="Action.TButton"
        )
        next_button.pack(side="right")

        today_button = ttk.Button(
            calendar_frame,
            text="Today",
            command=self.go_to_today
        )
        today_button.pack(pady=(0, 10))

        self.calendar_grid = ttk.Frame(calendar_frame)
        self.calendar_grid.pack(fill="both", expand=True)

        reminder_frame = ttk.LabelFrame(
            main_frame,
            text="Reminders",
            padding=15
        )
        reminder_frame.pack(side="right", fill="y", ipadx=10)

        self.selected_label = ttk.Label(
            reminder_frame,
            text="Selected Date",
            font=("Arial", 13, "bold")
        )
        self.selected_label.pack(pady=(0, 10))

        self.reminder_list = tk.Listbox(
            reminder_frame,
            width=35,
            height=15,
            font=("Arial", 11)
        )
        self.reminder_list.pack(fill="both", expand=True, pady=5)

        add_button = ttk.Button(
            reminder_frame,
            text="Add Reminder",
            command=self.add_reminder,
            style="Action.TButton"
        )
        add_button.pack(fill="x", pady=(10, 5))

        delete_button = ttk.Button(
            reminder_frame,
            text="Delete Selected",
            command=self.delete_reminder,
            style="Action.TButton"
        )
        delete_button.pack(fill="x", pady=5)

        self.status_label = ttk.Label(
            self.root,
            text="Select a date from the calendar",
            anchor="center"
        )
        self.status_label.pack(fill="x", pady=10)

    def show_calendar(self):
        for widget in self.calendar_grid.winfo_children():
            widget.destroy()

        year = self.current_date.year
        month = self.current_date.month

        month_name = self.current_date.strftime("%B %Y")
        self.month_label.config(text=month_name)

        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        for column, day_name in enumerate(weekdays):
            label = ttk.Label(
                self.calendar_grid,
                text=day_name,
                anchor="center",
                font=("Arial", 11, "bold")
            )
            label.grid(
                row=0,
                column=column,
                sticky="nsew",
                padx=2,
                pady=5
            )

        month_calendar = calendar.monthcalendar(year, month)

        for row_index, week in enumerate(month_calendar, start=1):
            for column_index, day in enumerate(week):
                if day == 0:
                    continue

                date_value = f"{year:04d}-{month:02d}-{day:02d}"

                button = ttk.Button(
                    self.calendar_grid,
                    text=str(day),
                    command=lambda d=date_value: self.select_date(d),
                    style="Day.TButton"
                )

                button.grid(
                    row=row_index,
                    column=column_index,
                    sticky="nsew",
                    padx=2,
                    pady=2
                )

                if date_value == self.selected_date:
                    button.state(["pressed"])

        for column in range(7):
            self.calendar_grid.columnconfigure(
                column,
                weight=1
            )

        for row in range(len(month_calendar) + 1):
            self.calendar_grid.rowconfigure(
                row,
                weight=1
            )

        self.update_reminder_list()

    def select_date(self, date_value):
        self.selected_date = date_value
        self.update_reminder_list()
        self.show_calendar()

    def previous_month(self):
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(
                year=self.current_date.year - 1,
                month=12
            )
        else:
            self.current_date = self.current_date.replace(
                month=self.current_date.month - 1
            )

        self.show_calendar()

    def next_month(self):
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(
                year=self.current_date.year + 1,
                month=1
            )
        else:
            self.current_date = self.current_date.replace(
                month=self.current_date.month + 1
            )

        self.show_calendar()

    def go_to_today(self):
        self.current_date = datetime.now()
        self.selected_date = self.current_date.strftime("%Y-%m-%d")
        self.show_calendar()

    def add_reminder(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Reminder")
        dialog.geometry("400x280")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(
            dialog,
            text="Add Reminder",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        ttk.Label(
            dialog,
            text=f"Date: {self.selected_date}"
        ).pack(pady=5)

        ttk.Label(
            dialog,
            text="Reminder"
        ).pack(pady=(10, 3))

        reminder_entry = ttk.Entry(
            dialog,
            width=40
        )
        reminder_entry.pack(pady=5)

        ttk.Label(
            dialog,
            text="Time (HH:MM)"
        ).pack(pady=(10, 3))

        time_entry = ttk.Entry(
            dialog,
            width=20
        )
        time_entry.pack(pady=5)
        time_entry.insert(0, datetime.now().strftime("%H:%M"))

        def save_reminder():
            reminder_text = reminder_entry.get().strip()
            reminder_time = time_entry.get().strip()

            if not reminder_text:
                messagebox.showwarning(
                    "Missing Reminder",
                    "Please enter a reminder."
                )
                return

            try:
                datetime.strptime(reminder_time, "%H:%M")
            except ValueError:
                messagebox.showerror(
                    "Invalid Time",
                    "Please enter time in HH:MM format."
                )
                return

            if self.selected_date not in self.reminders:
                self.reminders[self.selected_date] = []

            self.reminders[self.selected_date].append({
                "time": reminder_time,
                "text": reminder_text
            })

            self.save_reminders()
            self.update_reminder_list()
            dialog.destroy()

            self.status_label.config(
                text="Reminder added successfully."
            )

        ttk.Button(
            dialog,
            text="Save Reminder",
            command=save_reminder,
            style="Action.TButton"
        ).pack(pady=15)

    def update_reminder_list(self):
        self.reminder_list.delete(0, tk.END)

        formatted_date = datetime.strptime(
            self.selected_date,
            "%Y-%m-%d"
        ).strftime("%d %B %Y")

        self.selected_label.config(
            text=f"Reminders\n{formatted_date}"
        )

        reminders = self.reminders.get(
            self.selected_date,
            []
        )

        if not reminders:
            self.reminder_list.insert(
                tk.END,
                "No reminders for this date."
            )
            return

        for reminder in reminders:
            display_text = (
                f"{reminder['time']} - "
                f"{reminder['text']}"
            )
            self.reminder_list.insert(
                tk.END,
                display_text
            )

    def delete_reminder(self):
        selection = self.reminder_list.curselection()

        if not selection:
            messagebox.showwarning(
                "Select Reminder",
                "Please select a reminder to delete."
            )
            return

        reminders = self.reminders.get(
            self.selected_date,
            []
        )

        if not reminders:
            return

        index = selection[0]

        if index >= len(reminders):
            return

        deleted = reminders.pop(index)

        if not reminders:
            self.reminders.pop(self.selected_date)

        self.save_reminders()
        self.update_reminder_list()

        self.status_label.config(
            text=f"Deleted: {deleted['text']}"
        )

    def load_reminders(self):
        file_name = "reminders.json"

        if not os.path.exists(file_name):
            return {}

        try:
            with open(
                file_name,
                "r",
                encoding="utf-8"
            ) as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return {}

    def save_reminders(self):
        with open(
            "reminders.json",
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                self.reminders,
                file,
                indent=4
            )


root = tk.Tk()
app = CalendarReminderApp(root)
root.mainloop()