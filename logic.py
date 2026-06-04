import random
class MemoryGameLogic:
    def __init__(self, rows=6, cols=6):
        self.rows = rows
        self.cols = cols
        self.cards = []
        self.revealed = []
        self.first_selected = None
        self.moves = 0
        self.reset_game()

    def reset_game(self):
        num_pairs = (self.rows * self.cols) // 2
        values = [chr(65 + i) for i in range(num_pairs)] * 2
        random.shuffle(values)
        self.cards = [values[i * self.cols:(i + 1) * self.cols] for i in range(self.rows)]
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.first_selected = None
        self.moves = 0

    def get_value(self, row, col):
        return self.cards[row][col]

    def is_revealed(self, row, col):
        return self.revealed[row][col]

    def select_card(self, row, col):
        if self.revealed[row][col]:
            return None
        if self.first_selected is None:
            self.first_selected = (row, col)
            return 'first', None
        else:
            r1, c1 = self.first_selected
            if r1 == row and c1 == col:
                return None
            self.first_selected = None
            self.moves += 1
            if self.cards[r1][c1] == self.cards[row][col]:
                self.revealed[r1][c1] = True
                self.revealed[row][col] = True
                return 'match', (r1, c1)
            else:
                return 'mismatch', (r1, c1)

    def is_game_over(self):
        for row in self.revealed:
            if not all(row):
                return False
        return True
