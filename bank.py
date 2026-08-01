32154454
import random
import sys
import json
import csv
import os
from datetime import datetime

try:
    import tkinter as tk
    from tkinter import messagebox, simpledialog, ttk, font
    TK_AVAILABLE = True
except Exception:
    TK_AVAILABLE = False
    # tkinter not available; will fall back to console mode

USERS_FILE = "users.json"
accounts = {}
current_theme = "Light"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users_dict):
    with open(USERS_FILE, 'w') as f:
        json.dump(users_dict, f, indent=4)

def update_account_state(atm_obj):
    accounts[atm_obj.account_number] = {
        "name": atm_obj.name,
        "pin": atm_obj.pin,
        "balance": atm_obj.balance,
        "history": atm_obj.history
    }
    save_users(accounts)

class ATM():
    def __init__(self, name, account_number, balance = 0, pin = "", history = None):
        self.name = name
        self.account_number = account_number
        self.balance = balance
        self.pin = pin
        self.history = history if history is not None else []
         
    def account_detail(self):
        print("\n----------ACCOUNT DETAIL----------")
        print(f"Account Holder: {self.name.upper()}")
        print(f"Account Number: {self.account_number}")
        print(f"Available balance: Ruppes.{self.balance}\n")
         
    def deposit(self, amount):
        self.amount = amount
        self.balance = self.balance + self.amount
        # record transaction
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append((now, "Deposit", amount, self.balance))
        update_account_state(self)
        print("Current account balance: Ruppes.", self.balance)
        print()
 
    def withdraw(self, amount):
        self.amount = amount
        if self.amount > self.balance:
            print("Insufficient fund!")
            print(f"Your balance is Ruppes.{self.balance} only.")
            print("Try with lesser amount than balance.")
            print()
        else:
            self.balance = self.balance - self.amount
            # record transaction
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.history.append((now, "Withdraw", amount, self.balance))
            update_account_state(self)
            print(f"Nu.{amount} withdrawal successful!")
            print("Current account balance: Ruppes.", self.balance)
            print()
 
    def check_balance(self):
        print("Available balance: ", self.balance)
        print()
 
    def transaction(self):
        print("""
            TRANSACTION 
        *********************
            Menu:
            1. Account Detail
            2. Check Balance
            3. Deposit
            4. Withdraw
            5. Export Statement
            6. Exit
        *********************
        """)
        
        while True:
            try:
                option = int(input("Enter 1, 2, 3, 4, 5 or 6:"))
            except:
                print("Error: Enter 1, 2, 3, 4, 5 or 6 only!\n")
                continue
            else:
                if option == 1:
                    self.account_detail()
                elif option == 2:
                    self.check_balance()
                elif option == 3:
                    amount = int(input("How much you want to deposit(Ruppes.):"))
                    self.deposit(amount)
                elif option == 4:
                    amount = int(input("How much you want to withdraw(Ruppes.):"))
                    self.withdraw(amount)
                elif option == 5:
                    filename = f"Statement_{self.account_number}.csv"
                    try:
                        with open(filename, 'w', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(["Date", "Time", "Transaction Type", "Amount", "Balance"])
                            for h in self.history:
                                if len(h) == 4:
                                    dt, typ, amt, bal = h
                                    date_part, time_part = dt.split(' ', 1)
                                    writer.writerow([date_part, time_part, typ, amt, bal])
                                else:
                                    typ, amt, bal = h
                                    writer.writerow(["", "", typ, amt, bal])
                        print(f"Statement exported successfully to {filename}\n")
                    except Exception as e:
                        print(f"Could not export statement: {e}\n")
                elif option == 6:
                    print(f"""
                printing receipt..............
          ******************************************
              Transaction is now complete.                         
              Transaction number: {random.randint(10000, 1000000)} 
              Account holder: {self.name.upper()}                  
              Account number: {self.account_number}                
              Available balance: Nu.{self.balance}                    
 
              Thanks for choosing us as your bank                  
          ******************************************
          """)
                    sys.exit()
                 
 
def open_transaction_window(atm_obj):
    root = tk.Tk()
    root.title("Bank of Dream World - ATM")
    root.geometry("520x420")
    root.configure(bg="#eef6ff")

    # Use ttk styles for a modern look
    style = ttk.Style(root)
    try:
        style.theme_use('clam')
    except Exception:
        pass
    style.configure('TButton', font=('Helvetica', 10), padding=6)
    style.configure('Header.TLabel', font=('Helvetica', 14, 'bold'), background="#eef6ff")
    style.configure('Sub.TLabel', font=('Helvetica', 10), background="#eef6ff")

    header = ttk.Frame(root)
    header.pack(fill='x', padx=12, pady=10)
    header_lbl = ttk.Label(header, text="Bank of Dream World", style='Header.TLabel')
    header_lbl.pack(side='left')
    user_lbl = ttk.Label(header, text=f"  Welcome, {atm_obj.name.title()} (Acc#: {atm_obj.account_number})", style='Sub.TLabel')
    user_lbl.pack(side='left', padx=8)

    main = ttk.Frame(root)
    main.pack(fill='both', expand=True, padx=12, pady=6)

    # Left: controls
    controls = ttk.Frame(main)
    controls.grid(row=0, column=0, sticky='n', padx=(0,8))

    btn_detail = ttk.Button(controls, text="📄 Account Detail", width=22)
    btn_detail.grid(row=0, column=0, pady=6)
    btn_balance = ttk.Button(controls, text="💰 Check Balance", width=22)
    btn_balance.grid(row=1, column=0, pady=6)
    btn_deposit = ttk.Button(controls, text="➕ Deposit", width=22)
    btn_deposit.grid(row=2, column=0, pady=6)
    btn_withdraw = ttk.Button(controls, text="➖ Withdraw", width=22)
    btn_withdraw.grid(row=3, column=0, pady=6)
    btn_export = ttk.Button(controls, text="📁 Export Statement", width=22)
    btn_export.grid(row=4, column=0, pady=6)
    btn_theme = ttk.Button(controls, text="🌗 Toggle Theme", width=22)
    btn_theme.grid(row=5, column=0, pady=6)
    # Colored action buttons: separate Print Receipt and Exit
    btn_receipt = tk.Button(controls, text="🧾 Print Receipt", width=22, bg="#28a745", fg="white", activebackground="#1e7e34", relief='raised')
    btn_receipt.grid(row=6, column=0, pady=6)
    btn_exit = tk.Button(controls, text="⛔ Exit", width=22, bg="#dc3545", fg="white", activebackground="#b02a37", relief='raised')
    btn_exit.grid(row=7, column=0, pady=8)

    # Right: transaction history
    history_frame = ttk.Frame(main)
    history_frame.grid(row=0, column=1, sticky='nsew')
    main.columnconfigure(1, weight=1)
    history_lbl = ttk.Label(history_frame, text="Transaction History", style='Sub.TLabel')
    history_lbl.pack(anchor='w')
    history_list = tk.Listbox(history_frame, height=12, bd=0, highlightthickness=0, bg="#fffaf0")
    history_list.pack(fill='both', expand=True, pady=6)

    status = ttk.Label(root, text=f"Balance: Ruppes. {atm_obj.balance}", relief='sunken', anchor='w')
    status.pack(side='bottom', fill='x')

    # populate history
    def refresh_history():
        history_list.delete(0, tk.END)
        for t in atm_obj.history[-50:]:
            if len(t) == 4:
                dt, typ, amt, bal = t
                sign = '+' if typ.lower().startswith('d') else '-'
                history_list.insert(tk.END, f"[{dt}] {typ}: {sign}Ruppes.{amt} Bal:{bal}")
            else:
                typ, amt, bal = t
                sign = '+' if typ.lower().startswith('d') else '-'
                history_list.insert(tk.END, f"{typ}: {sign}Ruppes.{amt}   Bal: Ruppes.{bal}")
        status.config(text=f"Balance: Ruppes. {atm_obj.balance}")

    def show_account_detail():
        detail = f"Account Holder: {atm_obj.name.title()}\nAccount Number: {atm_obj.account_number}\nAvailable balance: Ruppes.{atm_obj.balance}"
        messagebox.showinfo("Account Detail", detail)

    def do_check_balance():
        messagebox.showinfo("Balance", f"Available balance: Ruppes.{atm_obj.balance}")

    def do_deposit():
        amt = simpledialog.askinteger("Deposit", "How much you want to deposit (Ruppes.):", minvalue=0)
        if amt is None:
            return
        atm_obj.deposit(amt)
        refresh_history()
        messagebox.showinfo("Deposit", f"Deposited Ruppes.{amt}. Current balance: Ruppes.{atm_obj.balance}")

    def do_withdraw():
        amt = simpledialog.askinteger("Withdraw", "How much you want to withdraw (Ruppes.):", minvalue=0)
        if amt is None:
            return
        if amt > atm_obj.balance:
            messagebox.showwarning("Insufficient Funds", f"Insufficient fund! Your balance is Ruppes.{atm_obj.balance} only.")
            return
        atm_obj.withdraw(amt)
        refresh_history()
        messagebox.showinfo("Withdraw", f"Ruppes.{amt} withdrawal successful! Current balance: Ruppes.{atm_obj.balance}")

    def do_print_receipt():
        receipt = f"Transaction number: {random.randint(10000, 1000000)}\nAccount holder: {atm_obj.name.title()}\nAccount number: {atm_obj.account_number}\nAvailable balance: Ruppes.{atm_obj.balance}\n\nThanks for choosing us as your bank"
        messagebox.showinfo("Receipt", receipt)

    def do_exit_confirm():
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            root.destroy()

    def do_export_statement():
        filename = f"Statement_{atm_obj.account_number}.csv"
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Time", "Transaction Type", "Amount", "Balance"])
                for h in atm_obj.history:
                    if len(h) == 4:
                        dt, typ, amt, bal = h
                        date_part, time_part = dt.split(' ', 1)
                        writer.writerow([date_part, time_part, typ, amt, bal])
                    else:
                        typ, amt, bal = h
                        writer.writerow(["", "", typ, amt, bal])
            messagebox.showinfo("Export", f"Statement exported successfully to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not export statement:\n{e}")

    def apply_theme():
        bg_color = "#2d2d2d" if current_theme == "Dark" else "#eef6ff"
        fg_color = "#ffffff" if current_theme == "Dark" else "#000000"
        list_bg = "#1e1e1e" if current_theme == "Dark" else "#fffaf0"
        btn_bg = "#404040" if current_theme == "Dark" else "#e0e0e0"
        btn_fg = "#ffffff" if current_theme == "Dark" else "#000000"
        
        root.configure(bg=bg_color)
        
        style = ttk.Style(root)
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color)
        style.configure('Header.TLabel', background=bg_color, foreground=fg_color)
        style.configure('Sub.TLabel', background=bg_color, foreground=fg_color)
        style.configure('TButton', background=btn_bg, foreground=btn_fg)
        
        def update_tk_widgets(w):
            if isinstance(w, tk.Listbox):
                w.configure(bg=list_bg, fg=fg_color)
            elif isinstance(w, tk.Label):
                w.configure(bg=bg_color, fg=fg_color)
            for child in w.winfo_children():
                update_tk_widgets(child)
                
        update_tk_widgets(root)

    def do_toggle_theme():
        global current_theme
        current_theme = "Dark" if current_theme == "Light" else "Light"
        apply_theme()

    # wire buttons
    btn_detail.config(command=show_account_detail)
    btn_balance.config(command=do_check_balance)
    btn_deposit.config(command=do_deposit)
    btn_withdraw.config(command=do_withdraw)
    btn_export.config(command=do_export_statement)
    btn_theme.config(command=do_toggle_theme)
    btn_receipt.config(command=do_print_receipt)
    btn_exit.config(command=do_exit_confirm)

    refresh_history()
    apply_theme()
    root.mainloop()


