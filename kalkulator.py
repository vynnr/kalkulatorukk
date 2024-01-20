import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import random

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

        ttk.Button(root, text="Mulai Game", command=self.start_game).grid(row=row_val + 1, column=0, columnspan=4, sticky="nsew")

        ttk.Button(root, text="Info Pembuat", command=self.show_info).grid(row=row_val + 2, column=0, columnspan=4, sticky="nsew")

        self.running_text_canvas = tk.Canvas(root, width=400, height=30, bg='#f2f2f2', highlightthickness=0)
        self.running_text_canvas.grid(row=row_val + 3, column=0, columnspan=4, sticky="nsew")

        self.running_text = "Selamat datang di kalkulator Alvin. "
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
        info_text = "Kalkulator\nPembuat: Alvin\nVersi: 1.0"
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

    def start_game(self):
        game_window = tk.Toplevel(self.root)
        snake_game = SnakeGame(game_window)

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")

        self.canvas = tk.Canvas(self.master, width=300, height=300, bg="black")
        self.canvas.pack()

        self.restart_button = tk.Button(self.master, text="Mulai Ulang", command=self.restart_game)
        self.restart_button.pack_forget()

        self.start_button = tk.Button(self.master, text="Mulai Game", command=self.start_game)
        self.start_button.pack()

        self.snake = []
        self.snake_direction = "Right"
        self.food = None
        self.score = 0
        self.score_label = tk.Label(self.master, text="Skor: 0")
        self.score_label.pack()

        self.master.bind("<Up>", lambda event: self.change_direction("Up"))
        self.master.bind("<Down>", lambda event: self.change_direction("Down"))
        self.master.bind("<Left>", lambda event: self.change_direction("Left"))
        self.master.bind("<Right>", lambda event: self.change_direction("Right"))

    def start_game(self):
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.snake_direction = "Right"
        self.food = self.spawn_food()
        self.score = 0
        self.score_label.config(text="Skor: 0")
        self.start_button.pack_forget()
        self.update_game()

    def restart_game(self):
        self.canvas.delete("all")
        self.restart_button.pack_forget()
        self.start_button.pack()
        self.snake = []
        self.snake_direction = "Right"
        self.food = None
        self.score = 0
        self.score_label.config(text="Skor: 0")

    def spawn_food(self):
        x = random.randint(1, 29) * 10
        y = random.randint(1, 29) * 10
        return self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="red")

    def change_direction(self, direction):
        opposite_directions = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if direction != opposite_directions[self.snake_direction]:
            self.snake_direction = direction

    def move_snake(self):
        head = self.snake[0]
        if self.snake_direction == "Up":
            new_head = (head[0], head[1] - 10)
        elif self.snake_direction == "Down":
            new_head = (head[0], head[1] + 10)
        elif self.snake_direction == "Left":
            new_head = (head[0] - 10, head[1])
        elif self.snake_direction == "Right":
            new_head = (head[0] + 10, head[1])

        self.snake = [new_head] + self.snake[:-1]

        if self.check_collision():
            self.game_over()

        if self.check_food_collision():
            self.canvas.delete(self.food)
            self.food = self.spawn_food()
            self.extend_snake()
            self.update_score()

        self.draw_snake()

    def draw_snake(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="green", tags="snake")

    def check_collision(self):
        head = self.snake[0]
        return (head[0] < 0 or head[0] >= 300 or
                head[1] < 0 or head[1] >= 300 or
                head in self.snake[1:])

    def check_food_collision(self):
        head = self.snake[0]
        food_coords = self.canvas.coords(self.food)
        return head[0] == food_coords[0] and head[1] == food_coords[1]

    def extend_snake(self):
        tail = self.snake[-1]
        if self.snake_direction == "Up":
            new_tail = (tail[0], tail[1] + 10)
        elif self.snake_direction == "Down":
            new_tail = (tail[0], tail[1] - 10)
        elif self.snake_direction == "Left":
            new_tail = (tail[0] + 10, tail[1])
        elif self.snake_direction == "Right":
            new_tail = (tail[0] - 10, tail[1])

        self.snake.append(new_tail)

    def update_score(self):
        self.score += 1
        self.score_label.config(text=f"Skor: {self.score}")

    def update_game(self):
        # Pastikan untuk menghapus snake terlebih dahulu sebelum memindahkan snake
        self.canvas.delete("snake")
        self.move_snake()

        if self.check_collision():
            self.canvas.create_text(150, 150, text="Game Over", fill="white", font=("Helvetica", 16, "bold"))
            self.restart_button.pack()

        self.master.after(100, self.update_game)

    def game_over(self):
        self.restart_button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
