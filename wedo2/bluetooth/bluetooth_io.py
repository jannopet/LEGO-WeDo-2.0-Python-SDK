
from wedo2.input_output.output_command import OutputCommand
from wedo2.bluetooth import bluetooth_helper


CHARACTERISTIC_INPUT_VALUE_UUID    = "0x1560"
CHARACTERISTIC_INPUT_FORMAT_UUID   = "0x1561"
CHARACTERISTIC_INPUT_COMMAND_UUID  = "0x1563"
CHARACTERISTIC_OUTPUT_COMMAND_UUID = "0x1565"


class BluetoothIO:

    def __init__(self, associated_device):
        # Associated device is the pygatt backend object we have connected to
        self.associated_device = associated_device

    
    # readValueForConnectId(connectId)

    # resetStateForConnectId(int connectId)

    # writeInputFormat(InputFormat inputFormat, int connectId)

    # readInputFormatForConnectId(int connectId)

    # writeInputCommand(InputCommand command)

    def write_motor_power(self, power, offset, connect_id):
        is_positive = power >= 0
        power = abs(power)

        actual_power = ((100.0 - offset) / 100.0) * power + offset
        actual_result_int = round(actual_power)

        if not is_positive:
            actual_result_int = -actual_result_int

        output_command = OutputCommand.command_write_motor_power(actual_result_int, connect_id)
        self.write_output_command(output_command.data)

    def write_piezo_tone_frequency(self, frequency, duration, connect_id):
        output_command = OutputCommand.command_write_piezo_tone_frequency(frequency, duration, connect_id)
        self.write_output_command(output_command.data)

    def write_piezo_tone_stop(self, connect_id):
        output_command = OutputCommand.command_write_piezo_tone_stop_for_connect_id(connect_id)
        self.write_output_command(output_command.data)

    def write_color(self, red, green, blue, connect_id):
        output_command = OutputCommand.command_write_rgb_light(red, green, blue, connect_id)
        self.write_output_command(output_command.data)

    # writeData(data, connect_id)

    def write_output_command(self, command):
        char_uuid = bluetooth_helper.uuid_with_prefix_custom_base(CHARACTERISTIC_OUTPUT_COMMAND_UUID)
        self.associated_device.char_write(char_uuid, command)


        
        
    


        
    
        
