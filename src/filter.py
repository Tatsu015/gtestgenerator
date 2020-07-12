# -*- coding: utf-8 -*-

import json
import parameter
import re

def is_export(data_obj):
    if __is_constructor(data_obj):
        return False

    if __is_destructor(data_obj):
        return False

    if __is_main_function(data_obj):
        return False

    if not __is_exclude(data_obj):
        return False

    if data_obj['ccn'] < parameter.get('ccn'):
        return False

    if data_obj['nloc'] < parameter.get('nloc'):
        return False

    return True


def __is_constructor(data_obj):
    if data_obj['class'] == data_obj['function']:
        return True
    else:
        return False

def __is_destructor(data_obj):
    if '~'+data_obj['class'] == data_obj['function']:
        return True
    else:
        return False

def __is_main_function(data_obj):
    if 'main' == data_obj['function']:
        return True
    else:
        return False

def __is_exclude(data_obj):
    exclude = parameter.get('exclude')
    if exclude:
        for exclude in parameter.get('exclude'):
            repattern = re.compile(exclude)
            if repattern.search(data_obj['path']):
                return False

    return True