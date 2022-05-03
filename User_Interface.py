import tkinter as tk
from Game import Game
from SudokuBoard import SudokuBoard

if __name__ == '__main__':
    print("Please enter a difficulty for your SudoCool Game.")
    mode = input("\"E\" for easy,\"M\" for medium and \"H\" for hard: ")
    board = SudokuBoard(mode)
    board.create_game()
    root = tk.Tk()
    root.title("SudoCool Game Launcher")
    frame = Game(root,board)
    root.mainloop()


