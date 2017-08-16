import re


def is_split_case(raw_string):
    return (raw_string.find(';') > 0) and (raw_string.find('$') < 0)


def beautify_formation(name_str, capitalize=False):
    result = name_str.strip()
    sp_list = result.split('_')
    sp_list = [string_first_upper(w) for w in sp_list]
    if not capitalize:
        sp_list[0] = string_first_lower(sp_list[0])
    result = ''.join(sp_list)
    return result


def string_first_upper(org_str):
    return org_str[0].upper()+org_str[1:]


def string_first_lower(org_str):
    return org_str[0].lower()+org_str[1:]


def check_blank_cell(cell, file):
    if cell == '':
        raise Exception('值未定义 %s %s' % (file, cell.coordinate))
