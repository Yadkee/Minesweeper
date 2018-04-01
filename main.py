#! python3
from logging import (
    basicConfig,
    getLogger,
    DEBUG)
from os.path import (
    join,
    exists)
from json import load

basicConfig(format="%(asctime)s [%(levelname)s] %(name)s - %(message)s")
logger = getLogger("Minesweeper")
logger.setLevel(DEBUG)


def show_error(msg):
    logger.error(msg)
    input("Press enter to exit . . .\n")
    raise Exception(msg)

# Launch waiting screen

if not exists("media"):
    show_error("There is no media folder!")
# Load multiplicator factor from config.json
with open("config.json") as f:
    factor = int(load(f)["factor"])  # I'm not acepting floats
folderPath = join("cache", str(factor))
# Create cache for this factor
if not exists(folderPath):
    from os import mkdir
    mkdir(folderPath)
    hasPil = True
    if factor != 1:
        # Check if Pillow is installed (this may also recognise PIL but I
        #  trust the users and think that they've correctly read dependencies)
        try:
            from PIL import Image
        except ImportError:
            hasPil = False
            logger.warning("Pillow is not instaled")
    # Copying from default
    if factor == 1 or not hasPil:
        from generate_images import NAMES as names
        from shutil import copyfile
        if factor != 1:
            logger.warning("You chose a different size but Pillow is not"
                           "installed. Default size is going to be used")
        sourcePath = join("media", "default", "")
        destPath = join(folderPath, "")
        for name in names:
            copyfile(sourcePath + name, destPath + name)
        logger.info("Cached images from default")
    else:  # Generate images
        from generate_images import generate_images
        generate_images(factor)
        logger.info("Cached images for a factor of %d" % factor)
# Launch the game with the factor parameter