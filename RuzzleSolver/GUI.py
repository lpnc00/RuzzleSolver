from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import re
from unidecode import unidecode
from Solver import Graph


class App(Tk):
    def __init__(self):
        super().__init__()

        self.__bonusList = []
        self.__entryList = []

        self.Language = ''
        self.LetterGrid = []
        self.BonusGrid = []

        self.iconbitmap('./RuzzleSolver/ruzzle.ico')
        self.withdraw()
        self.__Letter()
        self.mainloop()

    def __WM_destroy(self):
        for widget in self.winfo_children():
            if isinstance(widget, Toplevel):
                widget.destroy()

    def __Letter(self):

        def validate(P, W):
            widget = self.nametowidget(W)
            if P == '':
                return True
            elif re.match('^[A-Z]$', P):
                widget.tk_focusNext().focus()
                return True
            else:
                return False

        def on_invalid(P, v, W):
            widget = self.nametowidget(W)
            if P.isalpha() and len(P) == 1:
                widget.insert(0, unidecode(P).upper())
                widget.tk_focusNext().focus()
            widget.after_idle(lambda W, v: self.nametowidget(W).configure(validate=v), W, v)

        def check(event=None):
            self.Language = lang.get()
            self.LetterGrid = []
            if self.Language == '':
                messagebox.showerror('Error', 'You have not selected any language'
                                              '\n Insert language to continue')
                lang.focus_set()
                return
            for x in range(4):
                self.LetterGrid.append([])
                for y in range(4):
                    ltr = self.__entryList[x][y].get()
                    if ltr == '':
                        messagebox.showerror('Error', 'Your grid contain one or more empty box '
                                                      '\n Insert missing letters to continue')
                        self.__entryList[x][y].focus_set()
                        return
                    self.LetterGrid[x].append(ltr)
            self.__Bonus()

        self.LetterGrid = []
        self.BonusGrid = []
        self.__WM_destroy()

        grid_w = Toplevel()
        grid_w.title('Letter Input')
        grid_w.option_add("*Entry.font", "Arial 50 bold")
        grid_w.iconbitmap('./RuzzleSolver/ruzzle.ico')
        grid_w.rowconfigure(5, minsize=10)
        grid_w.rowconfigure(7, minsize=10)
        grid_w.protocol("WM_DELETE_WINDOW", self.destroy)
        vcmd = (self.register(validate), '%P', '%W')
        ivcmd = (self.register(on_invalid), '%P', '%v', '%W')
        for x in range(4):
            self.__entryList.append([])
            for y in range(4):
                self.__entryList[x].append('')
                self.__entryList[x][y] = Entry(grid_w, bg="white", width=2, justify="center",
                                               takefocus=True, insertofftime=True,
                                               validate="key", validatecommand=vcmd,
                                               invalidcommand=ivcmd)
                self.__entryList[x][y].grid(row=x, column=y)
        Label(grid_w, text='Language:').grid(row=6, column=0, sticky=E)
        lang = ttk.Combobox(grid_w, values=['', 'English', 'Italian', 'Spanish'], width=8, state='readonly')
        lang.grid(row=6, column=1, sticky=W)
        lang.bind("<Return>", lambda e: lang.event_generate('<Down>'))
        lang.bind("<<ComboboxSelected>>", lambda e: lang.tk_focusNext().focus())
        nxt = Button(grid_w, text='Next', command=check)
        nxt.grid(row=6, column=2, sticky=EW)
        Button(grid_w, text='New Game', command=self.__Letter).grid(row=6, column=3, sticky=EW)
        nxt.bind('<Return>', check)

        self.__entryList[0][0].focus()
        self.eval(f'tk::PlaceWindow {str(grid_w)} center')

    def __Bonus(self):
        self.__WM_destroy()
        bonus_w = Toplevel()
        bonus_w.title('Bonus Input')
        bonus_w.protocol("WM_DELETE_WINDOW", self.destroy)
        bonus_w.iconbitmap('./RuzzleSolver/ruzzle.ico')
        bonus_w.rowconfigure(5, minsize=10)
        bonus_w.rowconfigure(7, minsize=10)
        bonuses = ['', 'DW', 'DL', 'TW', 'TL']
        for x in range(4):
            self.__bonusList.append([])
            for y in range(4):
                self.__bonusList[x].append('')
                self.__bonusList[x][y] = ttk.Combobox(bonus_w, values=bonuses,
                                                      font="Arial 50 bold", width=3, state='readonly')
                self.__bonusList[x][y].grid(row=x, column=y)
        Button(bonus_w, text='Solve', command=self.__Solve).grid(row=6, column=2, sticky=EW)
        Button(bonus_w, text='New Game', command=self.__Letter).grid(row=6, column=3, sticky=EW)
        self.eval(f'tk::PlaceWindow {str(bonus_w)} center')

    def __Solve(self):

        def path_show(event):
            def animation():
                i = 1
                for x, y in coord:
                    entryList[x][y].config(disabledbackground="white")
                    path_w.after(250 * i, change_bg, entryList, x, y)
                    i += 1

            def change_bg(entryList, x, y):
                entryList[x][y].config(disabledbackground="#ff6e00")

            selection = event.widget.curselection()
            word = event.widget.get(selection[0]).split(' ')[0].lower()
            path_w = Toplevel()
            path_w.title('Path Show')
            path_w.option_add("*Entry.Font", "Arial 50 bold")
            path_w.iconbitmap('./RuzzleSolver/ruzzle.ico')
            entryList = []
            for x in range(4):
                entryList.append([])
                for y in range(4):
                    entryList[x].append('')
                    entryList[x][y] = Entry(path_w, bg="white", width=2, justify="center",
                                            disabledbackground="white",
                                            disabledforeground="black")
                    entryList[x][y].insert(END, self.LetterGrid[x][y])
                    entryList[x][y].config(state=DISABLED)
                    entryList[x][y].grid(row=x, column=y)
            path_w.rowconfigure(4, minsize=10)
            Button(path_w, text='Show animation again', command=animation) \
                .grid(row=5, column=1, columnspan=2, sticky=EW)
            coord = solver[word][2]  
            animation()

        for x in range(4):
            self.BonusGrid.append([])
            for y in range(4):
                self.BonusGrid[x].append(self.__bonusList[x][y].get().upper())
        self.__WM_destroy()
        solver = Graph(self.LetterGrid, self.BonusGrid, self.Language).summary()
        ordered_wordlist = sorted(solver, key=lambda k: solver[k][1])
        ordered_wordlist.reverse()
        solve_w = Toplevel()
        solve_w.title('Words solution')
        solve_w.protocol("WM_DELETE_WINDOW", self.destroy)
        solve_w.iconbitmap('./RuzzleSolver/ruzzle.ico')
        solve_w.rowconfigure(0, minsize=10)
        solve_w.rowconfigure(2, minsize=10)
        solve_w.rowconfigure(4, minsize=10)
        solve_w.rowconfigure(6, minsize=10)

        Label(solve_w, text='Double click on any word\nto see the path on the grid',
              font="Arial 16").grid(row=1, column=0)
        Button(solve_w, text='New Game', command=self.__Letter).grid(row=7, column=0)
        scrollbar = Scrollbar(solve_w)
        scrollbar.grid(row=3, column=1, sticky=NS)
        lst = Listbox(solve_w, yscrollcommand=scrollbar.set, height=20, font="Arial 14")
        lst.grid(row=3, column=0)
        lst.bind('<Double-1>', path_show)
        total_score = 0
        for word in ordered_wordlist:
            score = solver[word][1]
            total_score += score
            lst.insert(END, f'{word.upper()} {score}')  
        scrollbar.config(command=lst.yview)
        Label(solve_w, text=f'Total Score: {total_score} \nWords found: {len(ordered_wordlist)}',
              font="Arial 16").grid(row=5, column=0)
        self.eval(f'tk::PlaceWindow {str(solve_w)} center')

