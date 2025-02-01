import datetime
import tkinter as tk
from tkinter import messagebox

# Event Class to store individual event details
class Event:
    def __init__(self, name, start, end):
        self.name = name
        self.start = datetime.datetime.strptime(start, "%H:%M")
        self.end = datetime.datetime.strptime(end, "%H:%M")

    def __repr__(self):
        return f"{self.name}: {self.start.strftime('%H:%M')} - {self.end.strftime('%H:%M')}"

# Function to detect conflicts in the schedule
def detect_conflicts(events):
    events.sort(key=lambda x: x.start)  # Sort events by start time
    conflicts = []

    for i in range(len(events) - 1):
        if events[i].end > events[i + 1].start:  # Overlapping condition
            conflicts.append((events[i], events[i + 1]))

    return conflicts

# Function to suggest alternative slots within working hours
def suggest_alternative(event, existing_events, working_hours):
    start_of_day = datetime.datetime.strptime(working_hours[0], "%H:%M")
    end_of_day = datetime.datetime.strptime(working_hours[1], "%H:%M")

    # Check for free slots between events
    possible_start = max(start_of_day, max((e.end for e in existing_events if e.end <= event.start), default=start_of_day))
    possible_end = possible_start + (event.end - event.start)

    if possible_end <= end_of_day:
        return possible_start.strftime("%H:%M"), possible_end.strftime("%H:%M")

    return None

# Function to display the schedule
def display_schedule(events):
    sorted_events = sorted(events, key=lambda x: x.start)
    schedule = "Sorted Schedule:\n"
    for event in sorted_events:
        schedule += f"{event}\n"
    return schedule

# GUI Application
class EventSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Scheduler and Conflict Detector")

        self.events = []

        # Input Fields
        tk.Label(root, text="Event Name:").grid(row=0, column=0)
        self.event_name_entry = tk.Entry(root)
        self.event_name_entry.grid(row=0, column=1)

        tk.Label(root, text="Start Time (HH:MM):").grid(row=1, column=0)
        self.start_time_entry = tk.Entry(root)
        self.start_time_entry.grid(row=1, column=1)

        tk.Label(root, text="End Time (HH:MM):").grid(row=2, column=0)
        self.end_time_entry = tk.Entry(root)
        self.end_time_entry.grid(row=2, column=1)

        # Buttons
        tk.Button(root, text="Add Event", command=self.add_event).grid(row=3, column=0, pady=10)
        tk.Button(root, text="Detect Conflicts", command=self.detect_conflicts_gui).grid(row=3, column=1, pady=10)
        tk.Button(root, text="Show Schedule", command=self.show_schedule).grid(row=4, column=0, columnspan=2, pady=10)

    def add_event(self):
        name = self.event_name_entry.get()
        start = self.start_time_entry.get()
        end = self.end_time_entry.get()

        try:
            new_event = Event(name, start, end)
            self.events.append(new_event)
            messagebox.showinfo("Success", f"Event '{name}' added successfully!")

            # Clear input fields
            self.event_name_entry.delete(0, tk.END)
            self.start_time_entry.delete(0, tk.END)
            self.end_time_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid time format. Please use HH:MM.")

    def detect_conflicts_gui(self):
        conflicts = detect_conflicts(self.events)
        if conflicts:
            conflict_message = "Conflicting Events:\n"
            for e1, e2 in conflicts:
                conflict_message += f"{e1} and {e2}\n"

            # Suggest resolutions
            conflict_message += "\nSuggested Resolutions:\n"
            for e1, e2 in conflicts:
                alternative = suggest_alternative(e2, self.events, ("08:00", "18:00"))
                if alternative:
                    conflict_message += f"Reschedule {e2.name} to Start: {alternative[0]}, End: {alternative[1]}\n"
                else:
                    conflict_message += f"No available slot for {e2.name}\n"

            messagebox.showinfo("Conflicts Detected", conflict_message)
        else:
            messagebox.showinfo("No Conflicts", "No conflicts detected in the schedule.")

    def show_schedule(self):
        schedule = display_schedule(self.events)
        messagebox.showinfo("Schedule", schedule)

if __name__ == "__main__":
    root = tk.Tk()
    app = EventSchedulerApp(root)
    root.mainloop()
