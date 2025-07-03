import tkinter as tk

def click(event):
    text = event.widget.cget("text")
    if text == "=":
        try:
            result = str(eval(screen.get()))
            screen_var.set(result)
        except Exception as e:
            screen_var.set("Error")
    elif text == "C":
        screen_var.set("")
    else:
        screen_var.set(screen_var.get() + text)

root = tk.Tk()
root.title("EasyCalc")

screen_var = tk.StringVar()
screen = tk.Entry(root, textvar=screen_var, font="lucida 20 bold")
screen.grid(row=0, column=0, columnspan=4, ipadx=8, pady=10, padx=10, sticky="nsew")

button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, columnspan=4, sticky="nsew")

buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    'C', '0', '=', '+'
]

row_val = 0
col_val = 0
for button in buttons:
    btn = tk.Button(button_frame, text=button, font="lucida 15 bold")
    btn.grid(row=row_val, column=col_val, sticky="nsew")
    btn.bind("<Button-1>", click)
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

for i in range(4):
    button_frame.grid_columnconfigure(i, weight=1)
    button_frame.grid_rowconfigure(i, weight=1)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

exit_button = tk.Button(root, text="Exit", font="lucida 15 bold", command=root.quit)
exit_button.grid(row=2, column=0, columnspan=4, sticky="nsew")

root.grid_rowconfigure(2, weight=1)
root.mainloop()