if __name__ == '__main__':
    print("*******WELCOME TO BANK OF DREAM WORLD*******")
    print("———————▶owner of dream world is suryansh tyagi◀—————————")
    print("___________________________________________________________\n")

    accounts = load_users()

    if TK_AVAILABLE:
        # GUI flow
        login_root = tk.Tk()
        login_root.title("Bank of Dream World - Login")
        login_root.geometry("300x200")
        login_root.configure(bg="#eef6ff")

        def do_register():
            name = simpledialog.askstring("Account Creation", "Enter your name:", parent=login_root)
            if not name: return
            account_number = simpledialog.askstring("Account Creation", "Enter your account number:", parent=login_root)
            if not account_number: return
            if account_number in accounts:
                messagebox.showerror("Error", "Account already exists!", parent=login_root)
                return
            pin = simpledialog.askstring("Account Creation", "Set your PIN:", show="*", parent=login_root)
            if not pin: return
            
            accounts[account_number] = {"name": name, "pin": pin, "balance": 0, "history": []}
            save_users(accounts)
            messagebox.showinfo("Success", "Account created successfully. You can now log in.", parent=login_root)

        def do_login():
            account_number = simpledialog.askstring("Login", "Enter your account number:", parent=login_root)
            if not account_number: return
            if account_number not in accounts:
                messagebox.showerror("Error", "Account not found!", parent=login_root)
                return
            pin = simpledialog.askstring("Login", "Enter your PIN:", show="*", parent=login_root)
            if pin != accounts[account_number]["pin"]:
                messagebox.showerror("Error", "Incorrect PIN!", parent=login_root)
                return
            
            # Login successful
            messagebox.showinfo("Success", "Login successful!", parent=login_root)
            user_data = accounts[account_number]
            atm = ATM(user_data["name"], account_number, user_data.get("balance", 0), user_data["pin"], user_data.get("history", []))
            login_root.destroy()
            open_transaction_window(atm)

        tk.Label(login_root, text="Bank of Dream World", font=('Helvetica', 14, 'bold'), bg="#eef6ff").pack(pady=20)
        tk.Button(login_root, text="Create Account", command=do_register, width=15).pack(pady=5)
        tk.Button(login_root, text="Log In", command=do_login, width=15).pack(pady=5)
        tk.Button(login_root, text="Exit", command=login_root.destroy, width=15).pack(pady=5)

        login_root.mainloop()

    else:
        # Console fallback
        while True:
            print("\n1. Create Account")
            print("2. Log In")
            print("3. Exit")
            choice = input("Choose an option: ")

            if choice == '1':
                print("----------ACCOUNT CREATION----------")
                name = input("Enter your name: ")
                account_number = input("Enter your account number: ")
                if account_number in accounts:
                    print("Account already exists!\n")
                    continue
                pin = input("Set your PIN: ")
                accounts[account_number] = {"name": name, "pin": pin, "balance": 0, "history": []}
                save_users(accounts)
                print("Congratulations! Account created successfully......\n")

            elif choice == '2':
                print("----------LOG IN----------")
                account_number = input("Enter your account number: ")
                if account_number not in accounts:
                    print("Account not found!\n")
                    continue
                pin = input("Enter your PIN: ")
                if accounts[account_number]["pin"] != pin:
                    print("Incorrect PIN!\n")
                    continue
                
                print("Login successful!\n")
                user_data = accounts[account_number]
                atm = ATM(user_data["name"], account_number, user_data.get("balance", 0), user_data["pin"], user_data.get("history", []))
                while True:
                    trans = input("Do you want to do any transaction?(yes/no):")
                    if trans.lower() == "yes":
                        atm.transaction()
                    elif trans.lower() == "no":
                        print("Logging out...")
                        break
                    else:
                        print("Wrong command!  Enter 'yes' for yes and 'no' for NO.\n")
            
            elif choice == '3':
                print("""
    -------------------------------------
   | Thanks for choosing us as your bank |
   | Visit us again!                     |
    -------------------------------------
        """)
                break
            else:
                print("Invalid choice, please try again.\n")
