# -*- coding: utf-8 -*-

import json
import os
from . import template
from . import testcode
from . import merge
from . import lizard_adapter
from . import parameter


def execute():
    parameter.load_args()
    js = lizard_adapter.parse(parameter.get("source"))
    template_tokens = template.parse(parameter.get("template"))
    __to_testcode(template_tokens, js)


def __to_testcode(template_tokens, data_objects):
    for data_object in data_objects:
        dstfilepath = data_object["dstfilepath"]
        already_exist = os.path.isfile(dstfilepath)
        if already_exist:
            if parameter.get("nomerge"):
                continue
            elif parameter.get("overwrite"):
                __write_testcode(dstfilepath, template_tokens, data_object["testdata"])
            else:
                old_data_obj = testcode.parse_file(dstfilepath)
                data_object = merge.merge(data_object, old_data_obj)
                __write_testcode(dstfilepath, template_tokens, data_object["testdata"])
        else:
            __write_testcode(dstfilepath, template_tokens, data_object["testdata"])


def __write_testcode(filepath, template_tokens, data_object):
    # create directory, if not exist
    dstdirpath = os.path.dirname(filepath)
    os.makedirs(dstdirpath, exist_ok=True)

    out = open(filepath, mode="w")
    d = template.to_code(template_tokens, data_object)
    out.write(d)
