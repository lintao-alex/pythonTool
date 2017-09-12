import re
import os
import zlib
import xlrd
import Mark
import utils
import ByteArray
import errorChecker
import struct
import reutils


class ParseXls(object):
    __total_class_list = []  # 记录解析出了哪些类
    __config_collection_dict = {}
    __error_info = errorChecker.ErrorInfo()
    __array_re = re.compile(r'(.+)\[]$')
    __define_re = re.compile(r'(\w+)\$([\w~;]+)\[]')
    __game_class_property_declare_list_re = re.compile(
        Mark.MARK_PROPERTY_DECLARE_LIST +
        r'(\s*)(.*)\s*' +
        Mark.MARK_VECTOR_DECLARE_MODE +
        r'(.*)')
    __multiple_line_pattern = r'\s*' + Mark.MARK_MULTIPLE_LINE_FORMAT_BEGIN + \
        r'([\s\S]*)' + Mark.MARK_MULTIPLE_LINE_FORMAT_END
    __game_class_parse_sentence_re = re.compile(
        Mark.MARK_PARSE_SENTENCE_LIST +
        r'(\s*)(.*)' +
        __multiple_line_pattern +
        __multiple_line_pattern +
        __multiple_line_pattern)

    # methods tobe override
    def _get_game_class_templet_str(self):
        pass

    def _get_define_class_templet_str(self):
        pass

    def _get_class_collection_templet_str(self):
        pass

    def _get_file_extension_name(self):
        pass

    def _get_line_note_mark(self):
        pass

    def _init_type_map(self, map_obj):
        pass

    def _init_type_fuc_map(self, map_obj):
        pass

    def __init__(self):
        # data type in different language
        self.__type_map = {}
        self._init_type_map(self.__type_map)
        # data parse function in different language
        self.__type_fuc_map = {}
        self._init_type_fuc_map(self.__type_fuc_map)

        self.__xls_full_path_name = ''
        self.__xls_file_name = ''
        self.__code_dest_path = ''
        self.__cfg_dest_path = ''
        self.__out_class_name = ''

        self.__type_list = []  # 可能是ClassInfo或ArrayInfo
        self.__proxy_define_list = []  # 筛选出的ClassInf子集
        self.__property_list = []  # 字段名
        self.__desc_list = []
        self.__values_list = []  # 注意这是二维数组
        self.__org_column_index_list = []  # 为数据错误精确定位

    def reset(self, xls_full_path, code_dest_path, cfg_dest_path):
        # 只做必要数据初始化与错误检查
        self.__xls_full_path_name = xls_full_path
        self.__xls_file_name = os.path.basename(xls_full_path)
        self.__code_dest_path = code_dest_path
        self.__cfg_dest_path = cfg_dest_path

        self.__type_list.clear()
        self.__proxy_define_list.clear()
        self.__property_list.clear()
        self.__desc_list.clear()
        self.__values_list.clear()
        self.__org_column_index_list.clear()

        work_book = xlrd.open_workbook(self.__xls_full_path_name)
        work_sheet = work_book.sheet_by_index(0)

        self.__error_info.file_name = self.__xls_file_name
        class_name = str(work_sheet.cell_value(0, 0))
        self.__error_info.check_value(class_name)
        self.__out_class_name = utils.beautify_formation(class_name, True)
        self.__error_info.check_class_name(self.__out_class_name)

        for col_index in range(0, work_sheet.ncols):
            work_cols = work_sheet.col_values(col_index, 1, 5)
            if ParseXls.need_care(work_cols[0]):
                self.__error_info.column_index = col_index
                type_name = work_cols[2]
                self.__error_info.row_index = 3
                self.__error_info.check_value(type_name)
                type_name = str(type_name).lower()
                property_name = work_cols[3]
                self.__error_info.row_index = 4
                self.__error_info.check_value(property_name)
                property_name = str(property_name)
                desc_str = str(work_cols[1])
                value_cols = work_sheet.col_values(
                    col_index, 5, work_sheet.nrows)
                if utils.is_split_case(type_name):  # 拆解成多列
                    in_type_list = type_name.split(';')
                    in_ppt_list = property_name.split(';')
                    in_len = len(in_type_list)
                    self.__error_info.check_equal_count(
                        len(in_ppt_list), in_len)
                    in_v_map = []
                    for in_i, in_v in enumerate(value_cols):
                        self.__error_info.row_index = 5 + in_i
                        if isinstance(in_v, float):
                            in_v_list = list(range(in_len))
                        else:
                            in_v_list = in_v.split('_')
                            self.__error_info.check_equal_count(
                                len(in_v_list), in_len)
                        in_v_map.append(in_v_list)
                    self.__error_info.row_index = 4
                    for in_i, in_type in enumerate(in_type_list):
                        value_split = [in_v_list[in_i]
                                       for in_v_list in in_v_map]
                        self.__append_export(
                            in_type, utils.beautify_formation(
                                in_ppt_list[in_i]), desc_str, value_split)
                else:
                    self.__error_info.row_index = 3
                    def_match = self.__define_re.match(type_name)
                    if def_match is not None:  # 自定义类
                        cl_name = utils.beautify_formation(
                            def_match.group(1), True)
                        self.__error_info.check_define_name(cl_name)
                        def_cl = ClassInfo(cl_name)
                        cl_desc = def_match.group(2)
                        for prop in cl_desc.split(';'):
                            cl_t_p = prop.split('~')
                            def_cl.type_list.append(cl_t_p[0])
                            def_cl.property_list.append(
                                utils.beautify_formation(cl_t_p[1]))
                        self.__append_export(
                            def_cl, utils.beautify_formation(property_name), desc_str, value_cols)
                        self.__proxy_define_list.append(def_cl)
                    else:
                        array_match = self.__array_re.match(type_name)
                        self.__error_info.row_index = 3
                        if array_match is not None:
                            base_type = array_match.group(1)
                            array_match2 = self.__array_re.match(base_type)
                            if array_match2 is not None:
                                base_type = array_match2.group(1)
                                base_type = ArrayInfo(base_type, 2)
                            else:
                                base_type = ArrayInfo(base_type, 1)
                        else:
                            base_type = type_name
                            if type_name not in self.__type_map:
                                self.__error_info.alert_type_err(type_name)
                        self.__append_export(
                            base_type,
                            utils.beautify_formation(property_name),
                            desc_str,
                            value_cols)

    def __append_export(self, type_obj, property_name, desc_str, values):
        self.__error_info.row_index = 4
        self.__error_info.check_repeat_value(
            property_name, self.__property_list, '字段名')
        self.__type_list.append(type_obj)
        self.__property_list.append(property_name)
        self.__desc_list.append(desc_str)
        self.__values_list.append(values)
        self.__org_column_index_list.append(self.__error_info.column_index)

    def __replace_game_class_property(self, matched):
        split_str = matched.group(1)
        declare_str = matched.group(2)
        list_mode_str = matched.group(3)
        content_list = []
        for index, type_obj in enumerate(self.__type_list):
            if isinstance(type_obj, ClassInfo):
                out_type = list_mode_str.replace(
                    Mark.MARK_PROPERTY_TYPE, type_obj.name)
            elif isinstance(type_obj, ArrayInfo):
                out_type = list_mode_str
                if type_obj.dimension == 2:
                    out_type = out_type.replace(
                        Mark.MARK_PROPERTY_TYPE, list_mode_str)
                out_type = out_type.replace(
                    Mark.MARK_PROPERTY_TYPE, self.__type_map[type_obj.type_name])
            else:
                out_type = self.__type_map[type_obj]
            one_property = declare_str.replace(
                Mark.MARK_PROPERTY_NAME,
                self.__property_list[index])
            one_property = one_property.replace(
                Mark.MARK_PROPERTY_TYPE, out_type)
            content_list.append(
                self._get_line_note_mark() +
                self.__desc_list[index].replace(
                    '\n',
                    ''))
            content_list.append(one_property)
        return split_str.join(content_list)

    def __replace_game_class_sentence(self, matched):
        split_str1 = matched.group(1)
        single_property_str = matched.group(2)
        define_property_str = matched.group(3)
        array_property_str = matched.group(4)
        array2_property_str = matched.group(5)
        content_list = []
        for index, type_obj in enumerate(self.__type_list):
            prop_str = self.__property_list[index]
            if isinstance(type_obj, ClassInfo):
                one_property = define_property_str.replace(
                    Mark.MARK_PROPERTY_NAME, prop_str)
                one_property = one_property.replace(
                    Mark.MARK_PROPERTY_TYPE, type_obj.name)
            else:
                if isinstance(type_obj, ArrayInfo):
                    base_type = type_obj.type_name
                    if type_obj.dimension == 2:
                        one_property = array2_property_str
                    else:
                        one_property = array_property_str
                else:
                    base_type = type_obj
                    one_property = single_property_str
                one_property = one_property.replace(
                    Mark.MARK_PROPERTY_NAME, prop_str)
                one_property = one_property.replace(
                    Mark.MARK_PARSE_FUNCTION_NAME, self.__type_fuc_map[base_type])
            content_list.append(one_property)
        return split_str1.join(content_list)

    # game data class
    def extract_game_class(self):
        content_str = self._get_game_class_templet_str()
        content_str = content_str.replace(
            Mark.MARK_SOURCE_TABLE,
            self.__xls_file_name)  # 注明数据来源
        content_str = content_str.replace(Mark.MARK_PACKAGE, Mark.PATH_PACKAGE)
        content_str = reutils.es_import_declare_list.sub(
            reutils.def_one_mark_list(
                Mark.MARK_CLASS_NAME,
                self.__proxy_define_list,
                'name'),
            content_str)
        content_str = content_str.replace(
            Mark.MARK_PACKAGE_DEFINE,
            Mark.PATH_PACKAGE_DEFINE)  # 替换import时会引入新的MARK_PACKAGE_DEFINE,所以在其后再作替换
        content_str = content_str.replace(
            Mark.MARK_CLASS_NAME, self.__out_class_name)
        content_str = self.__game_class_property_declare_list_re.sub(
            self.__replace_game_class_property, content_str)  # 字段申明
        content_str = self.__game_class_parse_sentence_re.sub(
            self.__replace_game_class_sentence, content_str)  # 赋值

        class_file_path_name = os.path.join(
            self.__code_dest_path,
            self.__out_class_name) + "." + self._get_file_extension_name()
        self.__total_class_list.append(self.__out_class_name)
        with open(class_file_path_name, 'w', -1, 'utf8') as class_file:
            class_file.write(content_str)
        print('write file to: ' + class_file_path_name)

    # the inner class defined by sponsor
    def extract_define_class(self):
        for define_class in self.__proxy_define_list:
            content_str = self._get_define_class_templet_str()
            content_str = content_str.replace(
                Mark.MARK_CLASS_NAME, define_class.name)
            content_str = content_str.replace(
                Mark.MARK_PACKAGE, Mark.PATH_PACKAGE)
            content_str = content_str.replace(
                Mark.MARK_PACKAGE_DEFINE, Mark.PATH_PACKAGE_DEFINE)
            content_str = reutils.property_declare_list.sub(
                reutils.def_two_mark_list(
                    Mark.MARK_PROPERTY_NAME,
                    define_class.property_list,
                    Mark.MARK_PROPERTY_TYPE,
                    define_class.type_list,
                    None,
                    self.__type_map),
                content_str)
            content_str = reutils.parse_sentence_list.sub(
                reutils.def_two_mark_list(
                    Mark.MARK_PROPERTY_NAME,
                    define_class.property_list,
                    Mark.MARK_PARSE_FUNCTION_NAME,
                    define_class.type_list,
                    None,
                    self.__type_fuc_map),
                content_str)

            class_file_name = os.path.join(
                self.__code_dest_path,
                Mark.PATH_PACKAGE_DEFINE,
                define_class.name) + '.' + self._get_file_extension_name()
            with open(class_file_name, 'w', -1, 'utf8') as fp:
                fp.write(content_str)
            print('write file to: ' + class_file_name)

    def record_config_stream(self):
        stream_obj = ByteArray.ByteArray()
        ParseXls.__config_collection_dict[self.__out_class_name] = stream_obj
        stream_obj.write_utf(self.__out_class_name)
        data_num = len(self.__values_list[0])
        stream_obj.write_unsigned_short(data_num)
        for value_index in range(data_num):
            self.__error_info.row_index = value_index + 5
            for ppt_index, ppt_name in enumerate(self.__property_list):
                self.__error_info.column_index = self.__org_column_index_list[ppt_index]
                type_obj = self.__type_list[ppt_index]
                value = self.__values_list[ppt_index][value_index]
                if isinstance(type_obj, ClassInfo):
                    if isinstance(value, float):
                        stream_obj.write_unsigned_byte(0)
                        continue
                    prop_num = len(type_obj.property_list)
                    obj_arr = value.split(';')
                    obj_arr = [not_empty for not_empty in obj_arr if not_empty]  # 去掉空项
                    stream_obj.write_unsigned_byte(len(obj_arr))
                    for obj_str in obj_arr:
                        prop_values = obj_str.split('_')
                        self.__error_info.check_equal_count(
                            len(prop_values), prop_num)
                        for prop_index, prop_value in enumerate(
                                prop_values):
                            self.write_base_type(
                                type_obj.type_list[prop_index], prop_value, stream_obj)
                else:
                    if isinstance(type_obj, ArrayInfo):
                        # 到这一步的应该是字符串，除非策划填的是0，被xlrd读成了0.0
                        if isinstance(value, float):
                            value = '0'
                        if type_obj.dimension == 2:
                            list1 = value.split(';')
                            self.write_base_type(
                                Mark.BYTE, len(list1), stream_obj)
                            for value1 in list1:
                                list2 = value1.split('_')
                                self.write_base_type(
                                    Mark.BYTE, len(list2), stream_obj)
                                for value2 in list2:
                                    self.write_base_type(
                                        type_obj.type_name, value2, stream_obj)
                        else:
                            list1 = value.split('_')
                            self.write_base_type(
                                Mark.BYTE, len(list1), stream_obj)
                            for value1 in list1:
                                self.write_base_type(
                                    type_obj.type_name, value1, stream_obj)
                    else:
                        self.write_base_type(type_obj, value, stream_obj)

    def extract_compress_configs(self):
        compress_obj = zlib.compressobj(wbits=-zlib.MAX_WBITS)
        out_path = os.path.join(self.__cfg_dest_path, "config.dat")
        with open(out_path, "wb") as file:
            for name, byte_obj in ParseXls.__config_collection_dict.items():
                file.write(compress_obj.compress(byte_obj.bytes_obj))
            file.write(compress_obj.flush())
        print('write file to: ' + out_path)

    def extract_config_dat_list(self):
        for name, byte_obj in ParseXls.__config_collection_dict.items():
            file_path = os.path.join(self.__cfg_dest_path, name) + ".dat"
            with open(file_path, "wb") as file:
                byte_obj.write_to_stream(file)
            print('wirte file to:' + file_path)

    def extract_class_collection_file(self):
        content_str = self._get_class_collection_templet_str()
        content_str = content_str.replace(Mark.MARK_PACKAGE, Mark.PATH_PACKAGE)
        content_str = reutils.es_import_declare_list.sub(
            reutils.def_one_mark_list(
                Mark.MARK_CLASS_NAME,
                self.__total_class_list),
            content_str)
        content_str = reutils.class_declare_list.sub(
            reutils.def_one_mark_list(
                Mark.MARK_CLASS_NAME,
                self.__total_class_list),
            content_str)
        content_str = reutils.property_declare_list.sub(
            reutils.def_one_mark_list(
                Mark.MARK_CLASS_NAME,
                self.__total_class_list),
            content_str)
        content_str = reutils.es_export_declare_list.sub(
            reutils.def_one_mark_list(
                Mark.MARK_PROPERTY_TYPE,
                self.__total_class_list),
            content_str)

        class_name = 'StaticData'
        content_str = content_str.replace(Mark.MARK_CLASS_NAME, class_name)
        file_path = os.path.join(
            self.__code_dest_path,
            class_name) + '.' + self._get_file_extension_name()
        with open(file_path, 'w', -1, 'utf-8') as file:
            file.write(content_str)
        print('write file to: ' + file_path)

    @staticmethod
    def write_base_type(type_name, value, writer):
        try:
            if type_name == Mark.STRING:
                writer.write_utf(value)
            elif type_name == Mark.BYTE:
                writer.write_unsigned_byte(value)
            elif type_name == Mark.SHORT:
                writer.write_unsigned_short(value)
            elif type_name == Mark.INT:
                writer.write_int(value)
            elif type_name == Mark.FLOAT:
                writer.write_float(value)
            else:
                raise Exception('new base type appear: ' + type_name)
        except struct.error:
            ParseXls.__error_info.alert_struct_err()

    @staticmethod
    def need_care(value):
        if isinstance(value, float) or isinstance(value, int):
            return value == 1
        return False


class ClassInfo:
    def __init__(self, name):
        self.__name = name
        self.type_list = []
        self.property_list = []

    @property
    def name(self):
        return self.__name


class ArrayInfo:
    def __init__(self, type_name, dimension):
        self.__type_name = type_name
        self.__dimension = dimension

    @property
    def type_name(self):
        return self.__type_name

    @property
    def dimension(self):
        return self.__dimension
