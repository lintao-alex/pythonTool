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

        xls_obj = ParseTs.ParseTs(
            xls_full_path, code_dir, cfg_dir)
        xls_obj.extract_class_info(Mark.PATH_PACKAGE_DEFINE)
        xls_obj.extract_game_struct()
        xls_obj.extract_config_file()


if __name__ == '__main__':
    check_xlrd_dir()
    import ParseTs
    main()
