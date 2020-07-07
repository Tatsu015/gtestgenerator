# -*- coding: utf-8 -*-

import json
import os

def to_testcode(template,data_objects):
    for data_object in data_objects:
        dstfilepath = data_object["dstfilepath"]
        dstdirpath = os.path.dirname(dstfilepath)
        os.makedirs(dstdirpath, exist_ok=True)

        out = open(dstfilepath,mode='w')
        d = template.to_code(data_object["testdata"])
        out.write(d)
