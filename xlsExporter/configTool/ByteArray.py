import struct
import io
import sys


def write_utf(stream_obj, data):
    data = str(data).encode('utf-8')
    data_len = len(data)
    value = struct.pack('!H%ds' % data_len, data_len, data)
    stream_obj.write(value)


def write_unsigned_byte(stream_obj, data):
    value = struct.pack('B', int(data))
    stream_obj.write(value)


def write_unsigned_short(stream_obj, data):
    value = struct.pack('!H', int(data))
    stream_obj.write(value)


def write_unsigned_int(stream_obj, data):
    value = struct.pack('!I', int(data))
    stream_obj.write(value)


def write_int(stream_obj, data):
    value = struct.pack('!i', int(data))
    stream_obj.write(value)


def write_float(stream_obj, data):
    value = struct.pack('!f', float(data))
    stream_obj.write(value)


class ByteArray:
    def __init__(self):
        self.__stream_obj = io.BytesIO()

    def __len__(self):
        return sys.getsizeof(self.__stream_obj)

    @property
    def bytes_obj(self):
        self.__stream_obj.seek(0)
        return self.__stream_obj.read()

    def write_to_stream(self, target):
        self.__stream_obj.seek(0)
        target.write(self.__stream_obj.read())

    def write_utf(self, data):
        write_utf(self.__stream_obj, data)

    def write_unsigned_byte(self, data):
        write_unsigned_byte(self.__stream_obj, data)

    def write_unsigned_short(self, data):
        write_unsigned_short(self.__stream_obj, data)

    def write_unsigned_int(self, data):
        write_unsigned_int(self.__stream_obj, data)

    def write_int(self, data):
        write_int(self.__stream_obj, data)

    def write_float(self, data):
        write_utf(self.__stream_obj, data)
