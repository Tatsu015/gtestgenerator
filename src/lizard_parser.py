# -*- coding: utf-8 -*-

import re
import os
import json
import parameter
import filter as obj_filter

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

def __trimmed(data):
    DERIMITA = '-----------------------------------\n'
    tmp = data.split(DERIMITA)
    table_data = re.split(r"\d+ file analyzed.", tmp[1])

    return table_data[0]

def parse(file_path):
    f = open(file_path, 'r')
    table_data = __trimmed(f.read())

    lines = []
    for line in table_data.splitlines():
        obj = __line_to_object(line)
        if obj_filter.is_export(obj):
            lines.append(obj)

    return lines

class SourceCodeInfo:
    def __init__(self):
        self.__files = []

    def to_json(self, lines):
        for line in lines:
            self.__line_to_json(line)

        return self.__files

    def __line_to_json(self, line):
        #　use file basename insted class name
        # because function (not method) has no class name
        file_name = line['path']
        dst_filepath = file_name.replace('.cpp', '_test.cpp').replace('./','./' + parameter.get('destination') + '/')
        class_name = line['class']
        if class_name == '':
            class_name = line['basename']
        func_name = line['function']

        hit_files = [x for x in self.__files if x['filepath'] == file_name]
        if len(hit_files) != 0:
            classes = [d.get('testdata').get('classes') for d in hit_files][0]
            hit_classes = [x for x in classes if x['classname'] == class_name]
            if len(hit_classes) != 0:
                cls = hit_classes[0]
                fncs = [d.get('func') for d in classes][0]
                fnc = [x for x in fncs if x['funcname'] == func_name]

                # append suffix index to same function name,
                # because override function name duplicatable.
                index = 1
                str_index = ''
                while fnc:
                    index = index + 1
                    str_index = str(index)
                    fnc = [x for x in fncs if x['funcname'] == (func_name + str_index)]

                cls['func'].append({'funcname':(func_name + str_index),'body':'','nloc':line['nloc'],'ccn':line['ccn']})
            else:
                classes.append({'classname':class_name,'func':[{'funcname':line['function'],'body':'','nloc':line['nloc'],'ccn':line['ccn']}]})
        else:
            self.__files.append({
                'filepath':file_name,
                'dstfilepath':dst_filepath,
                'testdata':{
                    'includepath':[
                        {'filepath':line['basename']+'.h'}
                    ],
                    'classes':[
                        {'classname':class_name,'func':[{'funcname':line['function'],'body':'','nloc':line['nloc'],'ccn':line['ccn']}
                        ]}
                    ]
                }
            })


    def dump(self):
        print(json.dumps(self.__files,indent=1))
