class ErrorInfo:
    __class_list = []
    __define_list = []

    def __init__(self):
        self.__file_name = None
        self.column_index = None
        self.row_index = None

    def __str__(self):
        out = self.__file_name
        if self.column_index is not None:
            column_name = chr(65+self.column_index)
            if self.row_index is None:
                out += ' column:%s' % column_name
            else:
                out += ' %s%d' % (column_name, self.row_index+1)
        return out

    def __repr__(self):
        return self.__str__()

    @property
    def file_name(self):
        return self.__file_name

    @file_name.setter
    def file_name(self, value):
        self.__init__()
        self.__file_name = value

    def alert_struct_err(self):
        raise Exception(self.__get_pos('数值超出设定类型最大值'))

    def alert_type_err(self, type_str):
        raise Exception(self.__get_pos('错误的数据类型: '+type_str))

    def check_class_name(self, value):
        self.check_value(value)
        if value in self.__class_list:
            raise Exception(self.__get_pos('重复定义的类名'))
        self.__class_list.append(value)

    def check_repeat_value(self, value, check_list, name="名称"):
        if value in check_list:
            raise Exception(self.__get_pos('重复定义的'+name))

    def check_equal_count(self, value, target):
        if value != target:
            raise Exception(self.__get_pos('字段数量不匹配'))

    def check_define_name(self, value):
        self.check_value(value)
        if value in self.__define_list:
            raise Exception(self.__get_pos('重复的自定义类名'))
        self.__define_list.append(value)

    def check_value(self, value):
        if value is None:
            raise Exception(self.__get_pos('值未定义'))

    def __get_pos(self, prefix):
        return prefix + ' @' + str(self)
