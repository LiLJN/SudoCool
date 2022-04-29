from SudokuBoard import SudokuBoard

if __name__ == '__main__':
    easy = SudokuBoard('H')
    easy.create_game()
    while True:
        x = int(input("Enter the row to input your number: "))
        y = int(input("Enter the column to input your number: "))
        x = x-1
        y = y-1
        hints = easy.hint(x,y)
        print("Your hints:",hints)
        number = int(input("Input your number for that spot: "))
        easy.player_input(number,x,y)
        easy.player_print()