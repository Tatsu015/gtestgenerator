# -*- coding: utf-8 -*-

import json
import os
import template_parser as tp

def to_testcode(template_tokens,data_objects):
    for data_object in data_objects:
        dstfilepath = data_object["dstfilepath"]
        already_exist = os.path.isfile(dstfilepath)
        need_merge = False
        if already_exist:
            need_merge = True
        else:
            dstdirpath = os.path.dirname(dstfilepath)
            os.makedirs(dstdirpath, exist_ok=True)

        out = open(dstfilepath,mode='w')
        d = tp.to_code(template_tokens, data_object["testdata"], need_merge)
        out.write(d)
