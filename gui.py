import tkinter as tk
from tkinter import messagebox
from logic import MemoryGameLogic

class MemoryGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Тренування пам'яті (Zikava gra)")
        self.rows = 6
        self.cols = 6
        self.logic = MemoryGameLogic(self.rows, self.cols)
        self.is_animating = True
        self.time_left = 300
        self.timer_id = None
        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.create_widgets()

    def create_widgets(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(side="top", fill="x", pady=10)
        self.timer_label = tk.Label(
            top_frame,
            text="Час: 05:00",
            font=("Arial", 16, "bold"),
            fg="red"
        )
        self.timer_label.pack(side="left", padx=20)
        self.moves_label = tk.Label(
            top_frame,
            text="Ходи: 0",
            font=("Arial", 16, "bold"),
            fg="blue"
        )
        self.moves_label.pack(side="left", padx=20)
        self.start_button = tk.Button(
            top_frame,
            text="СТАРТ",
            font=("Arial", 12, "bold"),
            bg="#3CB371",
            fg="white",
            command=self.start_game
        )
        self.start_button.pack(side="right", padx=20)
        grid_frame = tk.Frame(self.root)
        grid_frame.pack(side="bottom", padx=10, pady=10)
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(
                    grid_frame,
                    text="?",
                    font=("Arial", 18, "bold"),
                    width=4,
                    height=2,
                    bg="#FF69B4",
                    fg="white",
                    command=lambda row=r, col=c: self.on_card_click(row, col)
                )
                btn.grid(row=r, column=c, padx=4, pady=4)
                self.buttons[r][c] = btn

    def start_game(self):
        self.start_button.config(state="disabled", bg="#A9A9A9")
        self.is_animating = False
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            self.timer_label.config(text=f"Час: {minutes:02d}:{seconds:02d}")
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            messagebox.showwarning("Час вийшов!", "Спробуйте ще раз!")
            self.root.destroy()

    def on_card_click(self, row, col):
        if self.is_animating or self.logic.is_revealed(row, col):
            return
        self.buttons[row][col].config(text=self.logic.get_value(row, col), bg="#1E90FF")
        result = self.logic.select_card(row, col)
        if not result:
            return
        status, prev_coords = result
        if status in ('match', 'mismatch'):
            self.moves_label.config(text=f"Ходи: {self.logic.moves}")
        if status == 'match':
            r1, c1 = prev_coords
            self.buttons[r1][c1].config(bg="#3CB371")
            self.buttons[row][col].config(bg="#3CB371")
            if self.logic.is_game_over():
                if self.timer_id:
                    self.root.after_cancel(self.timer_id)
                messagebox.showinfo("Вітання!",
                                    f"Ви відкрили всі зображення за {self.logic.moves} ходів!\nПоставте 40 балів, будь ласка :)")
                self.reset_gui()
        elif status == 'mismatch':
            self.is_animating = True
            r1, c1 = prev_coords
            self.root.after(1000, lambda: self.hide_cards(r1, c1, row, col))

    def hide_cards(self, r1, c1, r2, c2):
        self.buttons[r1][c1].config(text="?", bg="#FF69B4")
        self.buttons[r2][c2].config(text="?", bg="#FF69B4")
        self.is_animating = False

    def reset_gui(self):
        self.logic.reset_game()
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.time_left = 300
        self.timer_label.config(text="Час: 05:00")
        self.moves_label.config(text="Ходи: 0")
        self.is_animating = True
        self.start_button.config(state="normal", bg="#3CB371")
        for r in range(self.rows):
            for c in range(self.cols):
                self.buttons[r][c].config(text="?", bg="#FF69B4")
