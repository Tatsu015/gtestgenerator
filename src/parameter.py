# -*- coding: utf-8 -*-

import json
import argparse

__parameter = {}

def load_args():
    parser = argparse.ArgumentParser(description='xxx')
    parser.add_argument('--ccn', type=int,default=0)
    parser.add_argument('--nloc', type=int,default=0)
    parser.add_argument('-s','--source', type=str,default='.')
    parser.add_argument('-d','--destination', type=str,default='testcode')
    parser.add_argument('--template', type=str,default='./conf/main.template')
    parser.add_argument('-f','--file', type=str,default='')

    args = parser.parse_args()

    __parameter['ccn'] = args.ccn
    __parameter['nloc'] = args.nloc
    __parameter['source'] = args.source
    __parameter['destination'] = args.destination
    __parameter['template'] = args.template

def get(key):
    return __parameter[key]

def parse_file(filepath):
    pass
