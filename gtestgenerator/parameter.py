# -*- coding: utf-8 -*-

import os
import json
import argparse
import pathlib

__parameter = {}

def get(key):
    global __parameter
    return __parameter[key]

def load_args():
    args = __setup_argument()
    __setup_default_parameter(args)

    if args.init:
        __export_default_config()
        exit(0)

    path = __find_config(os.getcwd())
    if path:
        f = open(path, 'r')
        global __parameter
        __parameter = json.loads(f.read())
    else:
        print('Cannot find .gigconfig file. Use default value.')

    if args.debug:
        print(__parameter)

def __setup_argument():
    parser = argparse.ArgumentParser(description='Automatically generate google test skeleton from c++ source code')

    parser.add_argument(
        '-i',
        '--init',
        help='Generate google test generator config file',
        action='store_true')

    parser.add_argument(
        '-s',
        '--source',
        type=str,
        default='.',
        help='Specify the source code directory for skeleton generation')

    parser.add_argument(
        '-d',
        '--destination',
        type=str,
        default='testcode',
        help='Specify the skeleton output destination directory')

    parser.add_argument(
        '--ccn',
        type=int,
        default=0,
        help='Generate skeletons only for functions greater than the specified cyclomatic complexity')

    parser.add_argument(
        '--nloc',
        type=int,
        default=0,
        help='Generate skeletons only for functions greater than the specified line count')

    parser.add_argument(
        '--template',
        type=str,
        default='../etc/gtestgenerator/testcode.template',
        help='Specify the skeleton template file')

    parser.add_argument(
        '--config',
        type=str,
        default='',
        help='Load configuration from specify file')

    parser.add_argument(
        '--exclude',
        type=str,
        default='',
        nargs='*',
        help='Exclude spacify source file name')

    parser.add_argument(
        '--debug',
        help='Show debug infomation',
        action='store_true')

    args = parser.parse_args()
    return args

def __setup_default_parameter(args):
    global __parameter
    __parameter['ccn'] = args.ccn
    __parameter['nloc'] = args.nloc
    __parameter['source'] = args.source
    __parameter['destination'] = args.destination
    __parameter['template'] = args.template
    __parameter['exclude'] = args.exclude

def __export_default_config():
    global __parameter
    f = open('.gtgconfig','w')
    parameter = {
        'ccn':__parameter['ccn'],
        'nloc':__parameter['nloc'],
        'source':__parameter['source'],
        'destination':__parameter['destination'],
        'template':__parameter['template'],
        'exclude':__parameter['exclude']
    }
    json.dump(parameter, f, indent=4)


def __find_config(currentpath):
    pos = currentpath.rfind('/')

    while pos != 0:
        configpath = currentpath + '/.gtgconfig'
        if os.path.exists(configpath):
            return configpath

        currentpath = currentpath[:pos]
        pos = currentpath.rfind('/')


    return ''

