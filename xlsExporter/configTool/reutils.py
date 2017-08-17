import Mark
import re

pattern_property_declare_list = Mark.MARK_PROPERTY_DECLARE_LIST + r'(\s*)(.+)'
pattern_parse_sentence_list = Mark.MARK_PARSE_SENTENCE_LIST + r'(\s*)(.+)'
pattern_class_declare_list = Mark.MARK_CLASS_DECLARE_LIST + r'(\s*)(.+)'
pattern_es_import_declare_list = Mark.MARK_ES_IMPORT_DECLARE_LIST + \
    r'(\s*)(.+)'
pattern_es_export_declare_list = Mark.MARK_ES_EXPORT_DECLARE_LIST + \
    r'(\s*)(.+)'

property_declare_list = re.compile(pattern_property_declare_list)
parse_sentence_list = re.compile(pattern_parse_sentence_list)
class_declare_list = re.compile(pattern_class_declare_list)
es_import_declare_list = re.compile(pattern_es_import_declare_list)
es_export_declare_list = re.compile(pattern_es_export_declare_list)


def def_one_mark_list(mark, src_list, org_input=None):
    """
    替换只有一种标签的标记语句列
    :param mark: 标签名
    :param src_list: 数据源
    :param org_input: 指定读取源数据的方式
    :return:
    """
    input_map = __trance_map(org_input)

    def out_fuc(matched):
        split_str = matched.group(1)
        sentence_str = matched.group(2)
        out_list = [sentence_str.replace(mark, input_map(list_element))
                    for list_element in src_list]
        return split_str.join(out_list)
    return out_fuc


def def_two_mark_list(mark1, list1, mark2, list2, map1=None, map2=None):
    map1 = __trance_map(map1)
    map2 = __trance_map(map2)

    def out_fuc(matched):
        split_str = matched.group(1)
        sentence_str = matched.group(2)
        out_list = []
        for index, ele1 in enumerate(list1):
            ele2 = list2[index]
            out_list.append(
                sentence_str.replace(
                    mark1,
                    map1(ele1)).replace(
                    mark2,
                    map2(ele2)))
        return split_str.join(out_list)
    return out_fuc


def __trance_map(org_input):
    if org_input is None:
        return __self_map
    elif isinstance(org_input, dict):
        return __from_map(org_input)
    elif isinstance(org_input, str):
        return __property_map(org_input)
    else:
        return org_input


def __property_map(p_name):
    def map_fuc(value):
        return getattr(value, p_name)
    return map_fuc


def __from_map(dict_map):
    def map_fuc(value):
        return dict_map[value]
    return map_fuc


def __self_map(value):
    return value
