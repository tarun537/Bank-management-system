import sqlite3
import hashlib
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk  # Import PIL for handling images

class BankApp:
    def __init__(self, root):
        self.conn = sqlite3.connect("bank_accounts.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        self.root = root
        self.root.title("Bank Application")
        self.root.geometry("1024x768")

        self.bg_photo = self.load_background_image()

        self.show_login_screen()

    def create_table(self):
        """Create the table to store user accounts."""
        self.cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY,
                username TEXT,
                password TEXT,
                balance REAL
            )
        ''')
        self.conn.commit()

    def load_background_image(self):
        """Load and return the background image."""
        bg_image = Image.open("C:/Users/Lenovo/Desktop/pngtree-illustration-of-3d-personal-bank-account-and-credit-card-with-money-image_3653857.jpg")  # Update the path if needed
        bg_image = bg_image.resize((1024, 768), Image.Resampling.LANCZOS)  # Resize to fit the window size

        bg_photo = ImageTk.PhotoImage(bg_image)
        return bg_photo

    def add_background(self, window):
        """Add background image to a given window."""
        canvas = tk.Canvas(window, width=1024, height=768)
        canvas.pack(fill="both", expand=True)  # Make the canvas fill the window
        canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)
        return canvas

    def create_account(self, username, password):
        """Create a new account."""
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("INSERT INTO accounts (username, password, balance) VALUES (?, ?, ?)",
                            (username, hashed_password, 0.0))
        self.conn.commit()

    def login(self, username, password):
        """Verify the user's login credentials."""
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("SELECT * FROM accounts WHERE username=? AND password=?", (username, hashed_password))
        account = self.cursor.fetchone()
        return account

    def check_balance(self, username):
        """Check the balance of the logged-in user."""
        self.cursor.execute("SELECT balance FROM accounts WHERE username=?", (username,))
        balance = self.cursor.fetchone()
        return balance[0] if balance else None

    def deposit(self, username, amount):
        """Deposit money into the user's account."""
        current_balance = self.check_balance(username)
        if current_balance is not None:
            new_balance = current_balance + amount
            self.cursor.execute("UPDATE accounts SET balance=? WHERE username=?", (new_balance, username))
            self.conn.commit()
            return new_balance
        return None

    def withdraw(self, username, amount):
        """Withdraw money from the user's account."""
        current_balance = self.check_balance(username)
        if current_balance is not None and amount <= current_balance:
            new_balance = current_balance - amount
            self.cursor.execute("UPDATE accounts SET balance=? WHERE username=?", (new_balance, username))
            self.conn.commit()
            return new_balance
        return None

    def transfer(self, sender_username, receiver_username, amount):
        """Transfer money from one user to another."""
        sender_balance = self.check_balance(sender_username)
        receiver_balance = self.check_balance(receiver_username)
        if sender_balance is not None and receiver_balance is not None and amount <= sender_balance:
            new_sender_balance = sender_balance - amount
            new_receiver_balance = receiver_balance + amount
            self.cursor.execute("UPDATE accounts SET balance=? WHERE username=?", (new_sender_balance, sender_username))
            self.cursor.execute("UPDATE accounts SET balance=? WHERE username=?", (new_receiver_balance, receiver_username))
            self.conn.commit()
            return new_sender_balance, new_receiver_balance
        return None, None

    def show_login_screen(self):
        """Show the login screen with a background image."""
        self.clear_screen()

        self.add_background(self.root)

        self.username_label = tk.Label(self.root, text="Username:", font=("Helvetica", 14))
        self.username_label.place(relx=0.5, rely=0.3, anchor="center")  # Center the label

        self.username_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.username_entry.place(relx=0.5, rely=0.35, anchor="center")  # Center the entry box

        self.password_label = tk.Label(self.root, text="Password:", font=("Helvetica", 14))
        self.password_label.place(relx=0.5, rely=0.45, anchor="center")  # Center the label

        self.password_entry = tk.Entry(self.root, show="*", font=("Helvetica", 14))
        self.password_entry.place(relx=0.5, rely=0.5, anchor="center")  # Center the entry box

        self.login_button = tk.Button(self.root, text="Login", command=self.login_user, font=("Helvetica", 14), width=20, height=2)
        self.login_button.place(relx=0.5, rely=0.6, anchor="center")  # Center the button with a gap between password entry

        self.create_account_button = tk.Button(self.root, text="Create Account", command=self.show_create_account_screen, font=("Helvetica", 14), width=20, height=2)
        self.create_account_button.place(relx=0.5, rely=0.7, anchor="center")  # Center the button below login

    def login_user(self):
        """Handle user login."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        account = self.login(username, password)
        if account:
            self.show_account_screen(username)
        else:
            messagebox.showerror("Login Error", "Invalid username or password")

    def show_create_account_screen(self):
        """Show the screen for account creation."""
        self.clear_screen()

        self.add_background(self.root)

        self.create_username_label = tk.Label(self.root, text="Username:", font=("Helvetica", 14))
        self.create_username_label.place(relx=0.5, rely=0.3, anchor="center")  # Center the label

        self.create_username_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.create_username_entry.place(relx=0.5, rely=0.35, anchor="center")  # Center the entry box

        self.create_password_label = tk.Label(self.root, text="Password:", font=("Helvetica", 14))
        self.create_password_label.place(relx=0.5, rely=0.4, anchor="center")  # Center the label

        self.create_password_entry = tk.Entry(self.root, show="*", font=("Helvetica", 14))
        self.create_password_entry.place(relx=0.5, rely=0.45, anchor="center")  # Center the entry box

        self.create_account_button = tk.Button(self.root, text="Create Account", command=self.create_account_user, font=("Helvetica", 14), width=20, height=2)
        self.create_account_button.place(relx=0.5, rely=0.5, anchor="center")  # Center the button

        self.back_button = tk.Button(self.root, text="Back", command=self.show_login_screen, font=("Helvetica", 14), width=20, height=2)
        self.back_button.place(relx=0.5, rely=0.6, anchor="center")  # Center the button below create account

    def create_account_user(self):
        """Handle account creation."""
        username = self.create_username_entry.get()
        password = self.create_password_entry.get()

        if username and password:
            self.create_account(username, password)
            messagebox.showinfo("Account Created", "Account successfully created!")
            self.show_login_screen()
        else:
            messagebox.showerror("Error", "Please provide a valid username and password.")

    def show_account_screen(self, username):
        """Show the main account screen with balance and options."""
        self.clear_screen()

        self.add_background(self.root)

        self.welcome_label = tk.Label(self.root, text=f"Welcome, {username}!", font=("Helvetica", 16, "bold"))
        self.welcome_label.place(relx=0.5, rely=0.2, anchor="center")  # Center the label

        self.balance_label = tk.Label(self.root, text=f"Balance: ₹{self.check_balance(username):.2f}", font=("Helvetica", 14))
        self.balance_label.place(relx=0.5, rely=0.3, anchor="center")  # Center the label below welcome message

        self.deposit_button = tk.Button(self.root, text="Deposit", command=lambda: self.deposit_action(username), font=("Helvetica", 14), width=20, height=2)
        self.deposit_button.place(relx=0.5, rely=0.4, anchor="center")  # Center the button

        self.withdraw_button = tk.Button(self.root, text="Withdraw", command=lambda: self.withdraw_action(username), font=("Helvetica", 14), width=20, height=2)
        self.withdraw_button.place(relx=0.5, rely=0.5, anchor="center")  # Center the button

        self.transfer_button = tk.Button(self.root, text="Transfer", command=lambda: self.transfer_action(username), font=("Helvetica", 14), width=20, height=2)
        self.transfer_button.place(relx=0.5, rely=0.6, anchor="center")  # Center the button

        self.logout_button = tk.Button(self.root, text="Logout", command=self.show_login_screen, font=("Helvetica", 14), width=20, height=2)
        self.logout_button.place(relx=0.5, rely=0.7, anchor="center")  # Center the button

    def deposit_action(self, username):
        """Handle deposit."""
        amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:")
        if amount and amount > 0:
            new_balance = self.deposit(username, amount)
            messagebox.showinfo("Deposit", f"Deposited ₹{amount:.2f}. New balance: ₹{new_balance:.2f}")
            self.show_account_screen(username)
        else:
            messagebox.showerror("Error", "Invalid deposit amount.")

    def withdraw_action(self, username):
        """Handle withdrawal."""
        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
        if amount and amount > 0:
            new_balance = self.withdraw(username, amount)
            if new_balance is not None:
                messagebox.showinfo("Withdraw", f"Withdrew ₹{amount:.2f}. New balance: ₹{new_balance:.2f}")
                self.show_account_screen(username)
            else:
                messagebox.showerror("Error", "Insufficient balance or invalid amount.")
        else:
            messagebox.showerror("Error", "Invalid withdrawal amount.")

    def transfer_action(self, username):
        """Handle money transfer between accounts."""
        receiver = simpledialog.askstring("Transfer", "Enter the recipient's username:")
        amount = simpledialog.askfloat("Transfer", "Enter amount to transfer:")
        if receiver and amount and amount > 0:
            new_sender_balance, new_receiver_balance = self.transfer(username, receiver, amount)
            if new_sender_balance is not None:
                messagebox.showinfo("Transfer", f"Transferred ₹{amount:.2f} to {receiver}.")
                self.show_account_screen(username)
            else:
                messagebox.showerror("Error", "Transfer failed. Check the recipient and balance.")
        else:
            messagebox.showerror("Error", "Invalid transfer details.")

    def clear_screen(self):
        """Clear the current widgets on the screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        """Run the Tkinter main loop."""
        self.root.mainloop()

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    app.run()

