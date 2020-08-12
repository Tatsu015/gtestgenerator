# -*- coding: utf-8 -*-

import json
import re
import merge
import condition


class _Token:
    def __init__(self):
        pass

    def _append_val_key(self, s):
        return "${" + s + "}"

    def _strip_val_key(self, s):
        return s.replace("$", "").replace("{", "").replace("}", "")

    def _replace_str_datas(self, s, data_obj):
        tmp = s
        for k, v in data_obj.items():
            if type(v) is str:
                tmp = tmp.replace(self._append_val_key(k), v)
        return tmp


class _LeafToken(_Token):
    def __init__(self, data):
        super().__init__()
        self.__data = data

    def to_code(self, data_obj):
        d = self.__data
        d = self._replace_str_datas(d, data_obj)
        return d


class _IfToken(_Token):
    def __init__(self, condition, true_child_token, false_child_token):
        super().__init__()
        self.__condition = condition
        self.__true_child_token = true_child_token
        self.__false_child_token = false_child_token

    def to_code(self, data_obj):
        d = ""
        child = None
        if self.__condition.check(data_obj):
            child = self.__false_child_token
        else:
            child = self.__true_child_token
        d = child.to_code(data_obj)
        d = self._replace_str_datas(d, data_obj)
        return d


class _ForeachToken(_Token):
    def __init__(self, condition, children):
        super().__init__()
        self.__condition = condition
        self.__children = children

    def to_code(self, data_obj):
        d = ""
        condition = self._strip_val_key(self.__condition)
        for i in data_obj[condition]:
            for child in self.__children:
                d = d + child.to_code(i)

        d = self._replace_str_datas(d, data_obj)
        return d


def parse(filepath):
    # TODO this tokens will read from main.template
    tokens = [
        _LeafToken(
            "#include <gtest/gtest.h>\n"
            "\n"
            "#define private public\n"
            "#define protected public\n\n"
        ),
        _ForeachToken("${includepaths}", [_LeafToken('#include "${filepath}"')]),
        _LeafToken("\n\n" "using namespace ::testing;\n" "\n"),
        _ForeachToken(
            "${classes}",
            [
                _LeafToken("class ${classname}_test : public ::testing::Test {\n"),
                _IfToken(
                    condition.MergeCondition(),
                    _LeafToken(
                        "protected:\n"
                        "  virtual void SetUp() {\n"
                        "  }\n"
                        "  virtual void TearDown() {\n"
                        "  }\n"
                    ),
                    _LeafToken("${fixturebody}\n"),
                ),
                _LeafToken("};\n\n"),
                _ForeachToken(
                    "${functions}",
                    [
                        _IfToken(
                            condition.MergeCondition(),
                            _LeafToken(
                                "TEST_F(${classname}_test, ${functionname}) {\n" "}\n\n"
                            ),
                            _LeafToken(
                                "TEST_F(${classname}_test, ${functionname}) {\n"
                                "${testbody}"
                                "}\n\n"
                            ),
                        )
                    ],
                ),
            ],
        ),
    ]
    return tokens


def to_code(tokens, data_obj):
    d = ""
    for t in tokens:
        d = d + t.to_code(data_obj)
    return d
