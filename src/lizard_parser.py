# -*- coding: utf-8 -*-

import re
import os

def __class_and_function(data):
    if '::' in data:
        tmp = data.split('::')
        return {'class':tmp[0], 'function':tmp[1]}
    else:
        return {'class':None, 'function':data}

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

def __trimmed(data):
    DERIMITA = '-----------------------------------\n'
    tmp = data.split(DERIMITA)
    table_data = re.split(r"\d+ file analyzed.", tmp[1])

    return table_data[0]

def parse(file_path):
    f = open(file_path, 'r')
    table_data = __trimmed(f.read())

    ls = []
    for line in table_data.splitlines():
        obj = __line_to_object(line)
        print(obj)
        ls.append(obj)

    return ls

parse('test.lizard')