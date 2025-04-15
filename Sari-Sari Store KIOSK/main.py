import tkinter as tk
from tkinter import PhotoImage, Button, Label, Spinbox, Entry, messagebox, ttk, Frame
from tkinter.font import Font
import sqlite3

'''
PROGRAM MADE BY: JHERED MIGUEL C. REPUBLICA
DATE MADE: APRIL 3, 2025 - APRIL 15, 2025

KIOSK FUNCTIONS:
MAIN APPLICATION - SHOWS KIOSK FUNCTIONALITIES
CONTACT - NUMBER OF STORE
LOCATION - ADDRESS OF STORE
CATALOG - SHOWS 3 MENU TYPES (CHIPS, BISCUITS, DRINKS)
CHIPS - CHIPS CATALOG
BISCUITS - BISCUITS CATALOG
DRINKS - DRINKS CATALOG
'''

class Window:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Jazmine Sari-Sari Store KIOSK")
        self.root.resizable(width=False, height=False)
        self.root.geometry("1440x1024")
        # Create or connect to the database when the app starts
        self.setup_database()

    def setup_database(self):
        """Initialize the database with product sections and items"""
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()

        # Check if table exists, if not create it
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                section TEXT NOT NULL,
                stock INTEGER NOT NULL,
                price REAL NOT NULL
            )
        """)

        # Check if there are already products in the database
        cursor.execute("SELECT COUNT(*) FROM products")
        count = cursor.fetchone()[0]

        # Only insert default products if the database is empty
        if count == 0:
            # Insert CHIPS section products
            chips_products = [
                ('Ri-chee', 'CHIPS', 20, 10.00),
                ('Moby Red', 'CHIPS', 15, 15.00),
                ('Moby Yellow', 'CHIPS', 15, 15.00),
                ('Peewee', 'CHIPS', 25, 8.00),
                ('Roller Coaster', 'CHIPS', 18, 12.00),
                ('Mr. Chips', 'CHIPS', 20, 10.00),
                ('Tortillos', 'CHIPS', 15, 15.00),
                ('Cheese Ring', 'CHIPS', 22, 12.00),
                ('Onion Rings', 'CHIPS', 20, 12.00)
            ]

            # Insert BISCUITS section products
            biscuits_products = [
                ('Fudgee Bar', 'BISCUITS', 30, 8.00),
                ('Fita', 'BISCUITS', 25, 7.50),
                ('Skyflakes', 'BISCUITS', 25, 7.50),
                ('Rebisco', 'BISCUITS', 30, 6.00),
                ('Oreo', 'BISCUITS', 20, 15.00),
                ('Cream-O', 'BISCUITS', 20, 12.00),
                ('Dewberry', 'BISCUITS', 15, 18.00),
                ('Choco Mallows', 'BISCUITS', 15, 18.00),
                ('Chips Delight', 'BISCUITS', 20, 15.00)
            ]

            # Insert DRINKS section products
            drinks_products = [
                ('Spring Water', 'DRINKS', 50, 15.00),
                ('Mountain Dew', 'DRINKS', 30, 20.00),
                ('Fruit Soda', 'DRINKS', 25, 18.00),
                ('RC Cola', 'DRINKS', 30, 20.00),
                ('Pepsi', 'DRINKS', 30, 20.00),
                ('Royal', 'DRINKS', 25, 20.00),
                ('Coca-Cola', 'DRINKS', 35, 20.00),
                ('Fanta', 'DRINKS', 20, 20.00),
                ('Sprite', 'DRINKS', 25, 20.00)
            ]

            # Combine all products into one list
            all_products = chips_products + biscuits_products + drinks_products

            # Insert all products into the database
            cursor.executemany("INSERT INTO products (name, section, stock, price) VALUES (?, ?, ?, ?)", all_products)

        conn.commit()
        conn.close()

    def catalog(self):
        """Display the catalog of product categories"""
        # First destroy the current root window if it exists
        if hasattr(self, 'root') and self.root.winfo_exists():
            self.root.destroy()

        # Create a new window for the catalog
        self.new_root = tk.Tk()
        self.new_root.geometry("1440x1024")
        self.new_root.title("Catalog")
        self.new_root.resizable(width=False, height=False)

        # Load background image
        image = PhotoImage(file=r"Desktop - 9.png")
        logo = tk.Label(self.new_root, image=image)
        logo.place(x=0, y=0)

        # Save reference to prevent garbage collection
        self.catalog_background = image

        # Chips Group
        chips = PhotoImage(file=r"Frame 2.png")
        chips_button = Button(self.new_root, image=chips, command=self.chips_menu, borderwidth=0)
        chips_button.place(x=198, y=400)
        # Save reference
        self.chips_image = chips

        # Biscuits Group
        biscuits = PhotoImage(file=r"Frame 3.png")
        biscuits_button = Button(self.new_root, image=biscuits, command=self.biscuits_menu, borderwidth=0)
        biscuits_button.place(x=575, y=400)
        # Save reference
        self.biscuits_image = biscuits

        # Drinks Group
        drinks = PhotoImage(file=r"Frame 4.png")
        drinks_button = Button(self.new_root, image=drinks, command=self.drinks_menu, borderwidth=0)
        drinks_button.place(x=953, y=400)
        # Save reference
        self.drinks_image = drinks

        # Return to main menu button - using lambda to pass self to the return_to_main_menu method
        return_to_main_menu_button = Button(self.new_root,
                                            text="Return to Main Menu",
                                            font=("Baloo", 40),
                                            fg="#FFFFFF",
                                            bg="#FF3B3B",
                                            borderwidth=2,
                                            command=lambda: self.return_to_main_menu(),
                                            padx=30)
        return_to_main_menu_button.place(x=420, y=230)

        self.new_root.mainloop()

    # Add this as a separate method of your class
    def return_to_main_menu(self):
        """Handle returning to main menu"""
        # Safely check and destroy any active window
        for window_attr in ['new_root', 'contact_root', 'location_root']:
            if hasattr(self, window_attr):
                try:
                    window = getattr(self, window_attr)
                    if window.winfo_exists():
                        window.destroy()
                except (tk.TclError, AttributeError):
                    # Window was already destroyed or invalid
                    pass

        # Set flag to indicate we're returning to main menu
        self.returning_to_main = True

        # Reopen the main application
        self.main_application()

    def main_application(self):
        """Display the main application window"""
        # Check if we're returning from another window
        if hasattr(self, 'returning_to_main') and self.returning_to_main:
            # Create a fresh root window
            self.root = tk.Tk()
            self.returning_to_main = False  # Reset the flag
        else:
            # Create the main root window if it doesn't exist or has been destroyed
            # Safely check window existence
            root_exists = hasattr(self, 'root')
            try:
                if not root_exists or (root_exists and not self.root.winfo_exists()):
                    self.root = tk.Tk()
            except (tk.TclError, AttributeError):
                # If we get an error checking winfo_exists, we need a new window
                self.root = tk.Tk()

        # Continue with window setup
        self.root.geometry("1440x1024")
        self.root.title("Main Application")
        self.root.resizable(width=False, height=False)

        # Load and place background image
        image = PhotoImage(file=r"Desktop - 8.png")
        logo = tk.Label(self.root, image=image)
        logo.place(x=0, y=0)

        # Save reference to prevent garbage collection
        self.main_background = image

        # Create buttons
        button = Button(self.root,
                        text="Order now",
                        font=("Archivo Black", 16),
                        fg="#FFFFFF",
                        bg="#E9D149",
                        padx=12,
                        pady=3,
                        command=self.catalog)
        button2 = Button(self.root,
                         text="Order now",
                         font=("Archivo Black", 18),
                         fg="#FFFFFF",
                         bg="#E9D149",
                         padx=12,
                         pady=3,
                         command=self.catalog)
        menu_button = Button(self.root,
                             text="Menu",
                             font=("Baloo", 24),
                             fg="#FFFFFF",
                             bg="#FF3B3B",
                             borderwidth=0,
                             command=self.catalog)
        contact_button = Button(self.root,
                                text="Contact",
                                font=("Baloo", 24),
                                fg="#FFFFFF",
                                bg="#FF3B3B",
                                borderwidth=0,
                                command=self.open_contact)
        location_button = Button(self.root,
                                 text="Location",
                                 font=("Baloo", 24),
                                 fg="#FFFFFF",
                                 bg="#FF3B3B",
                                 borderwidth=0,
                                 command=self.open_location)
        inventory_button = Button(self.root,
                                  text="",
                                  font=("Baloo", 24),
                                  fg="#FFFFFF",
                                  bg="#FFFFFF",
                                  borderwidth=0,
                                  command=self.inventory_location)

        # Place buttons
        button.place(x=1120, y=78)
        button2.place(x=624, y=337)
        menu_button.place(x=650, y=67)
        contact_button.place(x=770, y=67)
        location_button.place(x=920, y=67)
        inventory_button.place(x=0, y=950)

        self.root.mainloop()

    def open_contact(self):
        self.root.destroy()
        self.contact_root = tk.Tk()
        self.contact_root.geometry("700x700")
        self.contact_root.title("Contact")
        self.contact_root.resizable(width=False, height=False)
        image = PhotoImage(file=r"final contact.png")
        logo = tk.Label(self.contact_root, image=image)
        logo.place(x=0, y=0)

        return_to_main_menu_button = Button(self.contact_root,
                                            text="Return to Main Menu",
                                            font=("Baloo", 28),
                                            fg="#FFFFFF",
                                            bg="#FF3B3B",
                                            borderwidth=2,
                                            command=lambda: self.return_to_main_menu(),
                                            padx=30)
        return_to_main_menu_button.place(x=130, y=550)

        self.contact_root.mainloop()

    def open_location(self):
        self.root.destroy()
        self.location_root = tk.Tk()
        self.location_root.geometry("700x700")
        self.location_root.title("Location")
        self.location_root.resizable(width=False, height=False)
        image = PhotoImage(file=r"final location.png")
        logo = tk.Label(self.location_root, image=image)
        logo.place(x=0, y=0)
        return_to_main_menu_button = Button(self.location_root,
                                            text="Return to Main Menu",
                                            font=("Baloo", 20),
                                            fg="#FFFFFF",
                                            bg="#FF3B3B",
                                            borderwidth=2,
                                            command=lambda: self.return_to_main_menu(),
                                            padx=10)
        return_to_main_menu_button.place(x=200, y=600)
        self.location_root.mainloop()

    def chips_menu(self):
        self.new_root.destroy()
        self.chips_root = tk.Tk()
        self.chips_root.geometry("1440x1024")
        self.chips_root.title("Chips")
        self.chips_root.resizable(width=False, height=False)
        image = PhotoImage(file=r"final chips.png")
        logo = tk.Label(self.chips_root, image=image)
        logo.place(x=0, y=0)

        # Dictionary to store spinbox references with product IDs
        self.spinboxes = {}

        # Initialize cart_items if it doesn't exist yet
        if not hasattr(self, 'cart_items'):
            self.cart_items = {}

        # Fetch chips products from the database
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, stock, price FROM products WHERE section = 'CHIPS'")
        chips_products = cursor.fetchall()
        conn.close()

        # Function to update shopping cart when spinbox value changes
        def update_cart(product_id, product_name, price):
            def callback(*args):
                quantity = int(self.spinboxes[product_id].get())
                if quantity > 0:
                    self.cart_items[product_id] = {
                        'name': product_name,
                        'quantity': quantity,
                        'price': price,
                        'total': quantity * price
                    }
                else:
                    if product_id in self.cart_items:
                        del self.cart_items[product_id]

                # Update cart display
                self.update_cart_display()

            return callback

        # Create spinboxes with product data
        positions = [
            (145, 335),  # Richee
            (358, 335),  # Moby Red
            (577, 335),  # Moby Yellow
            (790, 335),  # Peewee
            (145, 570),  # Roller Coaster
            (363, 570),  # Mr. Chips
            (577, 570),  # Tortillos
            (793, 570),  # Cheese Ring
            (150, 793),  # Onion Ring
        ]

        # Create spinboxes for each product
        for i, product in enumerate(chips_products):
            if i < len(positions):
                product_id, name, stock, price = product

                # Create StringVar to track spinbox changes
                var = tk.StringVar()
                var.set("0")

                # If item is already in cart, set spinbox to that value
                if product_id in self.cart_items:
                    var.set(str(self.cart_items[product_id]['quantity']))

                # Create spinbox with maximum value based on stock
                spinbox = Spinbox(
                    self.chips_root,
                    from_=0,
                    to=stock,
                    textvariable=var,
                    width=20
                )
                spinbox.place(x=positions[i][0], y=positions[i][1])

                # Store reference to spinbox and connect to update function
                self.spinboxes[product_id] = var
                var.trace("w", update_cart(product_id, name, price))

        # Create shopping cart frame - made taller (height from 400 to 550)
        cart_frame = Frame(self.chips_root, bg="white", bd=2, relief="ridge", width=300, height=1400)
        cart_frame.place(x=1075, y=200)  # Moved up from y=300 to y=200

        # Cart title
        cart_title = Label(cart_frame, text="Shopping Cart", font=("Archivo Black", 16), bg="white", fg="#FF3B3B")
        cart_title.pack(pady=10)

        # Create Text widget to display cart items - made taller (height from 15 to 22)
        self.cart_text = tk.Text(cart_frame, width=35, height=22, wrap="word", bg="white")
        self.cart_text.pack(padx=10, pady=5)

        # Subtotal
        self.cart_subtotal_label = Label(cart_frame, text="Subtotal: ₱0.00", font=("Arial", 12), bg="white")
        self.cart_subtotal_label.pack(pady=5)

        # VAT (12%)
        self.cart_vat_label = Label(cart_frame, text="VAT (12%): ₱0.00", font=("Arial", 12), bg="white")
        self.cart_vat_label.pack(pady=5)

        # Cart total
        self.cart_total_label = Label(cart_frame, text="Total: ₱0.00", font=("Arial", 14, "bold"), bg="white")
        self.cart_total_label.pack(pady=5)

        # Update cart display with existing items
        self.update_cart_display()

        # Back button - now saves cart when going back
        back_button = Button(self.chips_root,
                             text="Back",
                             font=("Baloo", 40),
                             fg="#FFFFFF",
                             bg="#FF3B3B",
                             borderwidth=2,
                             command=self.save_cart_and_go_back,
                             padx=30)

        # Review and Pay button - now redirects to shopping cart
        review_and_pay_button = Button(self.chips_root,
                                       text="Review + Pay for Order",
                                       font=("Baloo", 40),
                                       fg="#FFFFFF",
                                       bg="#FF3B3B",
                                       borderwidth=2,
                                       command=self.shopping_cart,  # Changed to shopping_cart
                                       padx=130)

        back_button.place(x=1120, y=870)
        review_and_pay_button.place(x=100, y=870)

        self.chips_root.mainloop()

    def save_cart_and_go_back(self):
        """Save cart contents and go back to catalog"""
        # Cart is already saved in self.cart_items, just go back
        self.chips_root.destroy()
        self.root = tk.Tk()
        self.root.geometry("1440x1024")
        self.root.title("Jazmine Sari-Sari Store KIOSK")
        self.root.resizable(width=False, height=False)
        self.catalog()

    def update_cart_display(self):
        """Update the shopping cart display in product menus"""
        # This method should be the same across all menu types
        # Update cart summary
        cart_subtotal = sum(item['total'] for item in self.cart_items.values())
        vat = cart_subtotal * 0.12
        cart_total = cart_subtotal + vat

        # Clear current cart display
        self.cart_text.delete(1.0, tk.END)

        # Add items to cart display
        if not self.cart_items:
            self.cart_text.insert(tk.END, "Your cart is empty.\n\n")
        else:
            for item_id, details in self.cart_items.items():
                self.cart_text.insert(tk.END, f"{details['name']}\n")
                self.cart_text.insert(tk.END,
                                      f"  {details['quantity']} × ₱{details['price']:.2f} = ₱{details['total']:.2f}\n\n")

        # Update labels
        self.cart_subtotal_label.config(text=f"Subtotal: ₱{cart_subtotal:.2f}")
        self.cart_vat_label.config(text=f"VAT (12%): ₱{vat:.2f}")
        self.cart_total_label.config(text=f"Total: ₱{cart_total:.2f}")

    def shopping_cart(self):
        """Display shopping cart contents and provide checkout options"""
        # Save which menu we came from
        self.last_menu = None

        # Properly check if the Tkinter windows exist before trying to destroy them
        try:
            if hasattr(self, 'chips_root') and self.chips_root.winfo_exists():
                self.last_menu = "chips"
                self.chips_root.destroy()
        except (AttributeError, tk.TclError):
            pass

        try:
            if hasattr(self, 'biscuits_root') and self.biscuits_root.winfo_exists():
                self.last_menu = "biscuits"
                self.biscuits_root.destroy()
        except (AttributeError, tk.TclError):
            pass

        try:
            if hasattr(self, 'drinks_root') and self.drinks_root.winfo_exists():
                self.last_menu = "drinks"
                self.drinks_root.destroy()
        except (AttributeError, tk.TclError):
            pass

        # Create a new window for the shopping cart
        self.cart_root = tk.Tk()
        self.cart_root.geometry("1440x1024")
        self.cart_root.title("Shopping Cart")
        self.cart_root.resizable(width=False, height=False)

        # Load the shopping cart background image
        image = PhotoImage(file=r"cart final.png")
        logo = tk.Label(self.cart_root, image=image)
        logo.place(x=0, y=0)

        # Keep a reference to the image to prevent garbage collection
        self.cart_background_image = image

        # Create a frame to display cart items - made bigger
        cart_display_frame = Frame(self.cart_root, bg="white", bd=2, relief="ridge", width=900, height=500)
        cart_display_frame.place(x=370, y=100)

        # Add cart title
        cart_title = Label(cart_display_frame, text="Your Shopping Cart", font=("Archivo Black", 24), bg="white",
                           fg="#FF3B3B")
        cart_title.pack(pady=20)

        # Create cart items list with scrollbar
        cart_items_frame = Frame(cart_display_frame, bg="white", width=850, height=450)
        cart_items_frame.pack(pady=10)

        # Headers for cart items
        headers_frame = Frame(cart_items_frame, bg="white")
        headers_frame.pack(fill="x", pady=5)

        Label(headers_frame, text="Item", font=("Arial", 16, "bold"), bg="white", width=20).grid(row=0, column=0)
        Label(headers_frame, text="Quantity", font=("Arial", 16, "bold"), bg="white", width=10).grid(row=0, column=1)
        Label(headers_frame, text="Price", font=("Arial", 16, "bold"), bg="white", width=10).grid(row=0, column=2)
        Label(headers_frame, text="Total", font=("Arial", 16, "bold"), bg="white", width=10).grid(row=0, column=3)
        Label(headers_frame, text="Actions", font=("Arial", 16, "bold"), bg="white", width=10).grid(row=0,
                                                                                                    column=4)  # New column for edit/remove buttons

        # Separator
        Frame(cart_items_frame, height=2, bg="#FF3B3B").pack(fill="x", pady=5)

        # Create a canvas with scrollbar for items
        canvas = tk.Canvas(cart_items_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(cart_items_frame, orient="vertical", command=canvas.yview)

        # Configure the scrollable frame
        scrollable_frame = Frame(canvas, bg="white")
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Create a window inside the canvas to hold the scrollable frame
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Display cart items
        row = 0
        cart_subtotal = 0

        if not self.cart_items:
            Label(scrollable_frame, text="Your cart is empty", font=("Arial", 16), bg="white", fg="#888888").grid(
                row=0, column=0, columnspan=5, pady=20)
        else:
            for item_id, details in self.cart_items.items():
                Label(scrollable_frame, text=details['name'], font=("Arial", 14), bg="white", width=20).grid(
                    row=row, column=0, pady=10, sticky="w")
                Label(scrollable_frame, text=str(details['quantity']), font=("Arial", 14), bg="white", width=10).grid(
                    row=row, column=1)
                Label(scrollable_frame, text=f"₱{details['price']:.2f}", font=("Arial", 14), bg="white", width=10).grid(
                    row=row, column=2)
                Label(scrollable_frame, text=f"₱{details['total']:.2f}", font=("Arial", 14), bg="white", width=10).grid(
                    row=row, column=3)

                # Add edit button to modify cart item
                edit_frame = Frame(scrollable_frame, bg="white")
                edit_frame.grid(row=row, column=4, pady=10)

                # Edit button navigates to the appropriate product menu
                edit_button = Button(
                    edit_frame,
                    text="Edit",
                    font=("Arial", 10),
                    bg="#4CAF50",
                    fg="white",
                    command=lambda id=item_id: self.edit_cart_item(id),
                    padx=5
                )
                edit_button.pack(side="left", padx=2)

                # Remove button removes the item from cart
                remove_button = Button(
                    edit_frame,
                    text="✖",
                    font=("Arial", 10),
                    bg="#FF3B3B",
                    fg="white",
                    command=lambda id=item_id: self.remove_cart_item(id, scrollable_frame),
                    padx=5
                )
                remove_button.pack(side="left", padx=2)

                row += 1
                cart_subtotal += details['total']

        # Calculate VAT (12%)
        vat = cart_subtotal * 0.12
        cart_total = cart_subtotal + vat

        # Total frame
        total_frame = Frame(cart_display_frame, bg="white")
        total_frame.pack(fill="x", pady=10)

        # Separator
        Frame(total_frame, height=2, bg="#FF3B3B").pack(fill="x", pady=10)

        # Summary of totals - using grid for better layout
        totals_grid = Frame(total_frame, bg="white")
        totals_grid.pack(pady=10)

        # Subtotal row
        Label(totals_grid, text="Subtotal:", font=("Arial", 14), bg="white").grid(row=0, column=0, sticky="w", padx=20,
                                                                                  pady=5)
        self.subtotal_value = Label(totals_grid, text=f"₱{cart_subtotal:.2f}", font=("Arial", 14), bg="white")
        self.subtotal_value.grid(row=0, column=1, sticky="e", padx=20, pady=5)

        # VAT row
        Label(totals_grid, text="VAT (12%):", font=("Arial", 14), bg="white").grid(row=1, column=0, sticky="w", padx=20,
                                                                                   pady=5)
        self.vat_value = Label(totals_grid, text=f"₱{vat:.2f}", font=("Arial", 14), bg="white")
        self.vat_value.grid(row=1, column=1, sticky="e", padx=20, pady=5)

        # Total row
        Label(totals_grid, text="Total Amount:", font=("Arial", 16, "bold"), bg="white").grid(row=2, column=0,
                                                                                              sticky="w", padx=20,
                                                                                              pady=10)
        self.total_value = Label(totals_grid, text=f"₱{cart_total:.2f}", font=("Arial", 16, "bold"), bg="white",
                                 fg="#FF3B3B")
        self.total_value.grid(row=2, column=1, sticky="e", padx=20, pady=10)

        # Payment section
        payment_frame = Frame(cart_display_frame, bg="white", bd=2, relief="groove")
        payment_frame.pack(fill="x", padx=20, pady=10)

        # Payment title
        Label(payment_frame, text="Payment", font=("Archivo Black", 18), bg="white", fg="#FF3B3B").pack(pady=10)

        # Tender amount entry
        tender_frame = Frame(payment_frame, bg="white")
        tender_frame.pack(pady=10)

        Label(tender_frame, text="Cash Tendered:", font=("Arial", 14), bg="white").pack(side="left", padx=10)
        self.tender_entry = Entry(tender_frame, font=("Arial", 14), width=15)
        self.tender_entry.pack(side="left", padx=10)
        self.tender_entry.insert(0, f"{cart_total:.2f}")  # Default to exact amount

        # Change display
        self.change_frame = Frame(payment_frame, bg="white")
        self.change_frame.pack(pady=10, fill="x")

        Label(self.change_frame, text="Change:", font=("Arial", 14), bg="white").pack(side="left", padx=10)
        self.change_value = Label(self.change_frame, text="₱0.00", font=("Arial", 14, "bold"), bg="white")
        self.change_value.pack(side="left", padx=10)

        # Function to calculate change when tender amount is entered
        def calculate_change(*args):
            try:
                tendered = float(self.tender_entry.get())
                change = tendered - cart_total
                if change >= 0:
                    self.change_value.config(text=f"₱{change:.2f}")
                else:
                    self.change_value.config(text="Insufficient amount")
            except ValueError:
                self.change_value.config(text="Invalid input")

        # Bind the entry to update change when value changes
        self.tender_entry.bind("<KeyRelease>", calculate_change)

        # Pay button in payment frame
        pay_button = Button(payment_frame,
                            text="Pay Now",
                            font=("Archivo Black", 16),
                            fg="#FFFFFF",
                            bg="#4CAF50",  # Green color for Pay button
                            borderwidth=2,
                            command=lambda: self.process_payment(cart_total),
                            padx=20,
                            pady=5)
        pay_button.pack(pady=10)

        # Buttons frame at bottom
        buttons_frame = Frame(self.cart_root, bg="transparent")
        buttons_frame.place(x=100, y=850)  # Adjusted position to fit continue shopping buttons

        # Back button - now returns to the appropriate menu
        back_button = Button(buttons_frame,
                             text="Back to Shopping",
                             font=("Baloo", 30),
                             fg="#FFFFFF",
                             bg="#FF3B3B",
                             borderwidth=2,
                             command=self.back_to_menu_from_cart,
                             padx=30)
        back_button.pack(side="left", padx=20)

        # Continue shopping buttons for each category
        shop_chips_button = Button(buttons_frame,
                                   text="Shop Chips",
                                   font=("Baloo", 30),
                                   fg="#FFFFFF",
                                   bg="#4CAF50",
                                   borderwidth=2,
                                   command=self.shop_chips_from_cart,
                                   padx=10)
        shop_chips_button.pack(side="left", padx=5)

        shop_biscuits_button = Button(buttons_frame,
                                      text="Shop Biscuits",
                                      font=("Baloo", 30),
                                      fg="#FFFFFF",
                                      bg="#FF9800",  # Orange color
                                      borderwidth=2,
                                      command=self.shop_biscuits_from_cart,
                                      padx=10)
        shop_biscuits_button.pack(side="left", padx=5)

        shop_drinks_button = Button(buttons_frame,
                                    text="Shop Drinks",
                                    font=("Baloo", 30),
                                    fg="#FFFFFF",
                                    bg="#2196F3",  # Blue color
                                    borderwidth=2,
                                    command=self.shop_drinks_from_cart,
                                    padx=10)
        shop_drinks_button.pack(side="left", padx=5)

        # Configure the canvas for mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Set a fixed height for the canvas to ensure scrollbar appears when needed
        canvas.config(height=300)

        # Calculate change on load
        calculate_change()

        self.cart_root.mainloop()

    def process_payment(self, total_amount):
        """Process payment and complete the transaction"""
        if not self.cart_items:
            messagebox.showinfo("Cart Empty", "Please add items to your cart first.")
            return

        try:
            tendered = float(self.tender_entry.get())
            if tendered < total_amount:
                messagebox.showerror("Payment Error", "Insufficient amount tendered.")
                return

            change = tendered - total_amount

            # Update inventory in database
            conn = sqlite3.connect("inventory.db")
            cursor = conn.cursor()

            try:
                for product_id, details in self.cart_items.items():
                    # Get current stock
                    cursor.execute("SELECT stock FROM products WHERE id = ?", (product_id,))
                    current_stock = cursor.fetchone()[0]

                    # Calculate new stock
                    new_stock = current_stock - details['quantity']

                    # Validate stock
                    if new_stock < 0:
                        messagebox.showerror("Insufficient Stock",
                                             f"Not enough stock for {details['name']}. Available: {current_stock}")
                        conn.close()
                        return

                    # Update stock in database
                    cursor.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stock, product_id))

                conn.commit()

                # Show receipt with change
                receipt_message = f"Purchase completed successfully!\n\n"
                receipt_message += f"Total Amount: ₱{total_amount:.2f}\n"
                receipt_message += f"Cash Tendered: ₱{tendered:.2f}\n"
                receipt_message += f"Change: ₱{change:.2f}\n\n"
                receipt_message += "Thank you for shopping at Jazmine Sari-Sari Store!"

                messagebox.showinfo("Receipt", receipt_message)

                # Clear cart after purchase
                self.cart_items = {}

                # Return to catalog after successful purchase
                self.cart_root.destroy()
                self.root = tk.Tk()
                self.root.geometry("1440x1024")
                self.root.title("Jazmine Sari-Sari Store KIOSK")
                self.root.resizable(width=False, height=False)
                self.catalog()

            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
            finally:
                conn.close()

        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")

    def back_to_menu_from_cart(self):
        """Return to the appropriate menu from shopping cart, preserving cart contents"""
        self.cart_root.destroy()
        self.new_root = tk.Tk()  # Create a temporary root to destroy in the menu method

        # Go back to the appropriate menu based on last_menu
        if self.last_menu == "biscuits":
            self.biscuits_menu()
        elif self.last_menu == "drinks":
            self.drinks_menu()
        else:  # Default to chips if last_menu is not set or is "chips"
            self.chips_menu()

    def checkout(self):
        """Redirect to shopping cart (legacy method)"""
        self.shopping_cart()

    def biscuits_menu(self):
        self.new_root.destroy()
        self.biscuits_root = tk.Tk()
        self.biscuits_root.geometry("1440x1024")
        self.biscuits_root.title("Biscuits")
        self.biscuits_root.resizable(width=False, height=False)
        image = PhotoImage(file=r"final biscuits.png")
        logo = tk.Label(self.biscuits_root, image=image)
        logo.place(x=0, y=0)

        # Rest of your existing biscuits_menu code remains the same...

        # Dictionary to store spinbox references with product IDs
        self.spinboxes = {}

        # Initialize cart_items if it doesn't exist yet
        if not hasattr(self, 'cart_items'):
            self.cart_items = {}

        # Fetch biscuits products from the database
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, stock, price FROM products WHERE section = 'BISCUITS'")
        biscuits_products = cursor.fetchall()
        conn.close()

        # Function to update shopping cart when spinbox value changes
        def update_cart(product_id, product_name, price):
            def callback(*args):
                quantity = int(self.spinboxes[product_id].get())
                if quantity > 0:
                    self.cart_items[product_id] = {
                        'name': product_name,
                        'quantity': quantity,
                        'price': price,
                        'total': quantity * price
                    }
                else:
                    if product_id in self.cart_items:
                        del self.cart_items[product_id]

                # Update cart display
                self.update_cart_display()

            return callback

        # Create spinboxes with product data (existing code)
        positions = [
            (145, 335),  # Fudgee Bar
            (358, 335),  # Fita
            (577, 335),  # Skyflakes
            (790, 335),  # Rebisco
            (145, 570),  # Oreo
            (363, 570),  # Cream-O
            (577, 570),  # Dewberry
            (793, 570),  # Choco Mallows
            (150, 793),  # Chips Delight
        ]

        # Create spinboxes for each product (existing code)
        for i, product in enumerate(biscuits_products):
            if i < len(positions):
                product_id, name, stock, price = product

                # Create StringVar to track spinbox changes
                var = tk.StringVar()
                var.set("0")

                # If item is already in cart, set spinbox to that value
                if product_id in self.cart_items:
                    var.set(str(self.cart_items[product_id]['quantity']))

                # Create spinbox with maximum value based on stock
                spinbox = Spinbox(
                    self.biscuits_root,
                    from_=0,
                    to=stock,
                    textvariable=var,
                    width=20
                )
                spinbox.place(x=positions[i][0], y=positions[i][1])

                # Store reference to spinbox and connect to update function
                self.spinboxes[product_id] = var
                var.trace("w", update_cart(product_id, name, price))

        # Create shopping cart frame (existing code)
        cart_frame = Frame(self.biscuits_root, bg="white", bd=2, relief="ridge", width=300, height=1400)
        cart_frame.place(x=1075, y=200)

        # Cart title (existing code)
        cart_title = Label(cart_frame, text="Shopping Cart", font=("Archivo Black", 16), bg="white", fg="#FF3B3B")
        cart_title.pack(pady=10)

        # Create Text widget to display cart items (existing code)
        self.cart_text = tk.Text(cart_frame, width=35, height=22, wrap="word", bg="white")
        self.cart_text.pack(padx=10, pady=5)

        # Subtotal (existing code)
        self.cart_subtotal_label = Label(cart_frame, text="Subtotal: ₱0.00", font=("Arial", 12), bg="white")
        self.cart_subtotal_label.pack(pady=5)

        # VAT (12%) (existing code)
        self.cart_vat_label = Label(cart_frame, text="VAT (12%): ₱0.00", font=("Arial", 12), bg="white")
        self.cart_vat_label.pack(pady=5)

        # Cart total (existing code)
        self.cart_total_label = Label(cart_frame, text="Total: ₱0.00", font=("Arial", 14, "bold"), bg="white")
        self.cart_total_label.pack(pady=5)

        # Update cart display with existing items
        self.update_cart_display()

        # Back button - now saves cart when going back
        back_button = Button(self.biscuits_root,
                             text="Back",
                             font=("Baloo", 40),
                             fg="#FFFFFF",
                             bg="#FF3B3B",
                             borderwidth=2,
                             command=self.save_cart_and_go_back_biscuits,
                             padx=30)

        # Review and Pay button - explicitly call shopping_cart method
        review_and_pay_button = Button(self.biscuits_root,
                                       text="Review + Pay for Order",
                                       font=("Baloo", 40),
                                       fg="#FFFFFF",
                                       bg="#FF3B3B",
                                       borderwidth=2,
                                       command=self.shopping_cart,  # This ensures it calls the shopping_cart method
                                       padx=130)

        back_button.place(x=1120, y=870)
        review_and_pay_button.place(x=100, y=870)

        self.biscuits_root.mainloop()

    def save_cart_and_go_back_biscuits(self):
        """Save cart contents and go back to catalog from biscuits menu"""
        # Cart is already saved in self.cart_items, just go back
        self.biscuits_root.destroy()
        self.root = tk.Tk()
        self.root.geometry("1440x1024")
        self.root.title("Jazmine Sari-Sari Store KIOSK")
        self.root.resizable(width=False, height=False)
        self.catalog()

    def back_to_biscuits_from_cart(self):
        """Return to biscuits menu from shopping cart, preserving cart contents"""
        self.cart_root.destroy()
        self.new_root = tk.Tk()  # Create a temporary root to destroy in biscuits_menu
        self.biscuits_menu()  # Go back to biscuits menu

    def drinks_menu(self):
        self.new_root.destroy()
        self.drinks_root = tk.Tk()
        self.drinks_root.geometry("1440x1024")
        self.drinks_root.title("Drinks")
        self.drinks_root.resizable(width=False, height=False)
        image = PhotoImage(file=r"final drinks.png")
        logo = tk.Label(self.drinks_root, image=image)
        logo.place(x=0, y=0)

        # Dictionary to store spinbox references with product IDs
        self.spinboxes = {}

        # Initialize cart_items if it doesn't exist yet
        if not hasattr(self, 'cart_items'):
            self.cart_items = {}

        # Fetch drinks products from the database
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, stock, price FROM products WHERE section = 'DRINKS'")
        drinks_products = cursor.fetchall()
        conn.close()

        # Function to update shopping cart when spinbox value changes
        def update_cart(product_id, product_name, price):
            def callback(*args):
                quantity = int(self.spinboxes[product_id].get())
                if quantity > 0:
                    self.cart_items[product_id] = {
                        'name': product_name,
                        'quantity': quantity,
                        'price': price,
                        'total': quantity * price
                    }
                else:
                    if product_id in self.cart_items:
                        del self.cart_items[product_id]

                # Update cart display
                self.update_cart_display()

            return callback

        # Create spinboxes with product data
        positions = [
            (145, 335),  # Spring Water
            (358, 335),  # Mountain Dew
            (577, 335),  # Fruit Soda
            (790, 335),  # RC Cola
            (145, 570),  # Pepsi
            (363, 570),  # Royal
            (577, 570),  # Coca-Cola
            (793, 570),  # Fanta
            (150, 793),  # Sprite
        ]

        # Create spinboxes for each product
        for i, product in enumerate(drinks_products):
            if i < len(positions):
                product_id, name, stock, price = product

                # Create StringVar to track spinbox changes
                var = tk.StringVar()
                var.set("0")

                # If item is already in cart, set spinbox to that value
                if product_id in self.cart_items:
                    var.set(str(self.cart_items[product_id]['quantity']))

                # Create spinbox with maximum value based on stock
                spinbox = Spinbox(
                    self.drinks_root,
                    from_=0,
                    to=stock,
                    textvariable=var,
                    width=20
                )
                spinbox.place(x=positions[i][0], y=positions[i][1])

                # Store reference to spinbox and connect to update function
                self.spinboxes[product_id] = var
                var.trace("w", update_cart(product_id, name, price))

        # Create shopping cart frame - made taller (height from 400 to 550)
        cart_frame = Frame(self.drinks_root, bg="white", bd=2, relief="ridge", width=300, height=1400)
        cart_frame.place(x=1075, y=200)  # Moved up from y=300 to y=200

        # Cart title
        cart_title = Label(cart_frame, text="Shopping Cart", font=("Archivo Black", 16), bg="white", fg="#FF3B3B")
        cart_title.pack(pady=10)

        # Create Text widget to display cart items - made taller (height from 15 to 22)
        self.cart_text = tk.Text(cart_frame, width=35, height=22, wrap="word", bg="white")
        self.cart_text.pack(padx=10, pady=5)

        # Subtotal
        self.cart_subtotal_label = Label(cart_frame, text="Subtotal: ₱0.00", font=("Arial", 12), bg="white")
        self.cart_subtotal_label.pack(pady=5)

        # VAT (12%)
        self.cart_vat_label = Label(cart_frame, text="VAT (12%): ₱0.00", font=("Arial", 12), bg="white")
        self.cart_vat_label.pack(pady=5)

        # Cart total
        self.cart_total_label = Label(cart_frame, text="Total: ₱0.00", font=("Arial", 14, "bold"), bg="white")
        self.cart_total_label.pack(pady=5)

        # Update cart display with existing items
        self.update_cart_display()

        # Back button - now saves cart when going back
        back_button = Button(self.drinks_root,
                             text="Back",
                             font=("Baloo", 40),
                             fg="#FFFFFF",
                             bg="#FF3B3B",
                             borderwidth=2,
                             command=self.save_cart_and_go_back_drinks,
                             padx=30)

        # Review and Pay button - now redirects to shopping cart
        review_and_pay_button = Button(self.drinks_root,
                                       text="Review + Pay for Order",
                                       font=("Baloo", 40),
                                       fg="#FFFFFF",
                                       bg="#FF3B3B",
                                       borderwidth=2,
                                       command=self.shopping_cart,
                                       padx=130)

        back_button.place(x=1120, y=870)
        review_and_pay_button.place(x=100, y=870)

        self.drinks_root.mainloop()

    def save_cart_and_go_back_drinks(self):
        """Save cart contents and go back to catalog from drinks menu"""
        # Cart is already saved in self.cart_items, just go back
        self.drinks_root.destroy()
        self.root = tk.Tk()
        self.root.geometry("1440x1024")
        self.root.title("Jazmine Sari-Sari Store KIOSK")
        self.root.resizable(width=False, height=False)
        self.catalog()

    def back_to_drinks_from_cart(self):
        """Return to drinks menu from shopping cart, preserving cart contents"""
        self.cart_root.destroy()
        self.new_root = tk.Tk()  # Create a temporary root to destroy in drinks_menu
        self.drinks_menu()  # Go back to drinks menu

    def inventory_location(self):
        self.root.destroy()
        self.inventory_root = tk.Tk()
        self.inventory_root.geometry("723x300")
        self.inventory_root.title("ADMIN LOGIN")
        self.inventory_root.resizable(width=False, height=False)
        self.inventory_root.configure(bg="white")
        image = PhotoImage(file=r"SOLO LOGO.png")
        logo = tk.Label(self.inventory_root, image=image)
        logo.place(x=0, y=0)

        self.login_username = Entry(self.inventory_root, width=20, borderwidth=2)
        self.login_username.place(x=305, y=150)
        self.login_password = Entry(self.inventory_root, width=20, borderwidth=2, show='*')  # Hide password
        self.login_password.place(x=305, y=180)

        self.admin_button = Button(self.inventory_root,
                                   text="Enter",
                                   command=self.check_login)
        self.admin_button.place(x=345, y=207)

        self.inventory_root.mainloop()

    def check_login(self):
        username = self.login_username.get()
        password = self.login_password.get()

        correct_username = "jhered"
        correct_password = "jhered143"

        if username == correct_username and password == correct_password:
            messagebox.showinfo("Login Success", "Welcome Admin!")
            self.inventory()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def inventory(self):
        """Display inventory with ability to update stock levels"""
        self.inventory_root.destroy()
        self.real_inventory = tk.Tk()
        self.real_inventory.geometry("1440x1024")
        self.real_inventory.title("Jazmine Sari-Sari Store Inventory")
        self.real_inventory.resizable(width=False, height=False)

        # Create main frame
        main_frame = Frame(self.real_inventory)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Create title label
        title_label = Label(main_frame, text="Jazmine Sari-Sari Store Inventory",
                            font=("Archivo Black", 24), fg="#FF3B3B")
        title_label.pack(pady=10)

        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Create tabs for each product section
        chips_tab = Frame(notebook)
        biscuits_tab = Frame(notebook)
        drinks_tab = Frame(notebook)

        notebook.add(chips_tab, text="CHIPS")
        notebook.add(biscuits_tab, text="BISCUITS")
        notebook.add(drinks_tab, text="DRINKS")

        # Function to create and populate a treeview for each section
        def create_section_treeview(parent_frame, section):
            # Create treeview with scrollbar
            tree_frame = Frame(parent_frame)
            tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

            tree_scroll = ttk.Scrollbar(tree_frame)
            tree_scroll.pack(side="right", fill="y")

            columns = ("ID", "Product Name", "Stock", "Price", "Actions")
            tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=tree_scroll.set)

            # Define column headings
            tree.heading("ID", text="ID")
            tree.heading("Product Name", text="Product Name")
            tree.heading("Stock", text="Stock")
            tree.heading("Price", text="Price (₱)")
            tree.heading("Actions", text="Actions")

            # Define column widths
            tree.column("ID", width=50)
            tree.column("Product Name", width=200)
            tree.column("Stock", width=100)
            tree.column("Price", width=100)
            tree.column("Actions", width=200)

            tree.pack(fill="both", expand=True)
            tree_scroll.config(command=tree.yview)

            # Populate the treeview with data from database
            conn = sqlite3.connect("inventory.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, stock, price FROM products WHERE section = ?", (section,))
            products = cursor.fetchall()
            conn.close()

            for product in products:
                tree.insert("", "end", values=(product[0], product[1], product[2], f"{product[3]:.2f}", ""))

            # Frame for controls
            controls_frame = Frame(parent_frame)
            controls_frame.pack(fill="x", padx=10, pady=5)

            # Function to update stock
            def update_stock():
                selected_item = tree.selection()
                if not selected_item:
                    messagebox.showerror("Error", "Please select a product to update")
                    return

                item_id = tree.item(selected_item[0])['values'][0]
                product_name = tree.item(selected_item[0])['values'][1]
                current_stock = tree.item(selected_item[0])['values'][2]

                # Create update dialog
                update_window = tk.Toplevel(self.real_inventory)
                update_window.title(f"Update Stock: {product_name}")
                update_window.geometry("300x150")
                update_window.resizable(False, False)

                Label(update_window, text=f"Current Stock: {current_stock}", font=("Arial", 12)).pack(pady=5)

                Label(update_window, text="New Stock Value:", font=("Arial", 12)).pack(pady=5)
                new_stock_entry = Entry(update_window, font=("Arial", 12), width=10)
                new_stock_entry.insert(0, str(current_stock))
                new_stock_entry.pack(pady=5)

                def save_stock_change():
                    try:
                        new_stock = int(new_stock_entry.get())
                        if new_stock < 0:
                            messagebox.showerror("Error", "Stock cannot be negative")
                            return

                        # Update database
                        conn = sqlite3.connect("inventory.db")
                        cursor = conn.cursor()
                        cursor.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stock, item_id))
                        conn.commit()
                        conn.close()

                        # Update treeview
                        tree.item(selected_item[0], values=(
                        item_id, product_name, new_stock, tree.item(selected_item[0])['values'][3], ""))
                        messagebox.showinfo("Success", f"Stock for {product_name} updated to {new_stock}")
                        update_window.destroy()

                    except ValueError:
                        messagebox.showerror("Error", "Please enter a valid number")

                Button(update_window, text="Save", command=save_stock_change,
                       bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)

            # Add update button
            update_button = Button(controls_frame, text="Update Selected Stock",
                                   command=update_stock, bg="#FF3B3B", fg="white",
                                   font=("Arial", 12))
            update_button.pack(side="left", padx=5)

            # Add refresh button
            def refresh_data():
                # Clear existing data
                for item in tree.get_children():
                    tree.delete(item)

                # Repopulate the treeview
                conn = sqlite3.connect("inventory.db")
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, stock, price FROM products WHERE section = ?", (section,))
                products = cursor.fetchall()
                conn.close()

                for product in products:
                    tree.insert("", "end", values=(product[0], product[1], product[2], f"{product[3]:.2f}", ""))

            refresh_button = Button(controls_frame, text="Refresh Data",
                                    command=refresh_data, bg="#2196F3", fg="white",
                                    font=("Arial", 12))
            refresh_button.pack(side="left", padx=5)

            return tree

        # Create treeviews for each section
        chips_tree = create_section_treeview(chips_tab, "CHIPS")
        biscuits_tree = create_section_treeview(biscuits_tab, "BISCUITS")
        drinks_tree = create_section_treeview(drinks_tab, "DRINKS")

        # Add back button
        back_button = Button(main_frame,
                             text="Back to Main Menu",
                             font=("Archivo Black", 16),
                             fg="#FFFFFF",
                             bg="#FF3B3B",
                             borderwidth=3,
                             command=self.back_to_main)
        back_button.pack(pady=10)

        self.real_inventory.mainloop()

    def back_to_main(self):
        self.real_inventory.destroy()
        self.root = tk.Tk()
        self.root.title("Jazmine Sari-Sari Store KIOSK")
        self.root.resizable(width=False, height=False)
        self.root.geometry("1440x1024")
        self.main_application()

    def chips_to_catalog(self):
        self.chips_root.destroy()
        # Create a new window first before calling catalog
        self.root = tk.Tk()
        self.root.geometry("1440x1024")
        self.root.title("Jazmine Sari-Sari Store KIOSK")
        self.root.resizable(width=False, height=False)
        self.catalog()

window = Window()
window.main_application()