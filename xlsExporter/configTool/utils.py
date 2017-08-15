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


def convert_value(lst):
    ret = []
    for v in lst:
        data = v
        if isinstance(v, int):
            data = int(v)
        if isinstance(v, float):
            if v == int(v):
                data = int(v)
            else:
                data = float(v)
        # if isinstance(v, unicode):
        #     data = v.encode("gbk")
        data = str(data)
        ret.append(data)
    return ret


def check_blank_cell(cell, file):
    if cell == '':
        raise Exception('值未定义 %s %s' % (file, cell.coordinate))


def extract_variables_name(raw_string):
    variables_list = []
    variable_name = []
    wave_position_list = [m.start() for m in re.finditer('~', raw_string)]
    for i in range(len(wave_position_list)):
        if i == 0:
            continue  # the first ~ symble is just a mark for the form 'array~channel_type$short~map_id;int~x;int~y'
        variable_name[:] = []
        for j in range(wave_position_list[i] + 1, len(raw_string)):
            if (ord(raw_string[j]) == 95) or ((ord(raw_string[j]) >= 48) and (ord(raw_string[j]) <= 57)) or (
                    (ord(raw_string[j]) >= 65) and (ord(raw_string[j]) <= 90)) or ((ord(raw_string[j]) >= 97) and (ord(raw_string[j]) <= 122)):
                variable_name.append(raw_string[j])
            else:
                break
        variables_list.append(beautify_formation(''.join(variable_name)))
    return variables_list


def extract_class_name(raw_string):
    class_name_po = raw_string.find('~') + 1
    class_name = []
    for i in range(class_name_po, len(raw_string)):
        if (ord(raw_string[i]) == 95) or ((ord(raw_string[i]) >= 48) and (ord(raw_string[i]) <= 57)) or (
            (ord(raw_string[i]) >= 65) and (ord(raw_string[i]) <= 90)) \
                or ((ord(raw_string[i]) >= 97) and (ord(raw_string[i]) <= 122)):
            class_name.append(raw_string[i])
        else:
            break
    lst = [word[0].upper() + word[1:]
           for word in ''.join(class_name).split()]
    string_class_name = " ".join(lst)
    string_class_name = beautify_formation(string_class_name, True)
    return string_class_name


def extract_type_name(raw_string):
    tmp_list = []
    type_list = []
    # it seems that the first type name always appears after '$' symble.
    dollor_po = raw_string.find('$')
    type_name = []
    for i in range(dollor_po + 1, len(raw_string)):
        if ((ord(raw_string[i]) >= 48) and (ord(raw_string[i]) <= 57)) or ((ord(raw_string[i]) >= 65) and (
                ord(raw_string[i]) <= 90)) or ((ord(raw_string[i]) >= 97) and (ord(raw_string[i]) <= 122)):
            type_name.append(raw_string[i])
        else:
            tmp_list.append(''.join(type_name))
            break
    # from the second type name, it seems that the type name always appears after ';' symble.
    # find all the position of semicolon in string name.
    semicolon_positin_list = [m.start()
                              for m in re.finditer(';', raw_string)]
    # print "semicolonPositinList = ",semicolonPositinList
    for semicolonpositin in semicolon_positin_list:
        type_name[:] = []  # clear content of typeName
        for j in range(semicolonpositin + 1, len(raw_string)):
            if ((ord(raw_string[j]) >= 48) and (ord(raw_string[j]) <= 57)) or ((ord(raw_string[j]) >= 65) and (
                    ord(raw_string[j]) <= 90)) or ((ord(raw_string[j]) >= 97) and (ord(raw_string[j]) <= 122)):
                type_name.append(raw_string[j])
            else:
                tmp_list.append(''.join(type_name))
                break

    for rawType in tmp_list:
        # type_list.append(self.repairType(rawType.lower()))
        type_list.append(rawType.lower())
    return type_list
    # typeString has the form 'array~channel_type$short~map_id;int~x;int~y'
