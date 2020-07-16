# -*- coding: utf-8 -*-

import json
import argparse

__parameter = {}

def load_args():
    parser = argparse.ArgumentParser(description='Automatically generate google test skeleton from c++ source code')
    parser.add_argument('--ccn', type=int,default=0,help='Generate skeletons only for functions greater than the specified cyclomatic complexity')
    parser.add_argument('--nloc', type=int,default=0,help='Generate skeletons only for functions greater than the specified line count')
    parser.add_argument('-s','--source', type=str,default='.',help='Specify the source code directory for skeleton generation')
    parser.add_argument('-d','--destination', type=str,default='testcode',help='Specify the skeleton output destination directory')
    parser.add_argument('--template', type=str,default='./conf/testcode.template',help='Specify the skeleton template file')
    parser.add_argument('-f','--file', type=str,default='',help='Load parameters from specify file')
    parser.add_argument('--exclude', type=str,default='',nargs='*',help='Exclude spacify source file name')

    args = parser.parse_args()

    __parameter['ccn'] = args.ccn
    __parameter['nloc'] = args.nloc
    __parameter['source'] = args.source
    __parameter['destination'] = args.destination
    __parameter['template'] = args.template
    __parameter['exclude'] = args.exclude

def get(key):
    return __parameter[key]

def parse_file(filepath):
    pass
