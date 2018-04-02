#! python3
from logging import (
    getLogger,
    DEBUG)
import tkinter as tk
from os.path import join
from generate_images import NAMES as IMAGE_NAMES
from threading import Thread
from operator import mul
from itertools import count
from time import time as get_time
from time import sleep
from functools import partial
from random import randrange

logger = getLogger("game")
logger.setLevel(DEBUG)


def _near(cell, size, included=False):
    width, height = size
    row = cell // width
    col = cell % width
    zip1 = list(zip((-width, 0, width), (row, 1, row < height - 1)))
    zip2 = list(zip((-1, 0, 1), (col, 1, col < height - 1)))
    return set(cell + v + h for v, c1 in zip1 if c1
               for h, c2 in zip2 if c2 and v | h | included)


def timer(callback, miliseconds):
    def w():
        while not callback():
            sleep(miliseconds / 1000)
    Thread(target=w, daemon=True).start()


class App(tk.Frame):
    def __init__(self, master, factor, mapSize, nMines):
        tk.Frame.__init__(self, master, relief="flat", border=5)
        self.factor = factor
        self.mapSize = mapSize
        self.nMines = nMines
        self.load_images()
        self.create_widgets()
        self.new()
        self.near = partial(_near, size=self.mapSize)

    def update_time(self):
        if not self.playing:
            return True
        actualTime = int(get_time() - self.initialTime)
        stringTime = str(min(actualTime, 999)).rjust(3, "0")
        for a, i in enumerate(stringTime):
            self.timeCounter[a].config(image=self.images["n" + i])

    def update_mines(self):
        if self.playing is None:
            return
        mines = self.nMines - len(self.flagged)
        stringMines = str(min(mines, 999)).rjust(3, "0")
        for a, i in enumerate(stringMines):
            self.mineCounter[a].config(image=self.images["n" + i])

    def new(self):
        for cell in self.cells:
            cell.config(image=self.images["_"])
        self.button.config(image=self.images["happy"])
        for i in range(3):
            self.mineCounter[i].config(image=self.images["n0"])
            self.timeCounter[i].config(image=self.images["n0"])
        self.playing = None  # True if playing, False if lost
        self.shown = set()
        self.flagged = set()
        self.interrogated = set()
        self.temporal = set()

    def start(self, cell):
        self.generate(cell)
        self.playing = True
        self.initialTime = get_time()
        timer(self.update_time, 1000)
        self.update_mines()

    def create_widgets(self):
        f = self.factor
        width, height = self.mapSize
        # CREATION
        self.superTopFrame = tk.Frame(self, bd=2 * f, relief="sunken")
        self.topFrame = tk.Frame(self.superTopFrame, bg="gray76", pady=3 * f)
        self.mineFrame = tk.Frame(self.topFrame)
        self.timeFrame = tk.Frame(self.topFrame)
        self.bottomFrame = tk.Frame(self, bd=3 * f, relief="sunken")

        self.button = tk.Label(self.topFrame, bd=0)
        self.mineCounter = [tk.Label(self.mineFrame, bd=0) for _ in range(3)]
        self.timeCounter = [tk.Label(self.timeFrame, bd=0) for _ in range(3)]
        self.cells = [tk.Label(self.bottomFrame, bd=0)
                      for _ in range(mul(*self.mapSize))]
        # WEIGHT CONFIGURE
        for x in range(width):
            self.bottomFrame.columnconfigure(x, weight=1, uniform="same")
        for y in range(height):
            self.bottomFrame.rowconfigure(y, weight=1, uniform="same")
        [self.topFrame.columnconfigure(i, weight=1) for i in range(3)]
        self.columnconfigure(0, weight=1)
        [self.rowconfigure(i, weight=1) for i in range(2)]
        # GRID
        self.superTopFrame.grid(column=0, row=0, sticky="NEW",
                                padx=5 * f, pady=5 * f)
        self.topFrame.pack(expand=True, fill="both")
        self.button.grid(column=1, row=0)
        self.mineFrame.grid(column=0, row=0)
        self.timeFrame.grid(column=2, row=0)
        for i in range(3):
            self.mineCounter[i].grid(column=i, row=0)
            self.timeCounter[i].grid(column=i, row=0)
        self.bottomFrame.grid(column=0, row=1, sticky="NEW",
                              padx=5 * f, pady=5 * f)
        for w in range(width):
            for h in range(height):
                self.cells[w + width * h].grid(column=w, row=h)
        # EVENTS
        self.bind_class("Label", "<ButtonPress-1>", self.lpress)
        self.bind_class("Label", "<ButtonPress-2>", self.mpress)
        self.bind_class("Label", "<ButtonPress-3>", self.rpress)
        self.bind_class("Label", "<B1-Motion>", self.lpress)
        self.bind_class("Label", "<B2-Motion>", self.mpress)
        self.bind_class("Label", "<ButtonRelease-1>", self.lrelease)
        self.bind_class("Label", "<ButtonRelease-2>", self.mrelease)

    def lpress(self, event):
        if self.playing is False:
            return
        self.clean_temporal()
        widget = self.winfo_containing(event.x_root, event.y_root)
        try:
            cell = self.cells.index(widget)
        except ValueError:
            if widget is self.button:
                self.button.config(image=self.images["clicked"])
        else:
            if not (cell in self.shown or cell in self.flagged):
                self.cells[cell].config(image=self.images["0"])
                self.temporal.add(cell)
                self.button.config(image=self.images["undecise"])

    def mpress(self, event):
        if self.playing is False:
            return
        self.clean_temporal()
        widget = self.winfo_containing(event.x_root, event.y_root)
        try:
            cell = self.cells.index(widget)
        except ValueError:
            pass
        else:
            for c in self.near(cell, included=True):
                if not (c in self.shown or c in self.flagged):
                    self.cells[c].config(image=self.images["0"])
                    self.temporal.add(c)
            self.button.config(image=self.images["undecise"])

    def rpress(self, event):
        widget = event.widget
        try:
            cell = self.cells.index(widget)
        except ValueError:
            pass
        else:
            if self.playing:
                if cell in self.flagged:
                    widget.config(image=self.images["i"])
                    self.flagged.remove(cell)
                    self.interrogated.add(cell)
                elif cell in self.interrogated:
                    widget.config(image=self.images["_"])
                    self.interrogated.remove(cell)
                elif (cell not in self.shown and
                      self.nMines > len(self.flagged)):
                    event.widget.config(image=self.images["f"])
                    self.flagged.add(cell)
            self.update_mines()

    def lrelease(self, event):
        self.clean_temporal()
        widget = self.winfo_containing(event.x_root, event.y_root)
        if widget is not event.widget:
            return
        try:
            cell = self.cells.index(widget)
        except ValueError:
            if widget is self.button:
                self.new()
        else:
            if self.playing is False or cell in self.shown:
                return
            if self.playing is None:
                self.start(cell)
            else:
                self.show(cell)

    def mrelease(self, event):
        self.clean_temporal()
        widget = self.winfo_containing(event.x_root, event.y_root)
        if widget is not event.widget or self.playing is None:
            return
        try:
            cell = self.cells.index(widget)
        except ValueError:
            pass
        else:
            cellType = self.map[cell]
            if 0 < cellType < 9 and cell in self.shown:
                near = self.near(cell)
                if cellType == sum(1 for c in near if c in self.flagged):
                    [self.show(c) for c in near]

    def show(self, cell):
        if cell in self.shown or cell in self.flagged:
            return
        self.shown.add(cell)
        cellType = self.map[cell]
        if cellType == 9:
            for a, c in enumerate(self.map):
                if c == 9:
                    if a == cell:
                        self.cells[a].config(image=self.images["r"])
                    elif a not in self.flagged:
                        self.cells[a].config(image=self.images["b"])
                elif a in self.flagged:
                    self.cells[a].config(image=self.images["c"])
            self.button.config(image=self.images["sad"])
            self.playing = False
            return
        self.cells[cell].config(image=self.images[str(cellType)])
        if mul(*self.mapSize) - len(self.shown) == self.nMines:
            self.button.config(image=self.images["cool"])
            self.playing = False
        if cellType == 0:
            [self.show(c) for c in self.near(cell)]

    def generate(self, cell):
        length = mul(*self.mapSize)
        self.map = [0] * length
        nMines = 0
        near = self.near(cell, included=True)
        while nMines < self.nMines:
            rCell = randrange(0, length)  # Choosing mine cells
            if self.map[rCell] != 9 and rCell not in near:
                self.map[rCell] = 9
                nMines += 1
                for c in self.near(rCell):
                    if self.map[c] == 9:
                        continue
                    self.map[c] += 1  # Near cells must count this mine
        self.show(cell)

    def clean_temporal(self):
        for cell in self.temporal:
            if cell in self.interrogated:
                self.cells[cell].config(image=self.images["i"])
            else:
                self.cells[cell].config(image=self.images["_"])
        self.temporal.clear()
        if self.playing is not False:
            self.button.config(image=self.images["happy"])

    def load_images(self):
        self.images = {}
        folderPath = join("cache", str(self.factor), "")
        for name in IMAGE_NAMES:
            self.images[name] = tk.PhotoImage(file=folderPath + name + ".gif")


def run_game(factor, difficulty):
    asTuple = difficulty.split(" ")[:2]
    mapSize = [int(i) for i in asTuple[0].split("x")]
    nMines = int(asTuple[1])
    length = mul(*mapSize)
    if nMines >= length - 9:
        logger.error("There are way too many mines")
        nMines = max(min(length // 5, length - 9), 1)

    root = tk.Tk()
    root.title("Minesweeper")
    root.config(bg="gray76")
    root.resizable(0, 0)
    root.iconbitmap(default=join("media", "icon.ico"))
    rootSize = ((mapSize[0] * 16 + 16) * factor,
                (mapSize[1] * 16 + 26 + 36) * factor)
    x = y = 0
    geometry = "%dx%d+%d+%d" % (*rootSize, x, y)
    root.geometry(geometry)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    app = App(root, factor, mapSize, nMines)
    app.config(bg="gray76", bd=0)
    app.grid(column=0, row=0)
    root.mainloop()

if __name__ == "__main__":
    from main import prepare
    run_game(*prepare())
