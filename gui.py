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
        self.is_animating = False
        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.create_widgets()

    def create_widgets(self):
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(
                    self.root,
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

    def on_card_click(self, row, col):
        if self.is_animating or self.logic.is_revealed(row, col):
            return
        self.buttons[row][col].config(text=self.logic.get_value(row, col), bg="#1E90FF")
        result = self.logic.select_card(row, col)
        if not result:
            return
        status, prev_coords = result
        if status == 'match':
            r1, c1 = prev_coords
            self.buttons[r1][c1].config(bg="#3CB371")
            self.buttons[row][col].config(bg="#3CB371")
            if self.logic.is_game_over():
                messagebox.showinfo("Вітання!", "Ви відкрили всі зображення! Поставте 40 балів, будь ласка :)")
                self.reset_gui()
        elif status == 'mismatch':
            self.is_animating = True
            r1, c1 = prev_coords
            self.root.after(1000, lambda: self.hide_cards(r1, c1, row, col))

    def hide_cards(self, r1, c1, r2, c2):
        self.buttons[r1][c1].config(text="?", bg="#FF0000")
        self.buttons[r2][c2].config(text="?", bg="#FF0000")
        self.is_animating = False

    def reset_gui(self):
        self.logic.reset_game()
        for r in range(self.rows):
            for c in range(self.cols):
                self.buttons[r][c].config(text="?", bg="#FF69B4")

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryGameGUI(root)
    root.mainloop()