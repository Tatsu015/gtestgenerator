# -*- coding: utf-8 -*-

import os
import re

def parse_file(filepath):
    f = open(filepath, 'r')
    d = f.read()
    root_obj = {}

    root_obj['filepath'] = '' # TODO
    root_obj['dstfilepath'] = filepath
    root_obj['testdata'] = __parse_testdata(d)

    return root_obj

def __parse_testdata(testdata):
    testdata_obj = {}
    testdata_obj['includepath'] = __parse_includepath(testdata)
    testdata_obj['classes'] = ____parse_classes(testdata)

    return testdata_obj

def __parse_includepath(testdata):
    includefiles_obj = []
    for includefile in __extract_includefiles(testdata):
        filepath_obj = {'filepath':includefile}
        includefiles_obj.append(filepath_obj)

    return includefiles_obj

def ____parse_classes(testdata):
    classes_obj = []
    for testfixture in __extract_testfixtures(testdata):
        classes_obj.append(__parse_class(testfixture))

    return classes_obj

def __parse_class(testfixture):
    class_obj = {}
    class_obj['classname'] = __extract_class_name(testfixture)
    class_obj['fixturebody'] = __extract_testfixture_class_body(testfixture)
    class_obj['func'] = __parse_functions(testfixture)

    return class_obj

def __parse_functions(testfixture):
    func_objs = []
    for testcase in __extract_testcases(testfixture):
        func_obj = {
            'funcname':__extract_test_name(testcase),
            'body':__extract_test_body(testcase),
            'nloc':'',
            'ccn':''
        }
        func_objs.append(func_obj)

    return func_objs

def __extract_includefiles(testdata):
    includefiles = []
    for line in testdata.splitlines():
        if '#include' in line:
            tmp = line.replace('#include','').strip()
            includefile = tmp.replace('"','').replace('<', '').replace('>', '')
            if 'gtest.h' not in includefile and 'gmock.h' not in includefile:
                includefiles.append(includefile)
    return includefiles

def __extract_testfixtures(testdata):
    tmp = re.split(r'class\s',testdata)
    return tmp[1:]

def __extract_testfixture_class(testfixture):
    tmp = re.split('TEST_F|TEST', testfixture)
    return tmp[0]

def __extract_class_name(testfixture):
    tmp = testfixture.split(':')[0]
    tmp = tmp.strip().replace('_test', '')
    return tmp

def __extract_testfixture_class_body(testfixture):
    re_body = re.compile(r'(?<=\{\n).+(?=\n^\};)', flags=(re.MULTILINE | re.DOTALL))
    match_body = re_body.search(testfixture)
    return match_body.group()

def __extract_testcases(testfixture):
    tmp = re.split('TEST_F|TEST', testfixture)
    return tmp[1:]

def __extract_test_name(testcase):
    re_name = re.compile(r'(?<=\()[^\(\)]+(?=\))')
    match_names = re_name.search(testcase)
    return match_names.group().split(',')[1].strip()

def __extract_test_body(testcase):
    re_body = re.compile(r'(?<=\{).+(?=\})', flags=(re.MULTILINE | re.DOTALL))
    match_body = re_body.search(testcase)
    return match_body.group()
