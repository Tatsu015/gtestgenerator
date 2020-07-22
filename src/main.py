# -*- coding: utf-8 -*-

import lizard_parser as lp
import generator as g
import template_parser as tp
import parameter

def main():
    parameter.load_args()
    js = lp.parse(parameter.get('source'))
    template_tokens = tp.parse(parameter.get('template'))
    g.to_testcode(template_tokens,js)

if __name__ == "__main__":
    main()
