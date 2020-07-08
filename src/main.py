# -*- coding: utf-8 -*-

import lizard_parser as lp
import generator as g
import template_parser as tp
import parameter

def main():
    parameter.load_args()

    lines = lp.parse('test/test.lizard')
    info = lp.SourceCodeInfo() # TODO will become dir path and generate lizard file and analyze
    js = info.to_json(lines)

    template = tp.parse(parameter.get('template'))
    g.to_testcode(template,js)

if __name__ == "__main__":
    main()
