#! python3
"""This script splits sprites.gif into 3 animated gifs"""
from os.path import join
from PIL import Image
SPRITES_PATH = join("media", "sprites.gif")
SPR = Image.open(SPRITES_PATH)
NAMES = tuple("012345678bcrif_") + ("n0", "n1", "n2", "n3", "n4", "n5", "n6",
                                    "n7", "n8", "n9", "clicked", "happy",
                                    "undecise", "sad", "cool")


def generate_images(factor=1):
    """Every image will be resized by a factor of 'factor'"""
    filePath = join("cache", str(factor), "")
    limits = ((0, 0, 144, 16, 16, 16), (0, 16, 96, 32, 16, 16),
              (0, 32, 128, 55, 13, 23), (0, 55, 128, 78, 26, 26))
    images = []
    a = 0
    for box in limits:
        w, h = box[4], box[5]
        newSize = (int(w * factor), int(h * factor))
        for y in range(*box[1::2]):
            for x in range(*box[::2]):
                cropped = SPR.crop((x, y, x + w, y + h))
                if factor != 1:
                    resized = cropped.resize(newSize)
                else:
                    resized = cropped
                images.append(resized)
                a += 1
    for name, img in zip(NAMES, images):
        img.save(filePath + name + ".gif")
    # Do the same for the menu image
    menuPath = join("media", "menu.gif")
    img = Image.open(menuPath)
    w, h = img.size
    newSize = (int(w * factor), int(h * factor))
    resized = img.resize(newSize)
    resized.save(filePath + "menu.gif")

if __name__ == "__main__":
    generate_images()
