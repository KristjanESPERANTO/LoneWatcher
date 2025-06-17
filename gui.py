import tkinter as tk
import tomllib
import webbrowser

with open("config.toml", "rb") as file:
    VERSION = "0.3.0"
    CONFIG = tomllib.load(file)
    AUTHOR = "Kristjan ESPERANTO"
    LICENSE = "ISC"
    LICENSE_URL = "https://github.com/KristjanESPERANTO/LoneWatcher/blob/main/LICENSE.md"
    REPOSITORY = "https://github.com/KristjanESPERANTO/LoneWatcher"

    TITLE = (
        CONFIG["gui"]["custom_title"]
        if CONFIG["gui"]["custom_title"]
        else "LoneWatcher"
    )
    LANGUAGE = CONFIG["gui"]["language"]
    CHAR_WIDTH_MULTIPLIER = CONFIG["gui"]["char_width_multiplier"]
    ADDITIONAL_ROW_WIDTH = CONFIG["gui"]["additional_row_width"]
    MAX_ROW_WIDTH = CONFIG["gui"]["max_row_width"]
    FONT_SIZE = CONFIG["gui"]["font_size"]

with open("translations.toml", "rb") as file:
    translations = tomllib.load(file)
    translation = translations.get(LANGUAGE, translations["en"])

