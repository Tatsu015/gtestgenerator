# -*- coding: utf-8 -*-

import json
import parameter

def is_export(data_obj, parent_obj):
    if 'funcname' not in data_obj:
        return True

    if __is_constructor(data_obj, parent_obj):
        return False

    if __is_destructor(data_obj, parent_obj):
        return False

    if data_obj['ccn'] < parameter.get('ccn'):
        return False

    if data_obj['nloc'] < parameter.get('nloc'):
        return False

    return True


def __is_constructor(data_obj, parent_obj):
    if parent_obj['classname'] == data_obj['funcname']:
        return True
    else:
        return False

def __is_destructor(data_obj, parent_obj):
    if '~'+parent_obj['classname'] == data_obj['funcname']:
        return True
    else:
        return False