
import uuid

UUID_CUSTOM_BASE    = "1212-EFDE-1523-785FEABCD123"
UUID_STANDARD_BASE  = "0000-1000-8000-00805f9b34fb"

def uuid_with_prefix_custom_base(prefix):
    padding = add_leading_zeroes(prefix)
    return "{}-{}".format(padding, UUID_CUSTOM_BASE)

def uuid_with_prefix_standard_base(prefix):
    padding = add_leading_zeroes(prefix)
    return "{}-{}".format(padding, UUID_STANDARD_BASE)

def add_leading_zeroes(prefix):
    hex_prefix = "0x"
    if prefix[0:2] == hex_prefix:
        prefix = prefix[2:]

    return ("00000000" + prefix)[len(prefix):]

    
