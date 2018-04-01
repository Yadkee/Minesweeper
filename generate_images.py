#! python3
"""This script splits sprites.gif into 3 animated gifs"""
from os.path import join
from PIL import Image
SPRITES_PATH = join("media", "sprites.gif")
CACHE_PATH = join("cache", "")
SPR = Image.open(SPRITES_PATH)


def generate_images(factor=1):
    """Every image will be resized by a factor of 'factor'"""
    groups = ([], [], [])
    names = ("cell", "number", "face")
    indexes = (0, 0, 1, 2)
    limits = ((0, 0, 144, 16, 16, 16), (0, 16, 96, 32, 16, 16),
              (0, 32, 128, 55, 13, 23), (0, 55, 128, 78, 26, 26))
    for a, box in zip(indexes, limits):
        w, h = box[4], box[5]
        for y in range(*box[1::2]):
            for x in range(*box[::2]):
                cropped = SPR.crop((x, y, x + w, y + h))
                if factor != 1:
                    resized = cropped.resize((w * factor, h * factor))
                else:
                    resized = cropped
                groups[a].append(resized)
    for name, group in zip(names, groups):
        n = name == "number"  # There is a weird transparency error in number
        img = group[0 - 2 * n]
        with open(CACHE_PATH + name + ".gif", "wb") as f:
            img.save(f, save_all=True, append_images=group[1 - n:])

if __name__ == "__main__":
    generate_images()
