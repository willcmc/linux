#! /usr/bin/env python3

# definitions:

data_dir = "./data"
img_dir = "./img"
gnuplot_dir = "./gnuplot"

data = dict()
f = dict()

#files should have a commented header with variable name

data["IAS"] = "data/ias.txt"
data["M"] = "data/mach.txt"
data["h"] = "data/height.txt"
data["TAS"] = "data/tas.txt"
data["d"] = "data/dist.txt"

gp_prefix = "plotter-"
gp_suffix = ".p"

pathIn= img_dir+"/"
vid_name = 'A320.avi'
fps = 90

# imports

import re
import sys
import cv2
import numpy as np
import os
from os.path import isfile, join

# For running bash script from python
def run_script(script, stdin=None):
    import subprocess

    proc = subprocess.Popen(['bash', '-c', script],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        stdin=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode:
        raise ScriptException(proc.returncode, stdout, stderr, script)
    return stdout, stderr

class ScriptException(Exception):
    def __init__(self, returncode, stdout, stderr, script):
        self.returncode = returncode
        self.stdout = stdout.decode("utf-8")
        self.stderr = stderr.decode("utf-8")
        Exception().__init__('Error in script')

def list_files(path):
    from os import listdir
    return listdir(path)

def convert_frames_to_video(pathIn,pathOut,fps):
    frame_array = []
    files = [z for z in os.listdir(pathIn) if isfile(join(pathIn, z))]
    #for sorting the file names properly
    files.sort(key = lambda y: int(y[4:-4]))
    files = files[1::5]
    for i in range(len(files)):
        filename=pathIn + files[i]
        #reading each files
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        print(filename)
        #inserting the frames into an image array
        frame_array.append(img)
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()

# start of code

#finding out how many lines in files

size = None
for key, value in data.items():
    if size is None: size = sum(1 for line in open(value, "r"))
    elif size != sum(1 for line in open(value, "r")):
        raise ValueError("Provided data files do not have same length")
        exit()
print(size-1, "entries found")
count = 0
for i in range(1, size):
    if (i%5): continue
    fname = gnuplot_dir + "/" + gp_prefix + str(i) + gp_suffix
    fhand = open(fname, "w")
    fhand.write("""
set terminal pngcairo enhanced font \"LM-Roman-10, 30\" size 2048, 2048

set tmargin 1
set bmargin 1
set lmargin 17
set rmargin 17


set style line 1 lc rgb '#E41A1C' pt 1 ps 1 lt 1 lw 2 # red
set style line 2 lc rgb '#377EB8' pt 6 ps 1 lt 1 lw 2 # blue
set style line 3 lc rgb '#4DAF4A' pt 2 ps 1 lt 1 lw 2 # green
set style line 4 lc rgb '#984EA3' pt 3 ps 1 lt 1 lw 2 # purple
set style line 5 lc rgb '#FF7F00' pt 4 ps 1 lt 1 lw 2 # orange
set style line 6 lc rgb '#FFFF33' pt 5 ps 1 lt 1 lw 2 # yellow
set style line 7 lc rgb '#A65628' pt 7 ps 1 lt 1 lw 2 # brown
set style line 8 lc rgb '#F781BF' pt 8 ps 1 lt 1 lw 2 # pink

set palette maxcolors 8
set palette defined ( 0 '#E41A1C', 1 '#377EB8', 2 '#4DAF4A', 3 '#984EA3',\
4 '#FF7F00', 5 '#FFFF33', 6 '#A65628', 7 '#F781BF' )

set tics out nomirror
unset xtics

set style line 12 lc rgb '#808080' lt 0 lw 1
set grid back ls 12
unset grid

set output \"img/img-""" + str(i) + """.png\"
set origin 0,0
unset key
set autoscale
set multiplot layout 4,1 title \"A320 Climb Profile\" margins 0.15,0.9,0.1,0.95 spacing 0,0
set tics out nomirror
unset xtics

unset xlabel
set ylabel \"Altitude (km)\"
set yrange [0:14]
set xrange [0:390]
set ytic 2,2,12
set arrow 1 from 0,1.524 to 390,1.524 nohead dt 2
set arrow 2 from 0,4.572 to 390,4.572 nohead dt 2
set arrow 3 from 0,7.3152 to 390,7.3152 nohead dt 2
set arrow 4 from 0,10.6680 to 390,10.6680 nohead dt 2

set label 1 "I" at 350,0.9 center tc rgb "gray"
set label 2 "II" at 350,3 center tc rgb "gray"
set label 3 "III" at 350,6 center tc rgb "gray"
set label 4 "IV" at 350,9 center tc rgb "gray"
set label 5 "V" at 350,12 center tc rgb "gray"

plot \"<join """ + data["h"] +" "+ data["d"] + """\" using 3:2 every ::1::""" + str(i) + """ w l ls 2

unset arrow 1
unset arrow 2
unset arrow 3
unset arrow 4

unset label 1
unset label 2
unset label 3
unset label 4
unset label 5

unset xlabel
set ylabel \"TAS (km/h)\"
set yrange [200:950]
set xrange [0:390]
set ytic 300,200,900
plot \"<join """ + data["TAS"] +" "+ data["d"] + """\" using 3:2 every ::1::""" + str(i) + """ w l ls 3

unset xlabel
set ylabel \"IAS (km/h)\"
set yrange [200:650]
set xrange [0:390]
set ytic 200,100,600
plot \"<join """ + data["IAS"] +" "+ data["d"] + """\" using 3:2 every ::1::""" + str(i) + """ w l ls 4

set xlabel \"Distance (km)\"
set ylabel \"Mach Number\"
set yrange [0.25:0.9]
set xrange [0:390]
set ytic 0.2,0.1,0.8
set xtics nomirror
plot \"<join """ + data["M"] +" "+ data["d"] + """\" using 3:2 every ::1::""" + str(i) + """ w l ls 5

unset multiplot
    """)
    fhand.close()

    run_script("gnuplot " + fname);

# Plotting
convert_frames_to_video(pathIn, vid_name, fps)
