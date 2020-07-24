# -*- coding: utf-8 -*-

import json
import os
from gtestgenerator import template
from gtestgenerator import testcode
from gtestgenerator import merge
from gtestgenerator import lizard_adapter
from gtestgenerator import parameter


def execute():
    parameter.load_args()
    js = lizard_adapter.parse(parameter.get('source'))
    template_tokens = template.parse(parameter.get('template'))
    __to_testcode(template_tokens,js)

def __to_testcode(template_tokens,data_objects):
    for data_object in data_objects:
        dstfilepath = data_object["dstfilepath"]
        already_exist = os.path.isfile(dstfilepath)
        if already_exist:
            old_data_obj = testcode.parse_file(dstfilepath)
            data_object = merge.merge(data_object, old_data_obj)
        else:
            dstdirpath = os.path.dirname(dstfilepath)
            os.makedirs(dstdirpath, exist_ok=True)

        out = open(dstfilepath,mode='w')
        d = template.to_code(template_tokens, data_object["testdata"])
        out.write(d)
