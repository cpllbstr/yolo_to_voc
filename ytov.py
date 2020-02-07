import mako
import sys
from os import listdir
from os.path import isfile, join


names = []

class Detection():
    __slots__ = (
        "clss",
        "name",
        "x",
        "y",
        "w", 
        "h"
    )
    def __init__(self, yolo_line):
        spl = yolo_line.split(" ")
        self.clss = spl[0]
        self.name = names[int(spl[0])]
        self.x = spl[0]
        self.y = spl[1]
        self.w = spl[2]
        self.h = spl[3]


if __name__ == "__main__":
    # if len(sys.argv) < 4:
        # print("Usage: python ytov.py /path/to/yolo/data /path/to/yolo/names /output/path")
    yolo_data_folder = sys.argv[1]
    # yolo_names_path = sys.argv[2]
    names = open(sys.argv[2]).readlines()
    # output_folder = sys.argv[3]



    yolo_files = [f for f in listdir(yolo_data_folder) if isfile(join(yolo_data_folder, f))]

    res = {}

    for filename in yolo_files:
        file = open(yolo_data_folder +"/"+ filename)
        content = file.readlines()
        dets = []
        for line in content:
            dets.append(Detection(line))
        res[filename] = dets
    



