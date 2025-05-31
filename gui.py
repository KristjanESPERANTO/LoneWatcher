import tkinter as tk
import tomllib

with open("system.toml", "rb") as file:
    system_info = tomllib.load(file)
    print(system_info)
    name = system_info["system"]["name"]
    version = system_info["system"]["version"]


class StatusGUI:
    def __init__(self, monitoring_targets):
        self.root = tk.Tk()
        self.root.title(f"{name} - {version}")
        icon = tk.PhotoImage(file="./icon/app_icon.png")
        self.root.iconphoto(True, icon)
        self.root.attributes("-alpha", 0.80)
        self.root.configure(bg="black")
        self.root.attributes("-topmost", True)

        # Main frame for table
        self.frame = tk.Frame(self.root, bg="black")
        self.frame.pack(padx=3, pady=3)

        # Store status labels
        self.status_labels = {}

        self.center_window()

        self.last_highlighted_row = None

        for i, target in enumerate(monitoring_targets):
            # width is not fixed, but calculated based on the target name length but max 550
            width = min(len(target["name"]) * 10 + 250, 800)

            row_frame = tk.Frame(self.frame, bg="black", height=50, width=width)
            row_frame.grid(row=i, column=0, columnspan=3, sticky="ew", padx=5, pady=2)
            row_frame.grid_propagate(False)  # Prevent frame from shrinking

            name_label = tk.Label(
                row_frame,
                text=target["name"],
                fg="white",
                bg="black",
                anchor="w",
                width=25,
            )
            name_label.grid(row=0, column=0, padx=5)

            status_label = tk.Label(
                row_frame, text="❓  ...", fg="white", bg="black", width=10
            )
            status_label.grid(row=0, column=1, padx=5)

            self.status_labels[target["name"]] = (name_label, status_label, row_frame)

    def clear_highlight(self, row):
        row_frame, status_label, name_label = row
        row_frame.configure(bg="black")
        status_label.configure(bg="black")
        name_label.configure(bg="black")

    def update_status(self, target, success):
        name_label, status_label, row_frame = self.status_labels[target["name"]]

        # Clear previous highlight if it exists
        if self.last_highlighted_row is not None:
            self.clear_highlight(self.last_highlighted_row)
            self.last_highlighted_row = None

        # Highlight the current row
        row_frame.configure(bg="#333333")
        status_label.configure(bg="#333333")
        name_label.configure(bg="#333333")

        # Store current highlighted row
        self.last_highlighted_row = (row_frame, status_label, name_label)

        # Schedule highlight removal for last row
        self.root.after(3000, lambda: self.clear_highlight((row_frame, status_label, name_label)))

        if success:
            status_label.config(text="✔", fg="green")
            if hasattr(row_frame, "action_button"):
                row_frame.action_button.destroy()
                del row_frame.action_button
        else:
            self.root.lift()
            self.root.focus_force()
            status_label.config(text="❌", fg="red")
            if not hasattr(row_frame, "action_button"):
                row_frame.action_button = tk.Button(
                    row_frame,
                    text="Details",
                    command=lambda t=target: self.show_action_popup(t),
                )
                row_frame.action_button.grid(row=0, column=2, padx=5)

    def show_action_popup(self, target):
        popup = tk.Toplevel(self.root)
        popup.title(f"Empfehlung für {target['name']}")  # TODO: translation
        popup.geometry("300x150")
        popup.configure(bg="white")

        tk.Label(
            popup,
            text=f"Empfohlene Aktion für\n{target['name']}",  # TODO: translation
            fg="black",
            bg="white",
            font=("Arial", 12, "bold"),
        ).pack(pady=10)
        tk.Label(
            popup, text=target["action"], fg="black", bg="white", wraplength=280
        ).pack(pady=5)

        tk.Button(popup, text="OK", command=popup.destroy).pack(pady=10)

    def start_gui(self):
        self.root.mainloop()

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set window position to screen center
        self.root.geometry(f"+{screen_width // 2}+{screen_height // 2}")
