import random
import copy


class SudokuBoard:
    def __init__(self, mode):
        self._grids = [[], [], [], [], [], [], [], [], []]
        self.player_grid = []
        self._ori_positions = dict()
        self._mode = mode

    def _start_over(self):
        for i in range(9):
            for j in range(9):
                if self._grids[i][j] != 0:
                    self._grids[i][j] = 0
        self._ori_positions.clear()

    def _check_row(self, i, num):
        if num in self._grids[i]:
            return False
        return True

    def _check_col(self, i, num):
        for rows in self._grids:
            if num == rows[i]:
                return False
        return True

    def _check_grid(self, x, num):
        if 0 <= x <= 2:
            for r in range(3):
                if x == 0:
                    for c in range(3):
                        if num == self._grids[r][c]:
                            return False
                elif x == 1:
                    for c in range(3, 6):
                        if num == self._grids[r][c]:
                            return False
                else:
                    for c in range(6, 9):
                        if num == self._grids[r][c]:
                            return False
        elif 3 <= x <= 5:
            for r in range(3, 6):
                if x == 3:
                    for c in range(3):
                        if num == self._grids[r][c]:
                            return False
                elif x == 4:
                    for c in range(3, 6):
                        if num == self._grids[r][c]:
                            return False
                else:
                    for c in range(6, 9):
                        if num == self._grids[r][c]:
                            return False
        else:
            for r in range(6, 9):
                if x == 6:
                    for c in range(3):
                        if num == self._grids[r][c]:
                            return False
                elif x == 7:
                    for c in range(3, 6):
                        if num == self._grids[r][c]:
                            return False
                else:
                    for c in range(6, 9):
                        if num == self._grids[r][c]:
                            return False
        return True

    def _check(self, x, y, grid_num, num):
        if self._check_row(x, num) and self._check_col(y, num) and self._check_grid(grid_num, num):
            return True
        return False

    def _get_grid_num(self, i, j):
        ans = 0
        if 0 <= i <= 2:
            if 0 <= j <= 2:
                ans = 0
            elif 3 <= j <= 5:
                ans = 1
            else:
                ans = 2
        elif 3 <= i <= 5:
            if 0 <= j <= 2:
                ans = 3
            elif 3 <= j <= 5:
                ans = 4
            else:
                ans = 5
        else:
            if 0 <= j <= 2:
                ans = 6
            elif 3 <= j <= 5:
                ans = 7
            else:
                ans = 8
        return ans

    def _find_empty(self, ver):
        for row in range(9):
            for col in range(9):
                if self._grids[row][col] == 0:
                    ver[0] = row
                    ver[1] = col
                    return True
        return False

    def _backtrack(self):
        ver = [0, 0]
        if not self._find_empty(ver):
            return True
        row = ver[0]
        col = ver[1]
        grid_num = self._get_grid_num(row, col)
        for num in range(1, 10):
            if self._check(row, col, grid_num, num):
                self._grids[row][col] = num
                if self._backtrack():
                    return True
                self._grids[row][col] = 0
        return False

    def _read_file(self):
        file = open("0.txt", "r")
        choose = random.randint(1, 2)
        if self._mode == 'E':
            if choose == 2:
                file.close()
                file = open("1.txt", "r")
        elif self._mode == 'M':
            file.close()
            if choose == 1:
                file = open("2.txt", "r")
            else:
                file = open("3.txt", "r")
        else:
            file.close()
            if choose == 1:
                file = open("4.txt", "r")
            else:
                file = open("5.txt", "r")
        select = random.randint(1, 10000)
        count = 0
        line = ''
        while count < select:
            count += 1
            line = file.readline()
        file.close()
        num_count = 0
        count = 0
        for number in line:
            if number != '\n':
                self._grids[count].append(int(number))
            num_count += 1
            if num_count % 9 == 0:
                num_count = 0
                count += 1
        for x in range(len(self._grids)):
            for y in range(len(self._grids[x])):
                if self._grids[x][y] != 0:
                    if x in self._ori_positions.keys():
                        self._ori_positions[x].append(y)
                    else:
                        self._ori_positions[x] = [y]

    def _player_check(self, row, col, num):
        for x in range(9):
            if num in self.player_grid[row]:
                return False
        for x in range(9):
            if self.player_grid[x][col] == num:
                return False
        ori_row = row - row % 3
        ori_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if self.player_grid[i + ori_row][j + ori_col] == num:
                    return False
        return True

    def _check_ori(self, x, y):
        if x in self._ori_positions.keys():
            if y in self._ori_positions[x]:
                return False
        return True

    def create_game(self):
        self._read_file()
        self.player_grid = copy.deepcopy(self._grids)
        condition = self._backtrack()
        while not condition:
            self._start_over()
            self._read_file()
            condition = self._backtrack()
        self.player_print()
        print('')
        self._print_grid()

    def _print_grid(self):
        count = 0
        for element in self._grids:
            sub_count = 0
            for numbers in element:
                sub_count += 1
                if sub_count % 3 == 0 and sub_count != 9:
                    if numbers == 0:
                        print('?' + '  |  ', end='')
                    else:
                        print(str(numbers) + '  |  ', end='')
                else:
                    if numbers == 0:
                        print('?' + '  ', end='')
                    else:
                        print(str(numbers) + '  ', end='')
            print('')
            count = count + 1
            if count % 3 == 0 and count != 9:
                print("---------+-----------+----------")
        print('')

    def player_print(self):
        count = 0
        for element in self.player_grid:
            sub_count = 0
            for numbers in element:
                sub_count += 1
                if sub_count % 3 == 0 and sub_count != 9:
                    if numbers == 0:
                        print('?' + '  |  ', end='')
                    else:
                        print(str(numbers) + '  |  ', end='')
                else:
                    if numbers == 0:
                        print('?' + '  ', end='')
                    else:
                        print(str(numbers) + '  ', end='')
            print('')
            count = count + 1
            if count % 3 == 0 and count != 9:
                print("---------+-----------+----------")

    def player_input(self, num, x, y):
        if self._check_ori(x, y):
            print("Error! Number already exists!!")
        elif self._player_check(x, y, num):
            self.player_grid[x][y] = num
        else:
            print("Number illegal.")

    def hint(self, x, y):
        hints = []
        if self.player_grid[x][y] != 0:
            return hints
        for i in range(9):
            if self._player_check(x, y, i + 1):
                hints.append(i + 1)
        return hints

    def player_delete(self, x, y):
        if self._check_ori(x, y):
            print("Error! That number is not eligible to delete!")
        else:
            self.player_grid[x][y] = 0

