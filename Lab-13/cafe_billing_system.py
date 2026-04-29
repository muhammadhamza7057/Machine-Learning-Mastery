import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class CafeBillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("HUMVIX Cafe Billing System")
        self.root.geometry("1280x720")
        self.root.minsize(1200, 680)
        self.root.configure(bg="#f4efe8")

        self.items = {
            "Tea": {"price": 20, "suggestion": "Try a Sandwich with Tea"},
            "Coffee": {"price": 35, "suggestion": "Cookies or a Sandwich pair well"},
            "Sandwich": {"price": 60, "suggestion": "Add Coffee for a combo feel"},
            "Burger": {"price": 110, "suggestion": "Fries and Juice are great add-ons"},
            "Fries": {"price": 70, "suggestion": "Juice is a refreshing match"},
            "Juice": {"price": 50, "suggestion": "A light snack like Tea or Fries fits"},
        }

        self.name_var = tk.StringVar()
        self.contact_var = tk.StringVar()
        self.item_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.qty_var = tk.StringVar()
        self.manual_discount_var = tk.StringVar()
        self.time_var = tk.StringVar()
        self.suggestion_var = tk.StringVar(value="Select an item to see a smart suggestion.")
        self.status_var = tk.StringVar(value="Ready to generate bill.")
        self.cart_items = []

        self._configure_style()
        self._build_ui()
        self._set_default_item()
        self._update_clock()

    def _configure_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#f4efe8")
        style.configure("Card.TFrame", background="#fffaf4", relief="flat")
        style.configure("Header.TFrame", background="#1f3a5f")

        style.configure(
            "Title.TLabel",
            background="#1f3a5f",
            foreground="#ffffff",
            font=("Segoe UI", 22, "bold"),
        )
        style.configure(
            "SubTitle.TLabel",
            background="#1f3a5f",
            foreground="#d8e6ff",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Section.TLabel",
            background="#fffaf4",
            foreground="#1f3a5f",
            font=("Segoe UI", 12, "bold"),
        )
        style.configure(
            "Field.TLabel",
            background="#fffaf4",
            foreground="#3c3c3c",
            font=("Segoe UI", 9),
        )
        style.configure(
            "Hint.TLabel",
            background="#fffaf4",
            foreground="#6b5b4d",
            font=("Segoe UI", 9, "italic"),
        )
        style.configure(
            "Clock.TLabel",
            background="#1f3a5f",
            foreground="#ffdd99",
            font=("Segoe UI", 9, "bold"),
        )
        style.configure(
            "Status.TLabel",
            background="#f4efe8",
            foreground="#1f3a5f",
            font=("Segoe UI", 9, "bold"),
        )
        style.configure(
            "TButton",
            font=("Segoe UI", 9, "bold"),
            padding=(10, 6),
            background="#e3a857",
            foreground="#1f1f1f",
        )
        style.map(
            "TButton",
            background=[("active", "#f0bb67"), ("disabled", "#d7d0c6")],
            foreground=[("disabled", "#888888")],
        )
        style.configure(
            "Accent.TButton",
            font=("Segoe UI", 9, "bold"),
            padding=(10, 6),
            background="#1f3a5f",
            foreground="#ffffff",
        )
        style.map("Accent.TButton", background=[("active", "#27496f")])
        style.configure(
            "Danger.TButton",
            font=("Segoe UI", 9, "bold"),
            padding=(10, 6),
            background="#b93b3b",
            foreground="#ffffff",
        )
        style.map("Danger.TButton", background=[("active", "#d14b4b")])
        style.configure(
            "TEntry",
            padding=6,
            fieldbackground="#ffffff",
            bordercolor="#ccbca8",
            lightcolor="#ccbca8",
            darkcolor="#ccbca8",
        )
        style.configure(
            "TCombobox",
            padding=6,
            fieldbackground="#ffffff",
            background="#ffffff",
        )

    def _build_ui(self):
        header = ttk.Frame(self.root, style="Header.TFrame", padding=(24, 18))
        header.pack(fill="x")

        header_left = ttk.Frame(header, style="Header.TFrame")
        header_left.pack(side="left", fill="x", expand=True)

        ttk.Label(header_left, text="HUMVIX Cafe Billing System", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header_left,
            text="Tkinter widgets: Label, Entry, Button, Frame and Text with validation, cart support and smart billing rules",
            style="SubTitle.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        ttk.Label(header, textvariable=self.time_var, style="Clock.TLabel").pack(side="right", anchor="e")

        body = ttk.Frame(self.root, padding=14)
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        left_card = ttk.Frame(body, style="Card.TFrame", padding=14)
        left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left_card.columnconfigure(1, weight=1)

        right_card = ttk.Frame(body, style="Card.TFrame", padding=14)
        right_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        right_card.rowconfigure(1, weight=1)
        right_card.columnconfigure(0, weight=1)

        ttk.Label(left_card, text="Customer and Order Details", style="Section.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 14)
        )

        self._add_field(left_card, 1, "Customer Name", self.name_var)
        self._add_field(left_card, 2, "Contact Number", self.contact_var)

        ttk.Label(left_card, text="Cafe Item", style="Field.TLabel").grid(row=3, column=0, sticky="w", pady=8)
        self.item_combo = ttk.Combobox(
            left_card,
            textvariable=self.item_var,
            values=list(self.items.keys()),
            state="readonly",
            font=("Segoe UI", 10),
        )
        self.item_combo.grid(row=3, column=1, sticky="ew", pady=8)
        self.item_combo.bind("<<ComboboxSelected>>", self._on_item_selected)

        self._add_field(left_card, 4, "Item Price", self.price_var)
        self._add_field(left_card, 5, "Quantity", self.qty_var)
        self._add_field(left_card, 6, "Manual Discount (%)", self.manual_discount_var)

        ttk.Label(left_card, text="Smart suggestion", style="Field.TLabel").grid(row=7, column=0, sticky="nw", pady=(8, 0))
        ttk.Label(left_card, text="Smart suggestion", style="Field.TLabel").grid(row=7, column=0, sticky="nw", pady=(6, 0))
        suggestion_box = tk.Label(
            left_card,
            textvariable=self.suggestion_var,
            bg="#fff3df",
            fg="#7a4f13",
            font=("Segoe UI", 9, "italic"),
            wraplength=320,
            justify="left",
            padx=10,
            pady=8,
            relief="solid",
            bd=1,
        )
        suggestion_box.grid(row=7, column=1, sticky="ew", pady=(6, 0))

        ttk.Label(left_card, text="Selected Items (Cart)", style="Field.TLabel").grid(
            row=8, column=0, sticky="nw", pady=(10, 0)
        )
        cart_frame = ttk.Frame(left_card, style="Card.TFrame")
        cart_frame.grid(row=8, column=1, sticky="nsew", pady=(10, 0))
        cart_frame.columnconfigure(0, weight=1)
        cart_frame.rowconfigure(0, weight=1)

        self.cart_listbox = tk.Listbox(
            cart_frame,
            height=4,
            font=("Segoe UI", 9),
            bg="#fffdf9",
            fg="#2c2c2c",
            relief="solid",
            bd=1,
            activestyle="none",
        )
        self.cart_listbox.grid(row=0, column=0, sticky="nsew")


        ttk.Label(left_card, text="Add the current item with quantity to the cart before billing.", style="Hint.TLabel").grid(
            row=9, column=0, columnspan=2, sticky="w", pady=(6, 0)
        )

        button_row = ttk.Frame(left_card, style="Card.TFrame")
        button_row.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(14, 0))
        button_row.columnconfigure((0, 1, 2), weight=1)

        ttk.Button(button_row, text="Add Item", style="Accent.TButton", command=self.add_item_to_cart).grid(
            row=0, column=0, sticky="ew", padx=(0, 8)
        )

        ttk.Button(button_row, text="Generate Receipt", style="Accent.TButton", command=self.generate_receipt).grid(
            row=0, column=1, sticky="ew", padx=8
        )
        ttk.Button(button_row, text="Clear", command=self.clear_fields).grid(
            row=0, column=2, sticky="ew", padx=(8, 0)
        )
        ttk.Button(button_row, text="Exit", style="Danger.TButton", command=self.exit_app).grid(
            row=1, column=0, columnspan=3, sticky="ew", pady=(8, 0)
        )

        ttk.Label(right_card, text="Receipt", style="Section.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 8))

        receipt_frame = ttk.Frame(right_card, style="Card.TFrame")
        receipt_frame.grid(row=1, column=0, sticky="nsew")
        receipt_frame.rowconfigure(0, weight=1)
        receipt_frame.columnconfigure(0, weight=1)

        self.receipt_text = tk.Text(
            receipt_frame,
            wrap="word",
            font=("Consolas", 10),
            bg="#fffdf9",
            fg="#2c2c2c",
            insertbackground="#2c2c2c",
            relief="solid",
            bd=1,
            padx=10,
            pady=10,
        )
        self.receipt_text.grid(row=0, column=0, sticky="nsew")


        footer = ttk.Frame(self.root, padding=(18, 0, 18, 16))
        footer.pack(fill="x")
        ttk.Label(footer, textvariable=self.status_var, style="Status.TLabel").pack(anchor="w")

    def _add_field(self, parent, row, label_text, variable):
        ttk.Label(parent, text=label_text, style="Field.TLabel").grid(row=row, column=0, sticky="w", pady=8)
        entry = ttk.Entry(parent, textvariable=variable, font=("Segoe UI", 10))
        entry.grid(row=row, column=1, sticky="ew", pady=8)
        return entry

    def _set_default_item(self):
        default_item = list(self.items.keys())[0]
        self.item_var.set(default_item)
        self.price_var.set(str(self.items[default_item]["price"]))
        self.suggestion_var.set(self.items[default_item]["suggestion"])

    def _on_item_selected(self, _event=None):
        item_name = self.item_var.get()
        item_info = self.items.get(item_name)
        if item_info:
            self.price_var.set(str(item_info["price"]))
            self.suggestion_var.set(item_info["suggestion"])
            self.status_var.set(f"{item_name} selected. Price auto-filled and suggestion updated.")

    def add_item_to_cart(self):
        try:
            item_name = self.item_var.get().strip()
            if item_name not in self.items:
                raise ValueError("Please select a valid cafe item.")

            price = float(self.price_var.get().strip())
            quantity = int(self.qty_var.get().strip())

            if price <= 0:
                raise ValueError("Item price must be greater than zero.")
            if quantity <= 0:
                raise ValueError("Quantity must be greater than zero.")
        except ValueError as error:
            messagebox.showerror("Input Error", str(error))
            self.status_var.set("Please fix the item details before adding to cart.")
            return

        line_total = price * quantity
        self.cart_items.append({"item": item_name, "price": price, "quantity": quantity, "total": line_total})
        self.cart_listbox.insert(
            tk.END,
            f"{item_name}  x{quantity}  @ Rs. {price:.2f}  = Rs. {line_total:.2f}",
        )
        if self.cart_listbox.size() > 4:
            self.cart_listbox.delete(0)
        self.qty_var.set("")
        self.status_var.set(f"{item_name} added to cart. You can add more items.")

    def _update_clock(self):
        self.time_var.set(datetime.now().strftime("%d-%m-%Y %I:%M:%S %p"))
        self.root.after(1000, self._update_clock)

    def _validate_inputs(self):
        customer_name = self.name_var.get().strip()
        contact = self.contact_var.get().strip()
        manual_discount_text = self.manual_discount_var.get().strip()

        if not customer_name:
            raise ValueError("Customer name cannot be empty.")

        if not all(ch.isalpha() or ch.isspace() or ch in ".'-" for ch in customer_name):
            raise ValueError("Customer name should contain only letters and spaces.")

        if not contact.isdigit() or len(contact) != 10:
            raise ValueError("Contact number must contain exactly 10 digits.")

        if not self.cart_items:
            raise ValueError("Please add at least one item to the cart.")

        if manual_discount_text == "":
            manual_discount = 0.0
        else:
            try:
                manual_discount = float(manual_discount_text)
            except ValueError:
                raise ValueError("Manual discount must be numeric.") from None

        if manual_discount < 0:
            raise ValueError("Manual discount cannot be negative.")
        if manual_discount > 100:
            raise ValueError("Manual discount cannot exceed 100%.")

        return customer_name, contact, manual_discount

    def _smart_discount(self, subtotal, quantity):
        if subtotal >= 2000 or quantity >= 5:
            return 10.0, "High-value / bulk purchase rule applied"
        if subtotal >= 1000:
            return 5.0, "Mid-value purchase rule applied"
        return 0.0, "No automatic discount applied"

    def generate_receipt(self):
        try:
            customer_name, contact, manual_discount = self._validate_inputs()
        except ValueError as error:
            messagebox.showerror("Input Error", str(error))
            self.status_var.set("Validation failed. Please correct the highlighted inputs.")
            return

        subtotal = sum(item["total"] for item in self.cart_items)
        total_quantity = sum(item["quantity"] for item in self.cart_items)
        auto_discount_pct, discount_rule = self._smart_discount(subtotal, total_quantity)
        total_discount_pct = min(100.0, manual_discount + auto_discount_pct)
        discount_amount = subtotal * total_discount_pct / 100
        taxable_amount = subtotal - discount_amount
        tax_rate = 0.05
        tax_amount = taxable_amount * tax_rate
        final_total = taxable_amount + tax_amount

        cart_lines = [
            f"{index + 1}. {item['item']} x{item['quantity']} = Rs. {item['total']:.2f}"
            for index, item in enumerate(self.cart_items)
        ]

        receipt_lines = [
            "*" * 52,
            "                        HUMVIX",
            "                   CAFE BILLING SYSTEM",
            "*" * 52,
            f"Date/Time : {datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}",
            f"Customer  : {customer_name}",
            f"Contact   : {contact}",
            "-" * 52,
            "Items:",
            *cart_lines,
            "-" * 52,
            f"Discount  : {total_discount_pct:.2f}%",
            f"Discount Amount : Rs. {discount_amount:.2f}",
            f"Tax (5%)  : Rs. {tax_amount:.2f}",
            "-" * 52,
            f"Payable   : Rs. {final_total:.2f}",
            "-" * 52,
            "Thank you for visiting HUMVIX!",
            f"Rule: {discount_rule}",
        ]

        self.receipt_text.delete("1.0", tk.END)
        self.receipt_text.insert(tk.END, "\n".join(receipt_lines))
        self.status_var.set(f"Receipt generated for {customer_name}.")
        messagebox.showinfo("Success", "Receipt generated successfully.")

    def clear_fields(self):
        self.name_var.set("")
        self.contact_var.set("")
        self.qty_var.set("")
        self.manual_discount_var.set("")
        self.receipt_text.delete("1.0", tk.END)
        self.cart_items.clear()
        self.cart_listbox.delete(0, tk.END)
        self._set_default_item()
        self.status_var.set("Form cleared. Ready for a new bill.")

    def exit_app(self):
        if messagebox.askyesno("Exit Confirmation", "Do you really want to exit the billing system?"):
            self.root.destroy()


if __name__ == "__main__":
    app_root = tk.Tk()
    app = CafeBillingSystem(app_root)
    app_root.mainloop()
