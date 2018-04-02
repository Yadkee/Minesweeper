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

logger = getLogger("game")
logger.setLevel(DEBUG)


class App(tk.Frame):
    def __init__(self, master, factor, mapSize, nMines):
        tk.Frame.__init__(self, master, relief="flat", border=5)
        self.factor = factor
        self.mapSize = mapSize
        self.nMines = nMines
        self.load_images()
        self.create_widgets()
        self.new()

    def new(self):
        for cell in self.cells:
            cell.config(image=self.images["_"])
        self.button.config(image=self.images["happy"])
        for i in range(3):
            self.mineCounter[i].config(image=self.images["n0"])
            self.timeCounter[i].config(image=self.images["n0"])

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

    def load_images(self):
        self.images = {}
        folderPath = join("cache", str(self.factor), "")
        for name in IMAGE_NAMES:
            self.images[name] = tk.PhotoImage(file=folderPath + name + ".gif")


def run_game(factor, difficulty):
    asTuple = difficulty.split(" ")[:2]
    mapSize = [int(i) for i in asTuple[0].split("x")]
    nMines = int(asTuple[1])

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
