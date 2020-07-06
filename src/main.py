import lizard_parser as lp
import test_generator as tg

def main():
    lines = lp.parse('test/test.lizard')
    info = lp.SourceCodeInfo() # TODO will become dir path and generate lizard file and analyze
    js = info.to_json(lines)

    template = tg.create_template('test/main.template')
    tg.generate_test_code(template,js)

if __name__ == "__main__":
    main()
