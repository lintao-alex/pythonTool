import subprocess
import os
import sys
import re

NAME_SPACE = 'protolist'
JS_MARK = r'(function($protobuf)'


def main():
    out_dir = os.path.join('..', '..', 'yjqz', 'libs', 'proto')
    js_file_path = os.path.join(out_dir, 'protolist.js')
    ts_file_path = os.path.join(out_dir, 'protolist.d.ts')
    if os.path.exists(js_file_path):
        os.remove(js_file_path)
    if os.path.exists(ts_file_path):
        os.remove(ts_file_path)

    input_dir = sys.argv[1]
    print(input_dir)
    common_str = r"pbjs %s -t static-module -w closure" % input_dir
    common_str += r" --no-verify --no-delimited --no-create --no-convert"
    js_content = get_cli_out(common_str)
    js_content = js_content.replace(
        JS_MARK, r'var %s = %s' %
        (NAME_SPACE, JS_MARK), 1)
    with open(js_file_path, 'w', -1, 'utf8') as js_file:
        js_file.write(js_content)
    print('write file to: ' + js_file_path)

    common_str = r"pbts %s" % js_file_path
    common_str += r" --no-comments"
    ts_content = get_cli_out(common_str)
    ts_content = re.sub(
        r'import \* as \$protobuf from .*;\n',
        r'import $protobuf = protobuf;\nimport Long = protobuf.Long;\n\ndeclare namespace %s{' % NAME_SPACE,
        ts_content) + r'}'
    with open(ts_file_path, 'w', -1, 'utf8') as ts_file:
        ts_file.write(ts_content)
    print('write file to: ' + ts_file_path)


def get_cli_out(common_str):
    child_process = subprocess.Popen(
        common_str, shell=True, stdout=subprocess.PIPE)
    buffer_reader = child_process.stdout
    out = buffer_reader.read().decode('ascii')
    buffer_reader.close()
    return out


if __name__ == '__main__':
    main()
