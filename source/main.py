# Copyright (C) 2026 bo7dan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# LICENSE file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import customtkinter as ctk
import re

# -------------------- Calculator Logic --------------------
class CalculatorLogic:
    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self.expression = "0"

    def get_expression(self) -> str:
        return self.expression

    def add_digit(self, digit: str) -> None:
        if self.expression in ("0", "Error"):
            self.expression = digit
        else:
            self.expression += digit

    def add_operator(self, operator: str) -> None:
        if self.expression == "Error":
            return

        op = {"÷": "/", "×": "*", "+": "+", "-": "-", "%": "%"}.get(operator, operator)
        if self.expression[-1:] in "+-*/%":
            self.expression = self.expression[:-1] + op
        else:
            self.expression += op

    def add_decimal(self) -> None:
        if self.expression == "Error":
            return
        parts = re.split(r'[-+*/%]', self.expression)
        if "." not in parts[-1]:
            self.expression += "."

    def toggle_sign(self) -> None:
        if self.expression == "Error":
            return
        match = re.search(r'(\d+\.?\d*)$', self.expression)
        if match:
            number = match.group(1)
            start = match.start(1)
            if number.startswith("-"):
                self.expression = self.expression[:start] + number[1:]
            else:
                self.expression = self.expression[:start] + "-" + number

    def add_parentheses(self) -> None:
        if self.expression == "Error":
            return
        open_count = self.expression.count("(")
        close_count = self.expression.count(")")
        if open_count == close_count or self.expression[-1] in "+-*/%(":
            self.expression += "("
        elif open_count > close_count and (self.expression[-1].isdigit() or self.expression[-1] == ")"):
            self.expression += ")"
        else:
            self.expression += "("

    def clear(self) -> None:
        self.reset()

    def calculate(self) -> None:
        try:
            expr = self.expression.replace("×", "*").replace("÷", "/").replace("%", "/100*")
            if not re.match(r'^[+\-*/()%.\d\s]+$', expr):
                raise ValueError("Invalid characters")
            result = eval(expr, {"__builtins__": None}, {})
            if isinstance(result, float) and result.is_integer():
                self.expression = str(int(result))
            else:
                self.expression = str(result)
        except Exception:
            self.expression = "Error"

# -------------------- Display --------------------
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

# -------------------- Button Grid --------------------
class ButtonGrid:
    COLORS = {
        "digit": "#2E2E2E",
        "operator": "#FF9800",
        "hover": "#3E3E3E",
        "clear": "#FF5252"
    }

    def __init__(self, master, command_mapper):
        self.frame = ctk.CTkFrame(master, fg_color="transparent")
        self.command_mapper = command_mapper
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
            ("C", "clear"), ("()", "digit"), ("%", "operator"), ("÷", "operator"),
            ("7", "digit"), ("8", "digit"), ("9", "digit"), ("×", "operator"),
            ("4", "digit"), ("5", "digit"), ("6", "digit"), ("-", "operator"),
            ("1", "digit"), ("2", "digit"), ("3", "digit"), ("+", "operator"),
            ("±", "digit"), ("0", "digit"), (".", "digit"), ("=", "operator")
        ]

        self.buttons = []
        for text, typ in specs:
            color = self.COLORS.get(typ, "#2E2E2E")
            btn = ctk.CTkButton(
                self.frame,
                text=text,
                fg_color=color,
                hover_color=self.COLORS["hover"],
                command=lambda t=text: self.command_mapper(t)(),
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

# -------------------- Calculator App --------------------
class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.logic = CalculatorLogic()
        self._setup_appearance()
        self._create_widgets()
        self._setup_layout()

    def _setup_appearance(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        self.root.title("EasyCalc")
        self.root.geometry("450x550")
        self.root.minsize(400, 500)
        self.root.configure(fg_color="#1E1E1E")

    def _create_widgets(self):
        self.display = Display(self.root)
        self.button_grid = ButtonGrid(self.root, self._map_commands)

    def _setup_layout(self):
        self.display.pack(pady=(30, 20), padx=20, fill="x")
        self.button_grid.pack(padx=10, pady=10, fill="both", expand=True)

    def _update_display(self):
        expr = self.logic.get_expression()
        if len(expr) > 12:
            try:
                self.display.set(f"{float(expr):.8g}")
            except:
                self.display.set(expr)
        else:
            self.display.set(expr)

    def _map_commands(self, label: str):
        command_map = {
            "C": self.logic.clear,
            "=": self.logic.calculate,
            "±": self.logic.toggle_sign,
            "()": self.logic.add_parentheses,
            ".": self.logic.add_decimal,
            "+": lambda: self.logic.add_operator("+"),
            "-": lambda: self.logic.add_operator("-"),
            "×": lambda: self.logic.add_operator("×"),
            "÷": lambda: self.logic.add_operator("÷"),
            "%": lambda: self.logic.add_operator("%"),
        }
        if label.isdigit():
            return lambda: self._execute(self.logic.add_digit, label)
        return lambda: self._execute(command_map.get(label, lambda: None))

    def _execute(self, func, *args):
        func(*args)
        self._update_display()

# -------------------- Start App --------------------
def start_app():
    root = ctk.CTk()
    app = CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    start_app()
