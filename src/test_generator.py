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
    def __init__(self, loopable):
        self.__loopable = loopable
        self.__loop_array_key = []
        self.__body = ""
        self.__child_components = []

    def to_code(self,data):
        buf = self.__body

        if len(self.__loop_array_key) > 0:
            # branch
            for ary_key in self.__loop_array_key:
                for ary_val in data[ary_key]:
                    for conponent in self.__child_components:
                        child_data = conponent.to_code(ary_val)
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

    def __split_loop_keyword(self, s):
        LOOP_KEY = "$$FOREACH"
        ms = re.search(re.escape(LOOP_KEY) + r'.*', s)
        if ms is None:
            return {
            "before":s,
            "target":"",
            "after":""
            }

        key = ms.group().split(' ')[1]

        tmp = s[ms.end():]
        me = re.search(r'\$\$NEXT ' + re.escape(key), tmp)

        return {
            "before":s[:ms.start() - 1],   # -1 means remove return code
            "target":tmp[1: me.start()-1], #  1,-1 means remove return code
            "after":tmp[me.end() + 1:]     # +1 means remove return code
            }

    def analyze(self,data):
        sp = self.__split_loop_keyword(data)
        if sp["before"] is not '':
            c = Component(False)
            c.__body = sp["before"]
            self.__child_components.append(c)

        if sp["target"] is not '':
            c = Component(True)
            c.analyze(sp["target"])
            self.__child_components.append(c)

        if sp["after"] is not '':
            c = Component(False)
            c.analyze(sp["after"])
            self.__child_components.append(c)

    def dump(self):
        if self.__body is not '':
            print('>>>>>>>>>')
            print(self.__body)
        for a in self.__child_components:
            a.dump()

        if self.__body is not '':
            print('<<<<<<<<<')


        # LOOP_KEY = "$$FOREACH"


        # # ms = re.search(re.escape(LOOP_KEY) + r'.*', data)
        # # key = ms.group().split(' ')[1]

        # # tmp = data[ms.end():]
        # # me = re.search(r'\$\$NEXT ' + re.escape(key), tmp)

        # remain = data[me.end():]

        # if LOOP_KEY in remain:




        # search_word = '$$FOREACH'
        # foreach_elms = [(i, line) for i, line in enumerate(data.splitlines()) if search_word in line]

        # if len(foreach_elms) > 0:
        #     keyword = foreach_elms[0][1].replace(search_word, '').strip()

        #     start = data.find('$$FOREACH ' + keyword + '\n')
        #     end = data.find('$$NEXT ' + keyword+ '\n')
        #     start_size = len('$$FOREACH ' + keyword+ '\n')
        #     end_size = len('$$NEXT ' + keyword+ '\n')

        #     self.__loop_array_key.append(strip_val_key(keyword))
        #     self.__body = data[:start] + data[end+end_size:]

        #     test_case = Component()
        #     self.__child_components.append(test_case)

        #     loop_array_keysentence = data[start+start_size:end]
        #     test_case.analyze(loop_array_keysentence)
        # else:
        #     self.__body = data

f = open('test/main.template', 'r')
template = f.read()
t = Component(False)
t.analyze(template)

# t.dump()

jd=open('test/data.json', 'r')
data = json.loads(jd.read())

for i in data:
    d = t.to_code(i)
print(d)

