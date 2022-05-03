import tkinter as tk
from SudokuBoard import SudokuBoard

class Game:
    def __init__(self, Master, board):
        self.master = Master
        self.board = board
        self.entries = []
        self.draft_entries = []
        self.stored_time= [0,0,0]
        self.canvas = tk.Canvas(Master, bg='#ECF0F1', height=1000, width=1400)
        self.canvas.create_text(150,40,text="SudoCOOL", fill = "black", font=('Rockwell',45,'bold italic'))
        self.canvas.create_text(410,45,text="by Alan Chen", fill = "black", font=('Rockwell',35,'italic'))
        self.canvas.create_text(950,325,text="Draft Area", fill = "black", font=('Rockwell',30,'italic'))
        self.draw_line()
        self.draw_sub_line()
        self.input_number()
        self.draft_input()
        self.hint = tk.Button(self.canvas, text = "CHECK",width=17,font=('Rockwell',40,'italic'),command=self.show_result)
        self.hint.place(x=900,y=90)
        tk.Button(self.canvas, text = "QUIT!",fg='red',width=17,font=('Rockwell',40,'italic'),command=self.master.destroy).place(x=900,y=180)
        self.time = tk.Label(self.master, text=self.time_string(), font=('Rockwell',20,'bold italic'))
        self.time.pack()
        self.timer()
        self.canvas.pack(side=tk.LEFT)

    def draw_line(self):
        for i in range(11):
            if (i - 1) % 3 == 0:
                self.canvas.create_line(i * 80, 80, i * 80, 800, fill="black", width=5)
                self.canvas.create_line(80, i * 80, 800, i * 80, fill="black", width=5)
            else:
                self.canvas.create_line(i * 80, 80, i * 80, 800, fill="black", width=2)
                self.canvas.create_line(80, i * 80, 800, i * 80, fill="black", width=2)

    def draw_sub_line(self):
        for i in range(10):
            if i % 3 == 0:
                self.canvas.create_line(900+i * 50, 350, 900+i * 50, 800, fill="black", width=4)
                self.canvas.create_line(900, 350+i * 50, 1350, 350+i * 50, fill="black", width=4)
            else:
                self.canvas.create_line(900 + i * 50, 350, 900 + i * 50, 800, fill="black", width=1)
                self.canvas.create_line(900, 350 + i * 50, 1350, 350 + i * 50, fill="black", width=1)

    def call_back(self,num):
        if len(num) > 1:
            return False
        else:
            return True

    def input_number(self):
        player_grid = self.board.player_grid
        y = 120
        for i in range(len(player_grid)):
            x = 120
            for j in range(len(player_grid[i])):
                if player_grid[i][j] != 0:
                    self.canvas.create_text(x, y, text=str(player_grid[i][j]), fill="black", font=('Silom 40'))
                else:
                    number = tk.IntVar(self.master,value='')
                    vcmd = (self.master.register(self.call_back))
                    entry = tk.Entry(self.master, validate='all', validatecommand=(vcmd, '%P'), width=1, font=('Silom 40'),fg="blue",textvariable=number)
                    self.canvas.create_window(x, y,window=entry)
                    self.entries.append(entry)
                x = x + 80
            y = y + 80

    def draft_input(self):
        player_grid = self.board.player_grid
        y = 375
        for i in range(len(player_grid)):
            x = 925
            for j in range(len(player_grid[i])):
                if player_grid[i][j] != 0:
                    self.canvas.create_text(x, y, text=str(player_grid[i][j]), fill="black", font=('Chalkboard 25'))
                else:
                    number = tk.IntVar(self.master, value='')
                    vcmd = (self.master.register(self.call_back))
                    entry = tk.Entry(self.master, validate='all', validatecommand=(vcmd, '%P'), width=1,
                                     font=('Chalkboard',25), fg="red", textvariable=number)
                    self.canvas.create_window(x, y, window=entry)
                    self.draft_entries.append(entry)
                x = x + 50
            y = y + 50

    def time_string(self):
        if self.stored_time[0] < 10:
            hour_string = '0' + str(self.stored_time[0])
        else:
            hour_string = str(self.stored_time[0])
        if self.stored_time[1] < 10:
            minute_string = '0' + str(self.stored_time[1])
        else:
            minute_string = str(self.stored_time[1])
        if self.stored_time[2] < 10:
            second_string = '0' + str(self.stored_time[2])
        else:
            second_string = str(self.stored_time[2])
        time_count = hour_string + ":" + minute_string + ":" + second_string
        return time_count

    def timer(self):
        self.stored_time[2] += 1
        if self.stored_time[2] == 60:
            self.stored_time[2] = 0
            self.stored_time[1] += 1
        if self.stored_time[1] == 60:
            self.stored_time[1] = 0
            self.stored_time[0] += 1
        self.time.config(text = self.time_string())
        self.time.after(1000,self.timer)

    def ending_logic(self):
        solution = self.board.get_solution()
        player_solution = []
        player_board = self.board.player_grid
        index = 0
        for i in range(len(player_board)):
            new_lis = []
            for j in range(len(player_board[i])):
                if player_board[i][j] != 0:
                    new_lis.append(player_board[i][j])
                else:
                    element = self.entries[index].get()
                    if element.isdigit():
                        new_lis.append(int(element))
                        index += 1
                    else:
                        return False
            player_solution.append(new_lis)
        if player_solution == solution:
            return True
        else:
            return False

    def pop_up(self):
        top = tk.Toplevel(self.master)
        top.geometry("750x250")
        top.title("You Win this Game!")
        message1 = "Congrats!"
        message2 = ''
        if self.stored_time[0] == 0:
            message2 = "You find the solution in " + str(self.stored_time[1]) + " minutes " + str(
                self.stored_time[2]) + " seconds!"
        else:
            message2 = "You find the solution in " + str(self.stored_time[0]) + " hour " + str(
                self.stored_time[1]) + " minutes " + str(
                self.stored_time[2]) + " seconds."
        tk.Label(top, text=message1, font=('Rockwell', 35, 'bold italic')).place(x=285, y=80)
        tk.Label(top, text=message2, font=('Rockwell', 25, 'italic')).place(x=110, y=140)
        tk.Button(top, text="Quit", width = 5,fg='blue',font=('Rockwell',20,' bold italic'),command=self.master.destroy).place(x=325, y=170)

    def fail_pop_up(self):
        top = tk.Toplevel(self.master)
        top.geometry("750x250")
        top.title("ERROR EXISTS!")
        message = "Please double check your inputs :("
        tk.Label(top, text=message, font=('Rockwell', 35, 'bold italic')).place(x=75, y=100)
        tk.Button(top, text="Resume", width = 5,fg='black',font=('Rockwell',20,' bold italic'),command=top.destroy).place(x=325,y=160)

    def show_result(self):
        if self.ending_logic():
            self.pop_up()
        else:
            self.fail_pop_up()

    def bind_entries(self):
        fill_list = []
        for i in range(len(self.entries)):
            fill_list.append(int(self.entries[i].get()))
        for i in range(len(self.draft_entries)):
            self.draft_entries[i].delete(0,1)
        for i in range(len(fill_list)):
            self.draft_entries[i].insert(fill_list[i])
        print(fill_list)