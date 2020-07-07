import lizard_parser as lp
import generator as g
import template
import parameter

def main():
    parameter.load_args()

    lines = lp.parse('test/test.lizard')
    info = lp.SourceCodeInfo() # TODO will become dir path and generate lizard file and analyze
    js = info.to_json(lines)

    temp = template.create(parameter.get('template'))
    g.to_testcode(temp,js)

if __name__ == "__main__":
    main()
