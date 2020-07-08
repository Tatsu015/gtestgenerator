# -*- coding: utf-8 -*-

import json
import re

class _Component:
    def __init__(self):
        self.__loop_key = ''
        self.__body = ''
        self.__childlen = []

    def to_code(self,data_obj):
        buf = self.__body

        for child in self.__childlen:
            loop_key = child.__loop_key
            tmp = ''
            if loop_key is not '':
                for loop_key_obj in data_obj[loop_key]:
                    t = child.to_code(loop_key_obj)
                    for k,v in loop_key_obj.items():
                        if type(v) == str:
                            t = t.replace(self._append_val_key(k), v)
                    tmp = tmp + t
            else:
                tmp = child.to_code(data_obj)

            buf = buf + tmp

        return buf

    def analyze(self,data_obj):
        remain_obj = data_obj
        while remain_obj is not '':
            splited_obj = self.__split_loop_keyword(remain_obj)
            if splited_obj["before"] is not '':
                if self.__loop_key is not '':
                    self.__body = splited_obj["before"]
                else:
                    c = _Component()
                    c.__body = splited_obj["before"]
                    self.__childlen.append(c)

            if splited_obj["target"] is not '':
                c = _Component()
                c.analyze(splited_obj["target"])
                c.__loop_key = splited_obj["key"]
                self.__childlen.append(c)

            remain_obj = splited_obj["after"]

    def __split_loop_keyword(self, s):
        LOOP_KEY = "$$FOREACH"
        before_loop = re.search(re.escape(LOOP_KEY) + r'.*', s)
        if before_loop is None:
            return {
            "before":s,
            "target":'',
            "after":''
            }

        key = before_loop.group().split(' ')[1]

        after_loop = s[before_loop.end():]
        after_next = re.search(r'\$\$NEXT ' + re.escape(key), after_loop)

        return {
            "key":self._strip_val_key(key),
            "before":s[:before_loop.start()],
            "target":after_loop[1: after_next.start()],
            "after":after_loop[after_next.end():].rstrip()
            }

    def _strip_val_key(self,s):
        return s.replace('$','').replace('{','').replace('}','')

    def _append_val_key(self,s):
        return '${' + s + '}'

def parse(filepath):
    t = _Component()

    f = open(filepath, 'r')
    d = f.read()
    t.analyze(d)

    return t