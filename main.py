import tkinter as tk
from tkinter import messagebox
import numpy as np

class Connect4Game:
    def __init__(self):
        self.board = np.zeros((6, 7))
        self.game_over = False
        self.turn = 0

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[5][col] == 0

    def get_next_open_row(self, col):
        for r in range(6):
            if self.board[r][col] == 0:
                return r

    def winning_move(self, piece):
        # Check horizontal locations for a win
        for c in range(7 - 3):
            for r in range(6):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return True

        # Check vertical locations for a win
        for c in range(7):
            for r in range(6 - 3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True

        # Check positively sloped diagonals
        for c in range(7 - 3):
            for r in range(6 - 3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diagonals
        for c in range(7 - 3):
            for r in range(3, 6):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True

        return False

class Connect4GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect 4")

        self.game = Connect4Game()
        self.canvas = tk.Canvas(root, width=700, height=600, bg="blue")
        self.canvas.pack()

        self.light_mode = True
        self.draw_board()
        self.root.bind("<Button-1>", self.click)

        self.switch_mode_button = tk.Button(root, text="Switch to Dark Mode", command=self.switch_mode)
        self.switch_mode_button.pack(pady=10)

    def draw_board(self):
        self.canvas.delete("all")
        for c in range(7):
            for r in range(6):
                x0 = c * 100 + 5
                y0 = r * 100 + 5
                x1 = (c + 1) * 100 - 5
                y1 = (r + 1) * 100 - 5
                self.canvas.create_oval(x0, y0, x1, y1, fill="white", outline="black")
        
        self.update_board()

    def switch_mode(self):
        if self.light_mode:
            self.canvas.config(bg="black")
            self.switch_mode_button.config(text="Switch to Light Mode")
            self.light_mode = False
        else:
            self.canvas.config(bg="blue")
            self.switch_mode_button.config(text="Switch to Dark Mode")
            self.light_mode = True
        
        self.update_board()

    def click(self, event):
        x = event.x
        col = x // 100

        if self.game.is_valid_location(col):
            row = self.game.get_next_open_row(col)
            self.game.drop_piece(row, col, 1 if self.game.turn == 0 else 2)

            if self.game.winning_move(1 if self.game.turn == 0 else 2):
                winner = "Player 1" if self.game.turn == 0 else "Player 2"
                messagebox.showinfo("Connect 4", f"{winner} wins!")
                self.game = Connect4Game()
                self.draw_board()
                return

            self.game.turn += 1
            self.game.turn %= 2

            self.update_board()

    def update_board(self):
        for c in range(7):
            for r in range(6):
                x0 = c * 100 + 5
                y0 = (5 - r) * 100 + 5
                x1 = (c + 1) * 100 - 5
                y1 = (6 - r) * 100 - 5
                color = "white"
                if self.game.board[r][c] == 1:
                    color = "red"
                elif self.game.board[r][c] == 2:
                    color = "yellow"
                self.canvas.create_oval(x0, y0, x1, y1, fill=color, outline="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = Connect4GUI(root)
    root.mainloop()
