
from wedo2.utils import byte_utils
from enum import Enum

class InputFormatUnit(Enum):
    INPUT_FORMAT_UNIT_RAW = 0
    INPUT_FORMAT_UNIT_PERCENTAGE = 1
    INPUT_FORMAT_UNIT_SI = 2
    INPUT_FORMAT_UNIT_UNKNOWN = 3


INPUT_FORMAT_PACKAGE_SIZE = 11
FORMAT_DATA_SIZE = 8
    
class InputFormat:

    INPUT_FORMAT_PACKAGE_SIZE = 11
    FORMAT_DATA_SIZE = 8
    
    def __init__(self, connect_id, type_id, mode, delta_interval, unit,
                 notifications_enabled, revision=0, number_of_bytes=0):
        self.connect_id = connect_id
        self.type_id = type_id
        self.mode = mode
        self.delta_interval = delta_interval
        self.unit = unit
        self.notifications_enabled = notifications_enabled
        self.revision = revision
        self.number_of_bytes= number_of_bytes


    def input_format(*args):

        # InputFormat from bytearray
        if len(args) == 1:  
            data = args[0]
            if data == None:
                return None

            if len(data) != INPUT_FORMAT_PACKAGE_SIZE:
                return None
                    
            revision = data[0]
            connect_id = data[1]
            type_id = data[2]
            mode = data[3]
            delta_interval = byte_utils.get_unsigned_int(data[4:8])
            unit = InputFormatUnit(data[8])
            notifications_enabled = data[9] == 1
            number_of_bytes = data[10]

            return InputFormat(connect_id, type_id, mode, delta_interval, unit,
                               notifications_enabled, revision, number_of_bytes)

        # InputFormat from list of arguments
        elif len(args) == 6: 
            connect_id = args[0]
            io_type = args[1]
            mode = args[2]
            delta_interval = args[3]
            unit = args[4]
            notifications_enabled = args[5]

            return InputFormat(connect_id, io_type, mode, delta_interval,
                               unit.value, notifications_enabled)

        # Unknown case
        else:               
            return None
            
        
    def input_format_by_setting_mode(self, mode):
        return InputFormat(self.connect_id, self.type_id, mode, self.delta_interval,
                           self.unit, self.notifications_enabled)
     
    def input_format_by_setting_mode_and_unit(self, mode, unit):
        return InputFormat(self.connect_id, self.type_id, mode, self.delta_interval,
                           unit.value, self.notifications_enabled)

    def input_format_by_setting_delta_interval(self, delta_interval):
        return InputFormat(self.connect_id, self.type_id, self.mode, delta_interval,
                           self.unit, self.notifications_enabled)

    def input_format_by_setting_notifications_enabled(self, notifications_enabled):
        return InputFormat(self.connect_id, self.type_id, self.mode, self.delta_interval,
                           self.unit, notifications_enabled)

    def input_format_to_byte_array(self):
        array = bytearray(FORMAT_DATA_SIZE)
        array[0] = self.type_id
        array[1] = self.mode
        byte_utils.put_unsigned_int(array, self.delta_interval)
        array[6] = self.unit
        array[7] = self.notifications_enabled
        
        return array

    def __str__(self):
        return "InputFormat{" \
                "revision=" + str(self.revision) + "" \
                ", connect_id=" + str(self.connect_id) + "" \
                ", type_id=" + str(self.type_id) + "" \
                ", mode=" + str(self.mode) + "" \
                ", delta_interval=" + str(self.delta_interval) + "" \
                ", unit=" + str(self.unit) + "" \
                ", notifications_enabled=" + str(self.notifications_enabled) + "" \
                ", number_of_bytes=" + str(self.number_of_bytes) + '}'

    def __eq__(self, obj):
        try:
            if self.connect_id != obj.connect_id: return False
            if self.delta_interval != obj.delta_interval: return False
            if self.mode != obj.mode: return False
            if self.notifications_enabled != obj.notifications_enabled: return False
            if self.number_of_bytes != obj.number_of_bytes: return False
            if self.revision != obj.revision: return False
            if self.type_id != obj.type_id: return False
            if self.unit != obj.unit: return False

            return True
        except:
            return False

    def __ne__(self, obj):
        return not self.__eq__(obj)

