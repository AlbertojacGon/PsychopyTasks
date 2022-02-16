#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 02:28:03 2017

@author: albertogonzalezv
"""

import os
from PIL import Image

os.chdir("/Users/albertogonzalezv/Desktop/files/psychopy/elahe_tabary_tasks/picture_naming/round2/")

pngs = []
jpgs = []
for filei in os.listdir(os.getcwd()):
    if filei.endswith(".png"):
        pngs.append(filei)

for idx, filei in enumerate(pngs):
        img = Image.open(filei)
        img = Image.open(pngs[idx])
        img.save((filei[0:7]+ str(idx+61) +'.png'))
