from mako import template
import sys
import argparse
import imagesize
from os import listdir, mkdir
from os.path import isfile, split, abspath

parser = argparse.ArgumentParser(description='Convert YOLO dataset to Pascal VOC.')
parser.add_argument('--data', metavar='/yolo/dataset', type=str,
                    help='path to images and notations')
parser.add_argument('--notes', metavar='/yolo/notes', type=str,
                    help='if notes are separate to images, then use this argument to define path to notes')
parser.add_argument('--out', metavar='/out/dir', type=str,
                    help='output directory')

names = []

class Detection():
    def __init__(self, path, width, height):
        folder, self.filename = split(path)
        self.folder = split(folder)[1]
        self.path = abspath(path)
        self.width = width
        self.height = height
        self.folder = folder
        self.path = path
        self.objects = []

    def add_object(self, yolo_line):
        self.objects.append(Object(yolo_line, self.width, self.height))
       

class Object:
    def __init__(self, yolo_line, img_width, img_height):
        self.name, x, y, w, h = yolo_line.split(" ")  
        self.xmin = (float(x)-float(w)/2)*img_width
        self.xmax = (float(x)+float(w)/2)*img_width
        self.ymin = (float(y)-float(h)/2)*img_height
        self.ymax = (float(y)+float(h)/2)*img_height

if __name__ == "__main__":
    args = parser.parse_args()
    yolo_data_folder = args.data
    yolo_txt_p = args.notes if args.notes is not None else args.data
    out_path = args.out if args.out is not None else "./output"
    try:
        mkdir(out_path)
    except Exception as e:
        print ("Creation of the directory %s failed" % out_path)
        print ("Error:", e)

    yolo_img = [img for img in listdir(yolo_data_folder) if (img.split(".")[1] == "jpg" or img.split(".")[1] == "png" or img.split(".")[1] == "jpeg" )]

    res = []
    for filename in yolo_img:
        txt_path = yolo_txt_p +"/"+ filename.split(".")[0]+".txt"
        img_path = yolo_data_folder+"/"+filename
        try:
            note = open(txt_path)
        except Exception as e:
            print("Error:", e)
            continue
        content = note.readlines()
        w, h = imagesize.get(img_path)
        _, folder = split(yolo_data_folder)
        dets = Detection(img_path , w, h)
        for line in content:
            dets.add_object(line)
        res.append(dets)
    
    i = 0
    allr= len(res)
    for r in res:
        tmp = template.Template(filename="voc_template.xml")
        ready = int(25*i/allr)
        print("\r [" ,"="*(ready+1), " "*(25-ready-1), end="]")
        i+=1
        f = open(out_path + "/" + r.filename.split(".")[0] + ".xml", "w+")
        f.write(tmp.render_unicode(data=r))
        f.close()

    print()
            

    



