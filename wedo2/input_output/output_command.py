
from wedo2.utils import byte_utils

HEADER_SIZE = 3

WRITE_MOTOR_POWER_COMMAND_ID = 0x01

PLAY_PIEZO_TONE_COMMAND_ID = 0x02
STOP_PIEZO_TONE_COMMAND_ID = 0x03

WRITE_RGB_COMMAND_ID = 0x04

WRITE_DIRECT_ID = 0x05

COMMAND_PAYLOAD_SIZE_PIEZO = 4
COMMAND_PAYLOAD_SIZE_RGB_LIGHT = 3

class OutputCommand:

    def __init__(self, connect_id, command_id, payload_data):
        data = bytearray(HEADER_SIZE + len(payload_data))

        data[0] = connect_id
        data[1] = command_id
        data[2] = len(payload_data)

        index = HEADER_SIZE
        for byte in payload_data:
            data[index] = byte
            index += 1

        self.data = data

    
    def command_write_motor_power(power, connect_id):
        return OutputCommand(connect_id, WRITE_MOTOR_POWER_COMMAND_ID, bytearray([power]))

    def command_write_piezo_tone_frequency(frequency, duration, connect_id):
        array = bytearray(4)
        byte_utils.put_unsigned_short(array, frequency)
        byte_utils.put_unsigned_short(array, duration)

        return OutputCommand(connect_id, PLAY_PIEZO_TONE_COMMAND_ID, array)

    
        
