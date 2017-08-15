import struct


class ByteArray:
    def __init__(self):
        self.__file_obj = None

    def update_file_obj(self, file_obj):
        self.__file_obj = file_obj;

    def write_utf(self, data):
        data = str(data).encode('utf-8')
        data_len = len(data)
        value = struct.pack('!H%ds' % data_len, data_len, data)
        self.__file_obj.write(value)

    def write_unsigned_byte(self, data):
        value = struct.pack('B', int(data))
        self.__file_obj.write(value)

    def write_unsigned_short(self, data):
        value = struct.pack('!H', int(data))
        self.__file_obj.write(value)

    def write_unsigned_int(self, data):
        value = struct.pack('!I', int(data))
        self.__file_obj.write(value)

    def write_int(self, data):
        value = struct.pack('!i', int(data))
        self.__file_obj.write(value)

    def write_float(self, data):
        value = struct.pack('!f', float(data))
        self.__file_obj.write(value)
