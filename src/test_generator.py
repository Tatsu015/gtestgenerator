# -*- coding: utf-8 -*-

import json
import re
import os

class _Component:
    def __init__(self):
        self.__loop_key = ''
        self.__body = ''
        self.__child_components = []

    def to_code(self,data):
        buf = self.__body

        for child in self.__child_components:
            key = child.__loop_key
            tmp = ''
            if key is not '':
                for e in data[key]:
                    t = child.to_code(e)
                    for k,v in e.items():
                        if type(v) == str:
                            t = t.replace(self._append_val_key(k), v)
                    tmp = tmp + t
            else:
                tmp = child.to_code(data)

            buf = buf + tmp

        return buf

    def analyze(self,data):
        tmp = data
        while tmp is not '':
            sp = self.__split_loop_keyword(tmp)
            if sp["before"] is not '':
                if self.__loop_key is not '':
                    self.__body = sp["before"]
                else:
                    c = _Component()
                    c.__body = sp["before"]
                    self.__child_components.append(c)

            if sp["target"] is not '':
                c = _Component()
                c.analyze(sp["target"])
                c.__loop_key = sp["key"]
                self.__child_components.append(c)

            tmp = sp["after"]

    def __split_loop_keyword(self, s):
        LOOP_KEY = "$$FOREACH"
        ms = re.search(re.escape(LOOP_KEY) + r'.*', s)
        if ms is None:
            return {
            "before":s,
            "target":'',
            "after":''
            }

        key = ms.group().split(' ')[1]

        tmp = s[ms.end():]
        me = re.search(r'\$\$NEXT ' + re.escape(key), tmp)

        return {
            "key":self._strip_val_key(key),
            "before":s[:ms.start()],
            "target":tmp[1: me.start()],
            "after":tmp[me.end():].rstrip()
            }

    def _strip_val_key(self,s):
        return s.replace('$','').replace('{','').replace('}','')

    def _append_val_key(self,s):
        return '${' + s + '}'

def create_template(filepath):
    t = _Component()

    f = open(filepath, 'r')
    d = f.read()
    t.analyze(d)

    return t


def generate_test_code(template,data_objects):

    print(data_objects)

    for data_object in data_objects:
        dstfilepath = data_object["dstfilepath"]
        dstdirpath = os.path.dirname(dstfilepath)
        os.makedirs(dstdirpath, exist_ok=True)

        out = open(dstfilepath,mode='w')
        d = template.to_code(data_object["testdata"])
        out.write(d)
