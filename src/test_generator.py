# -*- coding: utf-8 -*-

import json
import re

class Component:
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
                            t = t.replace(self.append_val_key(k), v)
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
                    c = Component()
                    c.__body = sp["before"]
                    self.__child_components.append(c)

            if sp["target"] is not '':
                c = Component()
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
            "key":self.strip_val_key(key),
            "before":s[:ms.start()],
            "target":tmp[1: me.start()],
            "after":tmp[me.end():].rstrip()
            }

    def strip_val_key(self,s):
        return s.replace('$','').replace('{','').replace('}','')

    def append_val_key(self,s):
        return '${' + s + '}'

    def exist_variable(self,s):
        if '$' in s:
            return True
        else:
            return False

f = open('test/main.template', 'r')
template = f.read()
t = Component()
t.analyze(template)

jd=open('test/data.json', 'r')
data = json.loads(jd.read())

for dt in data:
    d = t.to_code(dt["testdata"])
    out = open(dt["filepath"],mode='w')
    out.write(d)

