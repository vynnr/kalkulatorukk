import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.expression = ""
        self.history = []

        label_kalkulator = tk.Label(root, text="Kalkulator", font=("Helvetica", 18), pady=10, bg='#e6e6e6')
        label_kalkulator.grid(row=0, column=0, columnspan=4, sticky="nsew")

        self.root.configure(bg='#f2f2f2')

        self.entry = tk.Entry(root, font=("Helvetica", 16), justify="right", bd=5)
        self.entry.grid(row=1, column=0, columnspan=4, sticky="nsew")

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C', 'Hapus', 'Hapus Histori', 'Histori'
        ]
        row_val = 2
        col_val = 0
        for button in buttons:
            ttk.Button(root, text=button, command=lambda btn=button: self.button_click(btn)).grid(row=row_val, column=col_val, sticky="nsew")
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

        ttk.Button(root, text="Info Pembuat", command=self.show_info).grid(row=row_val + 1, column=0, columnspan=4, sticky="nsew")

        self.running_text_canvas = tk.Canvas(root, width=400, height=30, bg='#f2f2f2', highlightthickness=0)
        self.running_text_canvas.grid(row=row_val + 2, column=0, columnspan=4, sticky="nsew")

        self.running_text = "Selamat datang di kalkulator asep. "
        self.marquee()

        for i in range(1, 8):
            root.grid_rowconfigure(i, weight=1)
            root.grid_columnconfigure(i, weight=1)

    def button_click(self, button_text):
        if button_text == '=':
            try:
                result = str(eval(self.expression))
                self.history.append(f"{self.expression} = {result}")
                self.expression = result
            except ZeroDivisionError:
                self.expression = "Error: Division by zero"
            except Exception as e:
                self.expression = "Error: Invalid expression"
        elif button_text == 'C':
            self.reset()
        elif button_text == 'Hapus':
            self.remove_last_entry()
        elif button_text == 'Hapus Histori':
            self.clear_history()
        elif button_text == 'Histori':
            self.show_history()
        else:
            self.expression += button_text

        self.update_entry()

    def update_entry(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.expression)

    def reset(self):
        self.expression = ""
        self.update_entry()

    def remove_last_entry(self):
        if len(self.expression) > 0:
            self.expression = self.expression[:-1]

        self.update_entry()

    def clear_history(self):
        self.history = []

    def show_history(self):
        history_text = "\n".join(self.history)
        messagebox.showinfo("Histori Perhitungan", history_text)

    def show_info(self):
        info_text = "Kalkulator\nPembuat: Asep\nVersi: 1.0"
        messagebox.showinfo("Informasi Pembuat", info_text)

    def marquee(self):
        self.running_text_canvas.delete("marquee")
        text_width = self.running_text_canvas.create_text(400, 15, text=self.running_text, anchor="w", font=("Helvetica", 12), fill="black")
        text_bbox = self.running_text_canvas.bbox(text_width)
        text_width = text_bbox[2] - text_bbox[0]
        start_pos = 400
        end_pos = -text_width
        self.running_text_canvas.create_text(start_pos, 15, text=self.running_text, anchor="w", tags="marquee", font=("Helvetica", 12, "italic", "bold"), fill="blue")
        self.animate_marquee(start_pos, end_pos)

    def animate_marquee(self, start_pos, end_pos):
        self.running_text_canvas.move("marquee", -2, 0)
        pos = self.running_text_canvas.coords("marquee")[0]
        if pos < end_pos:
            self.running_text_canvas.move("marquee", start_pos - end_pos, 0)
        self.root.after(25, lambda: self.animate_marquee(start_pos, end_pos))

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
