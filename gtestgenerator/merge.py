# -*- coding: utf-8 -*-

import json


def merge(new_data_obj, old_data_obj):
    merged_obj = {}
    merged_obj["filepath"] = new_data_obj["filepath"]
    merged_obj["dstfilepath"] = old_data_obj["dstfilepath"]
    merged_obj["testdata"] = __merge_testdata(
        new_data_obj["testdata"], old_data_obj["testdata"]
    )
    return merged_obj


def __merge_testdata(new_testdata_obj, old_testdata_obj):
    merged_obj = {}
    merged_obj["includepaths"] = old_testdata_obj["includepaths"]
    merged_obj["classes"] = __merge_classes(
        new_testdata_obj["classes"], old_testdata_obj["classes"]
    )
    return merged_obj


def __merge_classes(new_classes_obj, old_classes_obj):
    merged_objs = []
    for new_class_obj in new_classes_obj:
        classname = new_class_obj["classname"]
        tmp = [x for x in old_classes_obj if x["classname"] == classname]
        # old classes already has new class
        if tmp:
            old_class_obj = tmp[0]
            merged_class_obj = __merge_class(new_class_obj, old_class_obj)
            merged_objs.append(merged_class_obj)
        # old classes not has new class
        else:
            merged_objs.append(new_class_obj)
    return merged_objs


def __merge_class(new_class_obj, old_class_obj):
    merged_obj = {}
    merged_obj["classname"] = new_class_obj["classname"]
    merged_obj["fixturebody"] = old_class_obj["fixturebody"]
    merged_obj["functions"] = __merge_functions(
        new_class_obj["functions"], old_class_obj["functions"]
    )
    return merged_obj


def __merge_functions(new_functions_obj, old_functions_obj):
    merged_objs = []
    for new_function_obj in new_functions_obj:
        funcname = new_function_obj["functionname"]
        tmp = [x for x in old_functions_obj if x["functionname"] == funcname]
        # old functions already has new function
        if tmp:
            old_function_obj = tmp[0]
            merged_function_obj = __merge_function(new_function_obj, old_function_obj)
            merged_objs.append(merged_function_obj)
        # old functions not has new function
        else:
            merged_objs.append(new_function_obj)
    return merged_objs


def __merge_function(new_function_obj, old_function_obj):
    merged_obj = {}
    merged_obj["functionname"] = new_function_obj["functionname"]
    merged_obj["testbody"] = old_function_obj["testbody"]
    merged_obj["nloc"] = new_function_obj["nloc"]
    merged_obj["ccn"] = new_function_obj["ccn"]
    return merged_obj
