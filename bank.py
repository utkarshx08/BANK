32154454
import random
import sys
try:
    import tkinter as tk
    from tkinter import messagebox, simpledialog, ttk, font
    TK_AVAILABLE = True
except Exception:
    TK_AVAILABLE = False
    # tkinter not available; will fall back to console mode


class ATM():
    def __init__(self, name, account_number, balance = 0):
        self.name = name
        self.account_number = account_number
        self.balance = balance
        self.history = []
         
    def account_detail(self):
        print("\n----------ACCOUNT DETAIL----------")
        print(f"Account Holder: {self.name.upper()}")
        print(f"Account Number: {self.account_number}")
        print(f"Available balance: Ruppes.{self.balance}\n")
         
    def deposit(self, amount):
        self.amount = amount
        self.balance = self.balance + self.amount
        # record transaction
        self.history.append(("Deposit", amount, self.balance))
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
            self.history.append(("Withdraw", amount, self.balance))
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
            5. Exit
        *********************
        """)
        
        while True:
            try:
                option = int(input("Enter 1, 2, 3, 4 or 5:"))
            except:
                print("Error: Enter 1, 2, 3, 4, or 5 only!\n")
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
    # Colored action buttons: separate Print Receipt and Exit
    btn_receipt = tk.Button(controls, text="🧾 Print Receipt", width=22, bg="#28a745", fg="white", activebackground="#1e7e34", relief='raised')
    btn_receipt.grid(row=4, column=0, pady=6)
    btn_exit = tk.Button(controls, text="⛔ Exit", width=22, bg="#dc3545", fg="white", activebackground="#b02a37", relief='raised')
    btn_exit.grid(row=5, column=0, pady=8)

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

    # wire buttons
    btn_detail.config(command=show_account_detail)
    btn_balance.config(command=do_check_balance)
    btn_deposit.config(command=do_deposit)
    btn_withdraw.config(command=do_withdraw)
    btn_receipt.config(command=do_print_receipt)
    btn_exit.config(command=do_exit_confirm)

    refresh_history()
    root.mainloop()


if __name__ == '__main__':
    print("*******WELCOME TO BANK OF DREAM WORLD*******")
    print("———————▶owner of dream world is suryansh tyagi◀—————————")
    print("___________________________________________________________\n")

    if TK_AVAILABLE:
        # GUI flow
        gui_root = tk.Tk()
        gui_root.withdraw()  # hide the root while we get inputs
        messagebox.showinfo("Welcome", "Welcome to Bank of Dream World")
        name = simpledialog.askstring("Account Creation", "Enter your name:")
        if not name:
            messagebox.showerror("Error", "Name is required. Exiting.")
            sys.exit()
        account_number = simpledialog.askstring("Account Creation", "Enter your account number:")
        if not account_number:
            messagebox.showerror("Error", "Account number is required. Exiting.")
            sys.exit()
        messagebox.showinfo("Success", "Congratulations! Account created successfully......")
        gui_root.destroy()

        atm = ATM(name, account_number)
        open_transaction_window(atm)
    else:
        # Console fallback
        print("----------ACCOUNT CREATION----------")
        name = input("Enter your name: ")
        account_number = input("Enter your account number: ")
        print("Congratulations! Account created successfully......\n")

        atm = ATM(name, account_number)

        while True:
            trans = input("Do you want to do any transaction?(yes/no):")
            if trans == "yes":
                atm.transaction()
            elif trans == "no":
                print("""
    -------------------------------------
   | Thanks for choosing us as your bank |
   | Visit us again!                     |
    -------------------------------------
        """)
                break
            else:
                print("Wrong command!  Enter 'yes' for yes and 'no' for NO.\n")
