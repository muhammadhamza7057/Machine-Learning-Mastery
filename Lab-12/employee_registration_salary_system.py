import re
import tkinter as tk
from tkinter import messagebox, ttk


class EmployeeSalaryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Employee Registration and Salary Utility System")
        self.geometry("1120x760")
        self.minsize(1020, 700)
        self.configure(bg="#eef3f9")

        self._configure_styles()
        self._build_header()
        self._build_main_sections()
        self._build_status_bar()

    def _configure_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"), foreground="#123a5c", background="#dbe9f7")
        style.configure("SubHeader.TLabel", font=("Segoe UI", 11), foreground="#24455f", background="#dbe9f7")
        style.configure("Card.TLabelframe", background="#ffffff", borderwidth=1)
        style.configure("Card.TLabelframe.Label", font=("Segoe UI", 12, "bold"), foreground="#1c3f5d", background="#ffffff")
        style.configure("Body.TLabel", font=("Segoe UI", 10), background="#ffffff", foreground="#1f2937")
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.configure("Secondary.TButton", font=("Segoe UI", 10), padding=8)
        style.configure("Result.TLabel", font=("Segoe UI", 11, "bold"), background="#ffffff", foreground="#0a6e3f")
        style.configure("Error.TLabel", font=("Segoe UI", 9, "bold"), background="#ffffff", foreground="#b42318")
        style.configure("Success.TLabel", font=("Segoe UI", 9, "bold"), background="#ffffff", foreground="#0a6e3f")
        style.configure("FormTitle.TLabel", font=("Segoe UI", 11, "bold"), background="#ffffff", foreground="#163a56")
        style.configure("Hint.TLabel", font=("Segoe UI", 9), background="#ffffff", foreground="#425466")
        style.configure("Field.TLabel", font=("Segoe UI", 10, "bold"), background="#ffffff", foreground="#1f2937")
        style.configure("Main.TNotebook", background="#eef3f9", tabmargins=(8, 8, 8, 0))
        style.configure("Main.TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=(14, 8))

    def _build_header(self):
        header = tk.Frame(self, bg="#dbe9f7", bd=0, highlightthickness=0)
        header.pack(fill="x")

        ttk.Label(
            header,
            text="Employee Registration and Salary Utility System",
            style="Header.TLabel",
        ).pack(anchor="w", padx=20, pady=(18, 2))

        ttk.Label(
            header,
            text="HR operations demo: Tkinter introduction, registration form validation, and salary calculator",
            style="SubHeader.TLabel",
        ).pack(anchor="w", padx=22, pady=(0, 14))

    def _build_main_sections(self):
        container = tk.Frame(self, bg="#eef3f9")
        container.pack(fill="both", expand=True, padx=16, pady=10)

        canvas = tk.Canvas(container, bg="#eef3f9", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        content = tk.Frame(canvas, bg="#eef3f9")
        canvas_window = canvas.create_window((0, 0), window=content, anchor="nw")

        def _on_content_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def _on_canvas_configure(event):
            canvas.itemconfigure(canvas_window, width=event.width)

        content.bind("<Configure>", _on_content_configure)
        canvas.bind("<Configure>", _on_canvas_configure)

        # Enable mouse-wheel scrolling for long pages.
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        self._build_intro_card(content)
        self._build_registration_card(content)

        utility_row = tk.Frame(content, bg="#eef3f9")
        utility_row.pack(fill="both", expand=True)
        self._build_notice_card(utility_row)
        self._build_salary_card(utility_row)

    def _build_intro_card(self, parent):
        intro_frame = ttk.LabelFrame(parent, text="1) Tkinter Introduction and Advantages", style="Card.TLabelframe")
        intro_frame.pack(fill="both", expand=True, padx=6, pady=6)

        intro_text = (
            "Tkinter is Python's standard GUI toolkit used to build desktop applications with windows, forms, "
            "buttons, tables, and dialogs. It is highly suitable for office systems such as employee registration "
            "and payroll tools because it supports form-based workflows efficiently.\n\n"
            "Advantages in real desktop applications:\n"
            "1. Built-in and lightweight: Tkinter ships with Python, making deployment simple for office computers.\n"
            "2. Rapid development: HR teams can quickly get data-entry systems like employee registration forms.\n"
            "3. Cross-platform support: The same code runs on Windows, macOS, and Linux with minimal changes.\n"
            "4. Strong form controls: Entry widgets, labels, dropdowns, and validation patterns fit payroll workflows.\n"
            "5. Easy maintenance: Small and medium office tools remain readable and easy to update over time."
        )

        label = ttk.Label(intro_frame, text=intro_text, style="Body.TLabel", justify="left", wraplength=1000)
        label.pack(fill="x", padx=12, pady=10)

    def _build_notice_card(self, parent):
        notice_frame = ttk.LabelFrame(parent, text="2) HR Notice Window with Sticky Demo", style="Card.TLabelframe")
        notice_frame.pack(side="left", fill="both", expand=True, padx=6, pady=6)

        notice_frame.columnconfigure(0, weight=1)

        ttk.Label(
            notice_frame,
            text='Click to open notice window: "Welcome to Employee Registration and Salary Utility System"',
            style="Body.TLabel",
            wraplength=720,
            justify="left",
        ).grid(row=0, column=0, sticky="w", padx=12, pady=(10, 6))

        ttk.Button(
            notice_frame,
            text="Open Notice Window",
            style="Primary.TButton",
            command=self._open_notice_window,
        ).grid(row=1, column=0, sticky="w", padx=12, pady=(0, 12))

    def _open_notice_window(self):
        top = tk.Toplevel(self)
        top.title("HR Notice")
        top.geometry("780x400")
        top.configure(bg="#f4f8fc")

        top.columnconfigure(0, weight=1)
        top.rowconfigure(1, weight=1)

        title_label = tk.Label(
            top,
            text="Welcome to Employee Registration and Salary Utility System",
            font=("Segoe UI", 14, "bold"),
            bg="#f4f8fc",
            fg="#123a5c",
            pady=12,
        )
        title_label.grid(row=0, column=0, sticky="n")

        demo = tk.Frame(top, bg="#ffffff", bd=1, relief="solid")
        demo.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        demo.rowconfigure(0, weight=1)
        demo.columnconfigure(0, weight=1)

        center = tk.Frame(demo, bg="#ffffff")
        center.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        center.rowconfigure(0, weight=1)
        center.rowconfigure(1, weight=1)
        center.columnconfigure(0, weight=1)
        center.columnconfigure(1, weight=1)

        self._sticky_box(center, row=0, col=0, sticky="n", label_text="Sticky: N")
        self._sticky_box(center, row=0, col=1, sticky="e", label_text="Sticky: E")
        self._sticky_box(center, row=1, col=0, sticky="s", label_text="Sticky: S")
        self._sticky_box(center, row=1, col=1, sticky="w", label_text="Sticky: W")

    def _sticky_box(self, parent, row, col, sticky, label_text):
        box = tk.Frame(parent, width=280, height=120, bg="#edf3fb", bd=1, relief="ridge")
        box.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        box.grid_propagate(False)
        box.rowconfigure(0, weight=1)
        box.columnconfigure(0, weight=1)

        lbl = tk.Label(box, text=label_text, bg="#edf3fb", fg="#1c3f5d", font=("Segoe UI", 10, "bold"))
        lbl.grid(row=0, column=0, sticky=sticky, padx=8, pady=8)

    def _build_registration_card(self, parent):
        register_frame = ttk.LabelFrame(parent, text="3-4) Employee Registration Form", style="Card.TLabelframe")
        register_frame.pack(fill="both", expand=True, padx=6, pady=6)

        for i in range(2):
            register_frame.columnconfigure(i, weight=1)

        ttk.Label(
            register_frame,
            text="Fill all fields below to register an employee",
            style="FormTitle.TLabel",
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=12, pady=(10, 2))

        ttk.Label(
            register_frame,
            text="Fields marked with * are required",
            style="Hint.TLabel",
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=12, pady=(0, 8))

        labels = ["First Name *", "Last Name *", "Email Address *", "Department *"]
        for idx, text in enumerate(labels):
            ttk.Label(register_frame, text=text, style="Field.TLabel").grid(
                row=idx + 2, column=0, sticky="w", padx=12, pady=8
            )

        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.department_var = tk.StringVar()
        self.registration_feedback_var = tk.StringVar(value="")

        name_vcmd = (self.register(self._validate_name_keystroke), "%P")

        self.first_name_entry = ttk.Entry(
            register_frame,
            textvariable=self.first_name_var,
            validate="key",
            validatecommand=name_vcmd,
            width=34,
        )
        self.first_name_entry.grid(row=2, column=1, sticky="ew", padx=12, pady=8, ipady=3)

        self.last_name_entry = ttk.Entry(
            register_frame,
            textvariable=self.last_name_var,
            validate="key",
            validatecommand=name_vcmd,
            width=34,
        )
        self.last_name_entry.grid(row=3, column=1, sticky="ew", padx=12, pady=8, ipady=3)

        self.email_entry = ttk.Entry(register_frame, textvariable=self.email_var, width=34)
        self.email_entry.grid(row=4, column=1, sticky="ew", padx=12, pady=8, ipady=3)

        dept_combo = ttk.Combobox(
            register_frame,
            textvariable=self.department_var,
            values=["Human Resources", "Finance", "IT", "Operations", "Marketing"],
            state="readonly",
            width=32,
        )
        dept_combo.grid(row=5, column=1, sticky="ew", padx=12, pady=8, ipady=3)
        dept_combo.set("Select Department")
        self.department_combo = dept_combo

        btns = tk.Frame(register_frame, bg="#ffffff")
        btns.grid(row=6, column=0, columnspan=2, sticky="w", padx=12, pady=(10, 10))

        ttk.Button(btns, text="Submit", style="Primary.TButton", command=self._submit_registration).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(btns, text="Clear", style="Secondary.TButton", command=self._clear_registration).pack(side="left")

        self.registration_feedback_label = ttk.Label(
            register_frame,
            textvariable=self.registration_feedback_var,
            style="Error.TLabel",
            wraplength=420,
            justify="left",
        )
        self.registration_feedback_label.grid(row=7, column=0, columnspan=2, sticky="w", padx=12, pady=(0, 10))

    def _validate_name_keystroke(self, proposed_text):
        if proposed_text == "":
            return True
        return bool(re.fullmatch(r"[A-Za-z\s'-]+", proposed_text))

    def _get_registration_errors(self):
        first = self.first_name_var.get().strip()
        last = self.last_name_var.get().strip()
        email = self.email_var.get().strip()
        dept = self.department_var.get().strip()

        errors = []
        first_invalid = False
        last_invalid = False
        email_invalid = False
        dept_invalid = False

        name_pattern = re.compile(r"^[A-Za-z][A-Za-z\s'-]*$")
        email_pattern = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

        if not first:
            errors.append("First Name is required.")
            first_invalid = True
        elif not name_pattern.match(first):
            errors.append("First Name must contain only alphabets (no numbers).")
            first_invalid = True

        if not last:
            errors.append("Last Name is required.")
            last_invalid = True
        elif not name_pattern.match(last):
            errors.append("Last Name must contain only alphabets (no numbers).")
            last_invalid = True

        if not email:
            errors.append("Email Address is required.")
            email_invalid = True
        elif not email_pattern.match(email):
            errors.append("Email Address format is invalid.")
            email_invalid = True

        if not dept or dept == "Select Department":
            errors.append("Please select a Department.")
            dept_invalid = True

        return errors, first_invalid, last_invalid, email_invalid, dept_invalid

    def _submit_registration(self):
        first = self.first_name_var.get().strip()
        last = self.last_name_var.get().strip()
        email = self.email_var.get().strip()
        dept = self.department_var.get().strip()

        errors, first_invalid, last_invalid, email_invalid, dept_invalid = self._get_registration_errors()

        self.registration_feedback_label.configure(style="Error.TLabel")
        if first_invalid:
            self.first_name_entry.focus_set()
        elif last_invalid:
            self.last_name_entry.focus_set()
        elif email_invalid:
            self.email_entry.focus_set()
        elif dept_invalid:
            self.department_combo.focus_set()

        if errors:
            self.registration_feedback_var.set("Validation Errors: " + " | ".join(errors))
            messagebox.showerror("Validation Error", "\n".join(errors), parent=self)
            self.status_var.set("Registration validation failed.")
            return

        self.registration_feedback_label.configure(style="Success.TLabel")
        self.registration_feedback_var.set("Validation passed. Employee details submitted successfully.")
        messagebox.showinfo(
            "Registration Successful",
            f"Employee registered successfully.\n\nName: {first} {last}\nEmail: {email}\nDepartment: {dept}",
            parent=self,
        )
        self.status_var.set(f"Registered employee: {first} {last} ({dept})")

    def _clear_registration(self):
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.email_var.set("")
        self.department_var.set("Select Department")
        self.registration_feedback_label.configure(style="Error.TLabel")
        self.registration_feedback_var.set("")
        self.status_var.set("Registration form cleared.")

    def _build_salary_card(self, parent):
        salary_frame = ttk.LabelFrame(parent, text="5-6) Salary Utility Calculator", style="Card.TLabelframe")
        salary_frame.pack(side="left", fill="both", expand=True, padx=6, pady=6)

        salary_frame.columnconfigure(1, weight=1)

        ttk.Label(salary_frame, text="Daily Wage", style="Body.TLabel").grid(row=0, column=0, sticky="w", padx=12, pady=8)
        ttk.Label(salary_frame, text="Working Days", style="Body.TLabel").grid(row=1, column=0, sticky="w", padx=12, pady=8)

        self.daily_wage_var = tk.StringVar()
        self.working_days_var = tk.StringVar()
        self.salary_result_var = tk.StringVar(value="Total Salary: PKR 0.00")

        ttk.Entry(salary_frame, textvariable=self.daily_wage_var).grid(row=0, column=1, sticky="ew", padx=12, pady=8)
        ttk.Entry(salary_frame, textvariable=self.working_days_var).grid(row=1, column=1, sticky="ew", padx=12, pady=8)

        btn_area = tk.Frame(salary_frame, bg="#ffffff")
        btn_area.grid(row=2, column=0, columnspan=2, sticky="w", padx=12, pady=(8, 10))

        ttk.Button(btn_area, text="Calculate", style="Primary.TButton", command=self._calculate_salary).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(btn_area, text="Reset", style="Secondary.TButton", command=self._reset_salary).pack(side="left", padx=(0, 8))
        ttk.Button(btn_area, text="Exit", style="Secondary.TButton", command=self.destroy).pack(side="left")

        ttk.Label(salary_frame, textvariable=self.salary_result_var, style="Result.TLabel").grid(
            row=3, column=0, columnspan=2, sticky="w", padx=12, pady=(0, 12)
        )

    def _calculate_salary(self):
        wage_text = self.daily_wage_var.get().strip()
        days_text = self.working_days_var.get().strip()

        if not wage_text or not days_text:
            messagebox.showerror("Input Error", "Both Daily Wage and Working Days are required.", parent=self)
            self.status_var.set("Salary calculation failed: Missing input.")
            return

        try:
            daily_wage = float(wage_text)
            working_days = int(days_text)
            if daily_wage <= 0 or working_days <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Enter valid positive values.\nDaily Wage must be numeric and Working Days must be a positive integer.",
                parent=self,
            )
            self.status_var.set("Salary calculation failed: Invalid numeric values.")
            return

        total_salary = daily_wage * working_days
        self.salary_result_var.set(f"Total Salary: PKR {total_salary:,.2f}")
        self.status_var.set("Salary calculated successfully.")

    def _reset_salary(self):
        self.daily_wage_var.set("")
        self.working_days_var.set("")
        self.salary_result_var.set("Total Salary: PKR 0.00")
        self.status_var.set("Salary calculator reset.")

    def _build_status_bar(self):
        self.status_var = tk.StringVar(value="Ready")
        status = tk.Label(self, textvariable=self.status_var, anchor="w", bg="#dbe9f7", fg="#1f3a52", padx=14, pady=8)
        status.pack(fill="x", side="bottom")


if __name__ == "__main__":
    app = EmployeeSalaryApp()
    app.mainloop()
