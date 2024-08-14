import os
from os import stat
from os import walk
import time
import shutil
from icecream import ic
from PIL import Image

ic.enable()

START = os.environ.get("START_DATE")
END = os.environ.get("END_DATE")
MONTH = os.environ.get("MONTH")

while START <= END:
    pass