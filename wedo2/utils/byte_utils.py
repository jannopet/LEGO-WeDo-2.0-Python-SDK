
import struct

# Takes a value as an unsigned short, transforms it into an array of two bytes
# and adds those bytes to the end of the given bytearray 
def put_unsigned_short(array, value):
    short_array = struct.pack("<H", value)
    index = 0
    while array[index] != 0:
        index += 1

    array[index] = short_array[0]
    array[index+1] = short_array[1]

def get_unsigned_int(array):
    value = struct.unpack("<I", array)[0]
    return value
    
def array_from_unsigned_int(value):
    int_array = struct.pack("<I", value)
    return int_array

def array_from_signed_value(value):
    array = struct.pack('b', value)
    return array

def get_float(array):
    value = struct.unpack("<f", array)[0]
    return value

def get_short(array):
    value = struct.unpack("<h", array)[0]
    return value

def get_int(array):
    value = struct.unpack("<i", array)[0]
    return value
