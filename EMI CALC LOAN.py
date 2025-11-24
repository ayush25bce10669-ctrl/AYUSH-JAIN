import tkinter as tk
from tkinter import ttk, messagebox

def calculate_emi(principal, annual_rate, tenure_months):
    r = annual_rate / 12 / 100
    n = tenure_months

    if r == 0:
        emi = principal / n
    else:
        emi = principal * r * (1+r)**n / ((1+r)**n - 1)

    total_payment = emi * n
    total_interest = total_payment - principal

    return emi, total_interest, total_payment

def show_schedule(principal, annual_rate, tenure_months):
    r = annual_rate / 12 / 100
    n = tenure_months
    emi, _, _ = calculate_emi(principal, annual_rate, tenure_months)

    win = tk.Toplevel(root)
    win.title("Amortization Schedule")
    win.geometry("650x500")

    frame = ttk.Frame(win)
    frame.pack(fill="both", expand=True)

    columns = ("Month", "Opening", "EMI", "Interest", "Principal", "Closing")
    tree = ttk.Treeview(frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(expand=True, fill="both")

    balance = principal

    for month in range(1, n+1):
        interest = balance * r
        principal_component = emi - interest
        closing = balance - principal_component

        tree.insert("", "end",
                    values=(
                        month,
                        f"{balance:.2f}",
                        f"{emi:.2f}",
                        f"{interest:.2f}",
                        f"{principal_component:.2f}",
                        f"{closing:.2f}",
                    ))
        balance = closing

def calculate():
    try:
        P = float(entry_principal.get())
        rate = float(entry_rate.get())
        years = float(entry_years.get())
    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers.")
        return

    months = int(years * 12)
    emi, interest, total = calculate_emi(P, rate, months)

    label_emi_value.config(text=f"₹ {emi:,.2f}")
    label_interest_value.config(text=f"₹ {interest:,.2f}")
    label_total_value.config(text=f"₹ {total:,.2f}")

    btn_schedule.config(command=lambda: show_schedule(P, rate, months))

root = tk.Tk()
root.title("EMI Calculator")
root.geometry("400x400")
root.resizable(False, False)

title = tk.Label(root, text="EMI Calculator", font=("Arial", 18, "bold"))
title.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Loan Amount (₹):", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
entry_principal = tk.Entry(frame, font=("Arial", 12))
entry_principal.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Interest Rate (%):", font=("Arial", 12)).grid(row=1, column=0, sticky="w")
entry_rate = tk.Entry(frame, font=("Arial", 12))
entry_rate.grid(row=1, column=1, pady=5)

tk.Label(frame, text="Tenure (Years):", font=("Arial", 12)).grid(row=2, column=0, sticky="w")
entry_years = tk.Entry(frame, font=("Arial", 12))
entry_years.grid(row=2, column=1, pady=5)

btn = tk.Button(root, text="Calculate EMI", font=("Arial", 12, "bold"),
                command=calculate, bg="#0080ff", fg="white")
btn.pack(pady=10)

result_frame = tk.Frame(root)
result_frame.pack()

tk.Label(result_frame, text="Monthly EMI:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
label_emi_value = tk.Label(result_frame, text="₹ 0.00", font=("Arial", 12))
label_emi_value.grid(row=0, column=1)

tk.Label(result_frame, text="Total Interest:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w")
label_interest_value = tk.Label(result_frame, text="₹ 0.00", font=("Arial", 12))
label_interest_value.grid(row=1, column=1)

tk.Label(result_frame, text="Total Payment:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="w")
label_total_value = tk.Label(result_frame, text="₹ 0.00", font=("Arial", 12))
label_total_value.grid(row=2, column=1)

btn_schedule = tk.Button(root, text="Show Amortization Schedule", font=("Arial", 12),
                         bg="#00aa44", fg="white")
btn_schedule.pack(pady=15)

root.mainloop()
