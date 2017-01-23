
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
    
def put_unsigned_int(array, value):
    int_array = struct.pack("<I", value)
    index = 0
    while array[index] != 0:
        index += 1

    for i in range(4):
        array[index + i] = int_array[i]
