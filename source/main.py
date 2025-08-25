import customtkinter as ctk
import re

LICENSE_TEXT = """\
                      GNU GENERAL PUBLIC LICENSE
                         Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

 The GNU General Public License is a free, copyleft license for
 software and other kinds of works.

 The licenses for most software and other practical works are designed to
 take away your freedom to share and change the works. By contrast,
 the GNU General Public License is intended to guarantee your freedom to
 share and change all versions of a program--to make sure it remains free
 software for all its users. We, the Free Software Foundation, use the
 GNU General Public License for most of our software; it applies also to
 any other work released this way by its authors. You can apply it to
 your programs, too.

 When we speak of free software, we are referring to freedom, not price.
 ...
"""

class CalculatorLogic:
    def __init__(self):
        self.reset()

    def reset(self):
        self.expression = "0"

    def set_expression(self, expr: str):
        self.expression = expr

    def get_expression(self) -> str:
        return self.expression

    def add_digit(self, digit: str):
        if self.expression in ("0", "Error"):
            self.expression = digit
        else:
            self.expression += digit

    def add_operator(self, operator: str):
        if self.expression == "Error":
            return

        op = ""
        if operator == "÷":
            op = "/"
        elif operator == "×":
            op = "*"
        else:
            op = operator

        if self.expression.endswith(("+", "-", "*", "/", "%")):
            self.expression = self.expression[:-1] + op
        else:
            self.expression += op

    def add_decimal(self):
        if self.expression == "Error":
            return
        
        parts = re.split(r'[-+*/%]', self.expression)
        if "." not in parts[-1]:
            self.expression += "."

    def toggle_sign(self):
        if self.expression == "Error":
            return
        if self.expression.startswith("-"):
            self.expression = self.expression[1:]
        else:
            self.expression = "-" + self.expression

    def add_parentheses(self):
        if self.expression == "Error":
            return
        if self.expression == "0":
            self.expression = "()"
        elif self.expression and (self.expression[-1].isdigit() or self.expression[-1] == ")"):
            self.expression += "*()"
        else:
            self.expression += "()"

    def clear(self):
        self.reset()

    def calculate(self):
        try:
            expr = self.expression.replace("×", "*").replace("÷", "/").replace("%", "/100*")
            if not re.match(r'^[+\-*/()%.\d\s]+$', expr):
                raise ValueError("Invalid characters")
            result = eval(expr, {"__builtins__": None}, {})
            if isinstance(result, float) and result == int(result):
                self.expression = str(int(result))
            else:
                self.expression = str(result)
                
        except (ZeroDivisionError, ValueError, TypeError):
            self.expression = "Error"
        except Exception:
            self.expression = "Error"

class Display:
    def __init__(self, master, initial="0"):
        self.var = ctk.StringVar(value=initial)
        self.entry = ctk.CTkEntry(
            master,
            textvariable=self.var,
            font=("Roboto", 32),
            justify="right",
            border_width=0,
            fg_color="#1E1E1E",
            text_color="#FFFFFF",
            corner_radius=8
        )

    def pack(self, **kwargs):
        self.entry.pack(**kwargs)

    def set(self, text: str):
        self.var.set(text)

    def get(self) -> str:
        return self.var.get()

