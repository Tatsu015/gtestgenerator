# -*- coding: utf-8 -*-

import json
import re

def strip_val_key(s):
    return s.replace('$','').replace('{','').replace('}','')

def append_val_key(s):
    return '${' + s + '}'

def exist_variable(s):
    if '$' in s:
        return True
    else:
        return False
    # return re.match(r"\$\{.*?\}",s)


class Component:
    def __init__(self):
        self.__loop_array_key = []
        self.__body = ""
        self.__child_components = []

    def dump(self,data):
        buf = self.__body

        if len(self.__loop_array_key) > 0:
            # branch
            for ary_key in self.__loop_array_key:
                for ary_val in data[ary_key]:
                    for conponent in self.__child_components:
                        child_data = conponent.dump(ary_val)
                        for k, v in data.items():
                            var_k = append_val_key(k)
                            if var_k in child_data:
                                child_data = child_data.replace(var_k, v)
                        buf = buf + child_data
        else:
            # leaf
            for k, v in data.items():
                var_k = append_val_key(k)
                if var_k in buf:
                    buf = buf.replace(var_k, v)
            return buf

        return buf

    def analyze(self,data):
        search_word = '$$FOREACH'
        foreach_elms = [(i, line) for i, line in enumerate(data.splitlines()) if search_word in line]

        if len(foreach_elms) > 0:
            keyword = foreach_elms[0][1].replace(search_word, '').strip()

            start = data.find('$$FOREACH ' + keyword + '\n')
            end = data.find('$$NEXT ' + keyword+ '\n')
            start_size = len('$$FOREACH ' + keyword+ '\n')
            end_size = len('$$NEXT ' + keyword+ '\n')

            self.__loop_array_key.append(strip_val_key(keyword))
            self.__body = data[:start] + data[end+end_size:]

            test_case = Component()
            self.__child_components.append(test_case)

            loop_array_keysentence = data[start+start_size:end]
            test_case.analyze(loop_array_keysentence)
        else:
            self.__body = data

f = open('../test/main.template', 'r')
template = f.read()
t = Component()
t.analyze(template)

jd=open('../test/data.json', 'r')
data = json.loads(jd.read())

for i in data:
    d = t.dump(i)
print(d)