class StatusGUI:
    def __init__(self, monitoring_targets):
        self.root = tk.Tk()
        self.root.title(f"{TITLE} - v{VERSION}")
        icon = tk.PhotoImage(file="./icon/app_icon.png")
        self.root.iconphoto(True, icon)
        self.root.attributes("-alpha", 0.80)
        self.root.configure(bg="black")
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)

        # Main frame for table
        self.frame = tk.Frame(self.root, bg="black")
        self.frame.pack(padx=3, pady=3)

        # Store status labels
        self.status_labels = {}

        self.center_window()

        self.last_highlighted_row = None

        # Info button
        self.info_button = tk.Button(
            self.frame,
            text="ℹ",
            command=self.show_info,
            bg="black",
            fg="#555555",
            font=("Arial", FONT_SIZE-2, "bold"),
            borderwidth=0,
            highlightthickness=0,
            padx=5,
            pady=0
        )
        self.info_button.grid(row=0, column=3, sticky="ne")


        for i, target in enumerate(monitoring_targets):
            width = min(
                len(target["name"]) * CHAR_WIDTH_MULTIPLIER + ADDITIONAL_ROW_WIDTH,
                MAX_ROW_WIDTH,
            )

            row_frame = tk.Frame(self.frame, bg="black", height=50, width=width)
            row_frame.grid(row=i, column=0, columnspan=3, sticky="ew", padx=(15,0), pady=5)
            row_frame.grid_propagate(False)  # Prevent frame from shrinking

            status_label = tk.Label(
                row_frame,
                text="❓",
                font=("Arial", FONT_SIZE, "bold"),
                fg="white",
                bg="black",
                anchor="center",
                width=3,
            )
            status_label.grid(row=0, column=0, pady=15)

            actions_label = tk.Label(
                row_frame,
                text="",
                font=("Arial", FONT_SIZE, "bold"),
                fg="yellow",
                bg="black",
                anchor="center",
                width=3,
            )
            actions_label.grid(row=0, column=1, pady=15)

            name_label = tk.Label(
                row_frame,
                text=target["name"],
                font=("Arial", FONT_SIZE, "normal"),
                fg="white",
                bg="black",
                anchor="w",
            )
            name_label.grid(row=0, column=2, padx=5, pady=15)

            self.status_labels[target["name"]] = (
                status_label,
                actions_label,
                name_label,
                row_frame,
            )

    def clear_highlight(self, row):
        status_label, actions_label, name_label, row_frame = row
        row_frame.configure(bg="black")
        status_label.configure(bg="black")
        actions_label.configure(bg="black")
        name_label.configure(bg="black")

    def update_status(self, target, success):
        status_label, actions_label, name_label, row_frame = self.status_labels[
            target["name"]
        ]

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
        self.root.after(
            3000,
            lambda: self.clear_highlight(
                (status_label, actions_label, name_label, row_frame)
            ),
        )

        if success:
            status_label.config(text="✔", fg="green")
            actions_label.config(text="")
        else:
            self.root.lift()
            status_label.config(text="❌", fg="red")
            actions_label.config(text="ℹ")
            actions_label.bind(
                "<Button-1>", lambda e, t=target: self.show_action_popup(t)
            )
            actions_label.config(cursor="hand2")  # Changes cursor to hand when hovering

    def show_action_popup(self, target):
        popup = tk.Toplevel(self.root)
        popup.title(f"{translation['recommended_for']} {target['name']}")
        popup.geometry("300x150")
        popup.configure(bg="white")

        tk.Label(
            popup,
            text=f"{translation['recommended_action']}\n{target['name']}",
            fg="black",
            bg="white",
            font=("Arial", FONT_SIZE, "bold"),
        ).pack(pady=10)
        tk.Label(
            popup,
            text=target["action"],
            fg="black",
            bg="white",
            wraplength=280,
            font=("Arial", FONT_SIZE, "normal"),
        ).pack(pady=5)

        tk.Button(popup, text="OK", command=popup.destroy).pack(pady=10)

    def start_gui(self):
        self.root.mainloop()

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set window position to screen center
        self.root.geometry(f"+{screen_width // 2}+{screen_height // 2}")

    def show_info(self):
        popup = tk.Toplevel(self.root)
        popup.title(f"{TITLE} - v{VERSION}")
        popup.configure(bg="white")
        popup.resizable(False, False)
        popup.iconphoto(True, tk.PhotoImage(file="./icon/app_icon.png"))
        popup.attributes("-topmost", True)
        popup.attributes("-alpha", 0.95)
        popup.grab_set()
        popup.focus_set()
        popup.protocol("WM_DELETE_WINDOW", lambda: [popup.destroy(), self.info_button.config(state="normal")])

        info_frame = tk.Frame(popup, bg="white")
        info_frame.pack(padx=20, pady=20)

        tk.Label(
            info_frame,
            text=translation["description"],
            fg="black",
            bg="white",
            wraplength=400,
            font=("Arial", FONT_SIZE, "normal"),
        ).pack(pady=5)
        tk.Label(
            info_frame,
            text="Author",
            fg="black",
            bg="white",
            font=("Arial", FONT_SIZE, "bold"),
        ).pack(pady=(5,0))
        tk.Label(
            info_frame,
            text=AUTHOR,
            fg="black",
            bg="white",
            font=("Arial", FONT_SIZE, "normal"),
        ).pack(pady=(0,5))

        tk.Label(
            info_frame,
            text="License",
            fg="black",
            bg="white",
            font=("Arial", FONT_SIZE, "bold"),
        ).pack(pady=(5,0))
        license_label = tk.Label(
            info_frame,
            text=LICENSE,
            fg="blue",
            bg="white",
            font=("Arial", FONT_SIZE, "normal", "underline"),
            cursor="hand2"
        )
        license_label.pack(pady=(0,5))
        license_label.bind("<Button-1>", lambda e: open_url(LICENSE_URL))

        tk.Label(
            info_frame,
            text="Repository",
            fg="black",
            bg="white",
            font=("Arial", FONT_SIZE, "bold"),
        ).pack(pady=(5,0))
        url_label = tk.Label(
            info_frame,
            text=REPOSITORY,
            fg="blue",
            bg="white",
            font=("Arial", FONT_SIZE, "normal", "underline"),
            cursor="hand2"
        )
        url_label.pack(pady=(0,5))
        url_label.bind("<Button-1>", lambda e: open_url(REPOSITORY))

        def open_url(url):
            webbrowser.open(url)

        self.info_button.config(state="disabled")
