# -*- coding: utf-8 -*-

from gtestgenerator import lizard_parser as lp
from gtestgenerator import generator as g
from gtestgenerator import template_parser as tp
from gtestgenerator import parameter

def main():
    parameter.load_args()
    js = lp.parse(parameter.get('source'))
    template_tokens = tp.parse(parameter.get('template'))
    g.to_testcode(template_tokens,js)

if __name__ == "__main__":
    main()