class ButtonGrid:
    def __init__(self, master, command_mapper):
        self.master = master
        self.frame = ctk.CTkFrame(master, fg_color="transparent")
        self.command_mapper = command_mapper
        self.buttons = []
        self._create_buttons()
        self._layout_buttons()

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def _create_buttons(self):
        button_config = {
            "font": ("Roboto", 20),
            "width": 70,
            "height": 70,
            "corner_radius": 35,
            "border_width": 0,
            "text_color": "#FFFFFF"
        }
        
        specs = [
            ("C", "#FF5252", "#FF8A80"), ("()", "#2E2E2E", "#3E3E3E"), ("%", "#2E2E2E", "#3E3E3E"), ("÷", "#FF9800", "#FFB74D"),
            ("7", "#2E2E2E", "#3E3E3E"), ("8", "#2E2E2E", "#3E3E3E"), ("9", "#2E2E2E", "#3E3E3E"), ("×", "#FF9800", "#FFB74D"),
            ("4", "#2E2E2E", "#3E3E3E"), ("5", "#2E2E2E", "#3E3E3E"), ("6", "#2E2E2E", "#3E3E3E"), ("-", "#FF9800", "#FFB74D"),
            ("1", "#2E2E2E", "#3E3E3E"), ("2", "#2E2E2E", "#3E3E3E"), ("3", "#2E2E2E", "#3E3E3E"), ("+", "#FF9800", "#FFB74D"),
            ("±", "#2E2E2E", "#3E3E3E"), ("0", "#2E2E2E", "#3E3E3E"), (".", "#2E2E2E", "#3E3E3E"), ("=", "#FF9800", "#FFB74D"),
        ]

        for text, bg_color, hover_color in specs:
            btn = ctk.CTkButton(
                self.frame,
                text=text,
                command=self.command_mapper(text),
                fg_color=bg_color,
                hover_color=hover_color,
                **button_config
            )
            self.buttons.append(btn)

    def _layout_buttons(self):
        for i, btn in enumerate(self.buttons):
            row = i // 4
            col = i % 4
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.frame.grid_columnconfigure(col, weight=1)
            self.frame.grid_rowconfigure(row, weight=1)

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.logic = CalculatorLogic()
        self.setup_appearance()
        self.create_widgets()
        self.setup_layout()

    def setup_appearance(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        self.root.title("EasyCalc")
        self.root.geometry("450x450")
        self.root.resizable(True, True)
        self.root.configure(fg_color="#1E1E1E")

    def create_widgets(self):
        self.display = Display(self.root)
        self.button_grid = ButtonGrid(self.root, self.map_commands)

    def setup_layout(self):
        self.display.pack(pady=(30, 20), padx=20, fill="x")
        self.button_grid.pack(padx=10, pady=10, fill="both", expand=True)

    def _update_display(self):
        expr = self.logic.get_expression()
        if len(expr) > 20 and "." not in expr:
             self.display.set(f"{float(expr):.2e}")
        else:
             self.display.set(expr)

    def map_commands(self, label: str):

        def command_wrapper(logic_method, *args):
            logic_method(*args)
            self._update_display() 

        if label.isdigit():
            return lambda: command_wrapper(self.logic.add_digit, label)
        if label in ("+", "-", "×", "÷", "%"):
            return lambda: command_wrapper(self.logic.add_operator, label)
        if label == ".":
            return lambda: command_wrapper(self.logic.add_decimal)
        if label == "C":
            return lambda: command_wrapper(self.logic.clear)
        if label == "=":
            return lambda: command_wrapper(self.logic.calculate)
        if label == "±":
            return lambda: command_wrapper(self.logic.toggle_sign)
        if label == "()":
            return lambda: command_wrapper(self.logic.add_parentheses)
        
        return lambda: None

def show_license():
    license_root = ctk.CTk()
    license_root.title("license agreement")
    license_root.geometry("600x400")
    license_root.configure(fg_color="#1E1E1E")
    text_area = ctk.CTkTextbox(license_root, wrap="word", font=("Arial", 12))
    text_area.insert("end", LICENSE_TEXT)
    text_area.configure(state="disabled")
    text_area.pack(padx=20, pady=20, fill="both", expand=True)

    def close_license():
        license_root.destroy()
        start_app()

    ok_button = ctk.CTkButton(license_root, text="OK", command=close_license)
    ok_button.pack(pady=(0, 20))
    license_root.protocol("WM_DELETE_WINDOW", close_license)
    license_root.mainloop()

def start_app():
    root = ctk.CTk()
    app = CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    show_license()
