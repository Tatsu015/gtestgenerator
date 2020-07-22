# -*- coding: utf-8 -*-

import re
import os
import json
import parameter
import filter as obj_filter
import subprocess

def parse(path):
    res = subprocess.check_output(['lizard', path])
    table_data = __extract_function_part(res.decode())

    lines = []
    for line in table_data.splitlines():
        obj = __line_to_object(line)
        if obj_filter.is_export(obj):
            lines.append(obj)

    jsn = __to_code(lines)
    return jsn

def __class_and_function(data):
    if '::' in data:
        tmp = data.split('::')
        return {'class':tmp[0], 'function':tmp[1]}
    else:
        return {'class':'', 'function':data}

def __basename(path):
    tmp = os.path.basename(path)
    tmp = tmp.split('.')[0]
    return tmp

def __line_to_object(line):
    elms = list(filter(lambda a: a != "",line.split(' ')))

    locationElms = elms[5].split('@')
    cls_and_func = __class_and_function(locationElms[0])
    lineinfos = locationElms[1].split('-')

    obj = {
        'nloc':int(elms[0]),
        'ccn':int(elms[1]),
        'token':int(elms[2]),
        'param':int(elms[3]),
        'length':int(elms[4]),
        'class':cls_and_func['class'],
        'function':cls_and_func['function'],
        'startline':lineinfos[0],
        'endline':lineinfos[1],
        'path':locationElms[2],
        'basename': __basename(locationElms[2])
    }

    return obj

def __extract_function_part(data):
    DERIMITA = '-----------------------------------\n'
    tmp = data.split(DERIMITA)
    table_data = re.split(r"\d+ file analyzed.", tmp[1])

    return table_data[0]

def __to_code(line_objs):
    root = []
    for line_obj in line_objs:
        if not __has_file(root, line_obj):
            root.append(__to_file(line_obj))
            continue

        classname = line_obj['class']
        if classname == '':
            classname = line_obj['basename']

        testdata_obj = __extract_testdata_obj(root, line_obj['path'])
        classes_obj = __extract_classes_obj(testdata_obj)
        if not __has_class(classes_obj, classname):
            classes_obj.append(__to_class(line_obj))
            continue

        class_obj = __extract_class_obj(classes_obj,classname)
        funcs_obj = __extract_funcs_obj(class_obj, line_obj['function'])
        if not __has_func(funcs_obj, line_obj['function']):
            funcs_obj.append(__to_func(line_obj))
            continue

        funcs_obj.append(__to_overrided_func(funcs_obj,line_obj))

    return root

def __has_file(target_obj, line_obj):
    filepath = line_obj['path']
    hit_files = [x for x in target_obj if x['filepath'] == filepath]
    if hit_files:
        return True
    else:
        return False

def __to_file(line_obj):
    filepath = line_obj['path']
    dstfilepath = filepath.replace('.cpp', '_test.cpp').replace('./','./' + parameter.get('destination') + '/')
    include_filepath = line_obj['basename']+'.h'

    classname = line_obj['class']
    if classname == '':
        classname = line_obj['basename']

    funcname = line_obj['function']
    nloc = line_obj['nloc']
    ccn = line_obj['ccn']

    file_obj = {
                'filepath':filepath,
                'dstfilepath':dstfilepath,
                'testdata':{
                    'includepath':[
                        {'filepath':include_filepath}
                    ],
                    'classes':[
                        {
                            'classname':classname,
                            'fixturebody':'',
                            'func':[
                                {
                                    'funcname':funcname,
                                    'body':'',
                                    'nloc':nloc,
                                    'ccn':ccn
                                }
                            ]
                        }
                    ]
                }
            }
    return file_obj

def __extract_testdata_obj(target_obj, filepath):
    hit_files = [x for x in target_obj if x['filepath'] == filepath]
    if hit_files:
        return hit_files[0]['testdata']
    else:
        return None

def __extract_classes_obj(testdata_obj):
    return testdata_obj['classes']

def __has_class(classes_obj, classname):
    hit_classes = [x for x in classes_obj if x['classname'] == classname]
    if hit_classes:
        return True
    else:
        return False

def __to_class(line_obj):
    classname = line_obj['class']
    if classname == '':
        classname = line_obj['basename']

    obj = {
        'classname':classname,
        'fixturebody':'',
        'func':[
            {
                'funcname':line_obj['function'],
                'body':'',
                'nloc':line_obj['nloc'],
                'ccn':line_obj['ccn']
            }
        ]
    }

    return obj

def __extract_class_obj(classes_obj, classname):
    hit_classes = [x for x in classes_obj if x['classname'] == classname]
    if hit_classes:
        return hit_classes[0]
    else:
        return None

def __has_func(funcs_obj, funcname):
    hit_funcs = [x for x in funcs_obj if x['funcname'] == funcname]
    if hit_funcs:
        return True
    else:
        return False

def __to_func(line_obj):
    obj = {
        'funcname':line_obj['function'],
        'body':'',
        'nloc':line_obj['nloc'],
        'ccn':line_obj['ccn']
    }

    return obj

def __to_overrided_func(funcs_obj, line_obj):
    func_name = line_obj['function']

    func_obj = [x for x in funcs_obj if x['funcname'] == func_name]

    # append suffix index to same function name,
    # because override function name duplicatable.
    index = 1
    str_index = ''
    while func_obj:
        index = index + 1
        str_index = str(index)
        func_obj = [x for x in funcs_obj if x['funcname'] == (func_name + str_index)]

    obj = {
        'funcname':(func_name + str_index),
        'body':'',
        'nloc':line_obj['nloc'],
        'ccn':line_obj['ccn']
    }

    return obj

def __extract_funcs_obj(class_obj, funcname):
    return class_obj['func']
