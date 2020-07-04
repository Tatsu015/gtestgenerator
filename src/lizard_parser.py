# -*- coding: utf-8 -*-

import re
import os
import json

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
        lines.append(obj)

    return lines

class SourceCodeManager:
    def __init__(self):
        self.__files = []

    def to_json(self, line):
        #　use file basename insted class name
        # because function (not method) has no class name
        class_name = line['class']
        if class_name == '':
            class_name = line['basename']
        func_name = line['function']

        filepathes = [d.get('filepath') for d in self.__files]
        if line['path'] in filepathes:
            classes = [d.get('testdata').get('classes') for d in self.__files][0]
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

                cls['func'].append({'funcname':(func_name + str_index),'body':''})
            else:
                classes.append({'classname':class_name,'func':[{'funcname':line['function'],'body':''}]})
        else:
            self.__files.append({
                'filepath':line['path'],
                'testdata':{
                    'includepath':[
                        {'filepath':line['basename']+'.h'}
                    ],
                    'classes':[
                        {'classname':class_name,'func':[{'funcname':line['function'],'body':''}
                        ]}
                    ]
                }
            })

    def dump(self):
        print(json.dumps(self.__files,indent=1))

lines = parse('test/test.lizard')
m = SourceCodeManager()
for line in lines:
    m.to_json(line)

m.dump()
