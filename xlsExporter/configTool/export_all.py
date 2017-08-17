import sys
import os
import shutil
import Mark


def check_xlrd_dir():
    try:
        import xlrd
    except ImportError:
        xlrd_dir = os.path.realpath(__file__)
        xlrd_dir = os.path.abspath(
            os.path.join(
                xlrd_dir,
                os.pardir,
                os.pardir))
        sys.path.append(xlrd_dir)


def make_sure_out_dir(out_dir, with_child):
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    if with_child:
        os.mkdir(
            os.path.join(
                out_dir,
                Mark.PATH_PACKAGE_DEFINE))


def main():
    xls_dir = sys.argv[1]
    code_dir = sys.argv[2]
    cfg_dir = sys.argv[3]
    code_dir = os.path.join(code_dir, Mark.PATH_PACKAGE)
    cfg_dir = os.path.join(cfg_dir, Mark.PATH_CONFIG_PACKAGE)

    make_sure_out_dir(code_dir, True)
    make_sure_out_dir(cfg_dir, False)

    if '-s' in sys.argv:
        import ParseTsS
        parse_obj = ParseTsS.ParseTsS()
    else:
        import ParseTs
        parse_obj = ParseTs.ParseTs()

    for file_name in os.listdir(xls_dir):
        # check xls file
        if file_name[0] == '~':
            continue
        xls_full_path = os.path.join(xls_dir, file_name)
        if not os.path.isfile(xls_full_path):
            continue
        ext_name = os.path.splitext(file_name)[1]
        if ext_name != '.xls' and ext_name != '.xlsx':
            continue

        print('start deal file: %s' % file_name)

        parse_obj.reset(xls_full_path, code_dir, cfg_dir)
        parse_obj.extract_define_class()
        parse_obj.extract_game_class()
        parse_obj.record_config_stream()

    parse_obj.extract_class_collection_file()
    if '-c' in sys.argv:
        parse_obj.extract_compress_configs()  # 合并压缩
    else:
        parse_obj.extract_config_dat_list()  # 散开不压缩


if __name__ == '__main__':
    check_xlrd_dir()
    main()
