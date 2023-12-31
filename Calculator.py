import tkinter as tk
from tkinter import ttk, messagebox
import math

def on_click(button_value):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, str(current) + str(button_value))

def clear_entry():
    entry.delete(0, tk.END)

def delete_last():
    current = entry.get()[:-1]
    entry.delete(0, tk.END)
    entry.insert(tk.END, current)

def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

def calculate_log():
    try:
        value = float(entry.get())
        result = math.log10(value)
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except ValueError:
        messagebox.showerror("Error", "Invalid input for logarithm")

# Create the main window
root = tk.Tk()
root.title("Dynamic Calculator")

# Entry widget for displaying the input and output
entry = tk.Entry(root, width=15, borderwidth=5, font=('Arial', 14))
entry.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky='nsew')

# Define buttons with improved styling using ttk
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '%', '+'
]

# Add buttons to the grid with dynamic sizing
row_val = 1
col_val = 0

for button in buttons:
    ttk.Button(
        root,
        text=button,
        style='TButton',
        command=lambda b=button: on_click(b)
    ).grid(row=row_val, column=col_val, sticky='nsew')
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

# Clear, delete, equal, and log buttons with dynamic sizing
ttk.Button(
    root,
    text="C",
    style='TButton',
    command=clear_entry
).grid(row=5, column=0, columnspan=1)

ttk.Button(
    root,
    text="⌫",  # Delete symbol
    style='TButton',
    command=delete_last
).grid(row=5, column=2, columnspan=1)

ttk.Button(
    root,
    text="=",
    style='TButton',
    command=calculate
).grid(row=5, column=3)

# Combine () buttons into a single frame with a fixed width
frame_brackets = ttk.Frame(root, width=10)  # Adjust width as needed
frame_brackets.grid(row=5, column=1,columnspan=2, sticky='nsew')

ttk.Button(
    frame_brackets,
    text="(",
    style='TButton',
    command=lambda: on_click("(")
).pack(side='left')

ttk.Button(
    frame_brackets,
    text=")",
    style='TButton',
    command=lambda: on_click(")")
).pack(side='right')

ttk.Button(
    root,
    text="log",
    style='TButton',
    command=calculate_log
).grid(row=3, column=3,columnspan=1)

# Brackets buttons
ttk.Button(
    root,
    text=".",
    style='TButton',
    command=lambda: on_click(".")
).grid(row=4, column=0, sticky='nsew')

ttk.Button(
    root,
    text="0",
    style='TButton',
    command=lambda: on_click("0")
).grid(row=4, column=1, sticky='nsew')

# Configure row and column weights for resizing
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

# Style configuration for ttk buttons
style = ttk.Style()
style.configure('TButton', padding=5, font=('Arial', 12), background='#4CAF50', foreground='Red')

# Adjust font size based on screen resolution
screen_width = root.winfo_screenwidth()
font_size = int(screen_width / 75)
entry.config(font=('Arial', font_size))

# Bind an event to adjust font size on window resize
def on_resize(event):
    new_font_size = int(event.width / 75)
    entry.config(font=('Arial', new_font_size))

root.bind('<Configure>', on_resize)

# Run the main loop
root.mainloop()
