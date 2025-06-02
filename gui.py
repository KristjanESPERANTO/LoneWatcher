import tkinter as tk
import tomllib

with open("config.toml", "rb") as file:
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
            # width is not fixed, but calculated based on the target name length
            width = min(len(target["name"]) * 6 + 150, 800)

            row_frame = tk.Frame(self.frame, bg="black", height=50, width=width)
            row_frame.grid(row=i, column=0, columnspan=3, sticky="ew", padx=5, pady=2)
            row_frame.grid_propagate(False)  # Prevent frame from shrinking

            status_label = tk.Label(
                row_frame,
                text="❓",
                font=("Arial", 14, "bold"),
                fg="white",
                bg="black",
                anchor="center",
                width=3,
            )
            status_label.grid(row=0, column=0, pady=15)

            actions_label = tk.Label(
                row_frame,
                text="",
                font=("Arial", 14, "bold"),
                fg="yellow",
                bg="black",
                anchor="center",
                width=3,
            )
            actions_label.grid(row=0, column=1, pady=15)

            name_label = tk.Label(
                row_frame,
                text=target["name"],
                font=("Arial", 14, "normal"),
                fg="white",
                bg="black",
                anchor="w",
            )
            name_label.grid(row=0, column=2, padx=5, pady=15)

            self.status_labels[target["name"]] = (status_label, actions_label, name_label, row_frame)

    def clear_highlight(self, row):
        status_label, actions_label, name_label, row_frame = row
        row_frame.configure(bg="black")
        status_label.configure(bg="black")
        actions_label.configure(bg="black")
        name_label.configure(bg="black")

    def update_status(self, target, success):
        status_label, actions_label, name_label, row_frame = self.status_labels[target["name"]]

        # Clear previous highlight if it exists
        if self.last_highlighted_row is not None:
            self.clear_highlight(self.last_highlighted_row)
            self.last_highlighted_row = None

        # Highlight the current row
        row_frame.configure(bg="#333333")
        status_label.configure(bg="#333333")
        actions_label.configure(bg="#333333")
        name_label.configure(bg="#333333")

        # Store current highlighted row
        self.last_highlighted_row = (status_label, actions_label, name_label, row_frame)

        # Schedule highlight removal for last row
        self.root.after(3000, lambda: self.clear_highlight((status_label, actions_label, name_label, row_frame)))

        if success:
            status_label.config(text="✔", fg="green")
            actions_label.config(text="")
        else:
            self.root.lift()
            status_label.config(text="❌", fg="red")
            actions_label.config(text="ℹ")
            actions_label.bind('<Button-1>', lambda e, t=target: self.show_action_popup(t))
            actions_label.config(cursor="hand2")  # Changes cursor to hand when hovering

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
