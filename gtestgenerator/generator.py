# -*- coding: utf-8 -*-

import json
import os
from gtestgenerator import template_parser as tp
from gtestgenerator import test_code_parser as tcp
from gtestgenerator import merge as mg
from gtestgenerator import lizard_parser as lp
from gtestgenerator import parameter


def execute():
    parameter.load_args()
    js = lp.parse(parameter.get('source'))
    template_tokens = tp.parse(parameter.get('template'))
    __to_testcode(template_tokens,js)

def __to_testcode(template_tokens,data_objects):
    for data_object in data_objects:
        dstfilepath = data_object["dstfilepath"]
        already_exist = os.path.isfile(dstfilepath)
        if already_exist:
            old_data_obj = tcp.parse_file(dstfilepath)
            data_object = mg.merge(data_object, old_data_obj)
        else:
            dstdirpath = os.path.dirname(dstfilepath)
            os.makedirs(dstdirpath, exist_ok=True)

        out = open(dstfilepath,mode='w')
        d = tp.to_code(template_tokens, data_object["testdata"])
        out.write(d)
