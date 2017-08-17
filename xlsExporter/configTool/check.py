import re
import zlib
def main():
    test = 'enter_limit$byte~limit_type;int~limit_data[]'
    reg = re.compile(r'(\w+)\$([\w~;]+)\[]')
    b = reg.match(test)


if __name__ == '__main__':
    main()
