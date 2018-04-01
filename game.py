#! python3
from logging import (
    getLogger,
    DEBUG)
import tkinter as tk
from os.path import join
from generate_images import NAMES as IMAGE_GROUPS

logger = getLogger("game")
logger.setLevel(DEBUG)


class App(tk.Frame):
    def __init__(self, master, factor, mapSize, nMines):
        tk.Frame.__init__(self, master, relief="flat", border=5)
        self.factor = factor
        self.mapSize = mapSize
        self.nMines = nMines
        self.load_images()

    def load_images(self):
        self.images = {}
        folderPath = join("cache", str(self.factor), "")
        for name in IMAGE_GROUPS:
            self.images[name] = tk.PhotoImage(folderPath + name)

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
    app = App(root, factor, mapSize, nMines)
    app.grid(column=0, row=0)
    root.mainloop()

if __name__ == "__main__":
    from main import prepare
    run_game(*prepare())
