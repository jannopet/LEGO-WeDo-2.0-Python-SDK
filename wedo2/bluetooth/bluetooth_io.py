
from wedo2.input_output.output_command import OutputCommand
from wedo2.input_output.input_command import InputCommand
from wedo2.bluetooth.connect_info import ConnectInfo, IOType
from wedo2.bluetooth import bluetooth_helper

CHARACTERISTIC_INPUT_VALUE_UUID    = "0x1560"
CHARACTERISTIC_INPUT_FORMAT_UUID   = "0x1561"
CHARACTERISTIC_INPUT_COMMAND_UUID  = "0x1563"
CHARACTERISTIC_OUTPUT_COMMAND_UUID = "0x1565"


class BluetoothIO:

    def __init__(self, associated_device):
        # Associated device is the pygatt backend object we have connected to
        self.associated_device = associated_device
        self.services = []
    
    def read_value_for_connect_id(self, connect_id):
        input_command = InputCommand.command_read_value_for_connect_id(connect_id)
        self.write_input_command(input_command.data)
        value = self.read_input_value()
        return value

    def read_input_value(self):
        char_uuid = bluetooth_helper.uuid_with_prefix_custom_base(CHARACTERISTIC_INPUT_VALUE_UUID)
        data = self.associated_device.char_read(char_uuid)
        print(data, "LENGTH: ", len(data))
        return data[2:]

    def reset_state_for_connect_id(self, connect_id):
        reset_bytes = bytearray([0x44, 0x11, 0xAA])
        self.write_data(reset_bytes, connect_id)

    def write_input_format(self, input_format, connect_id):
        input_command = InputCommand.command_write_input_format(input_format, connect_id)
        self.write_input_command(input_command.data)

    def read_input_format_for_connect_id(self, connect_id):
        input_command = InputCommand.command_read_input_format_for_connect_id(connect_id)
        self.write_input_command(input_command.data)
        return self.read_input_format()

    def read_input_format(self):
        char_uuid = bluetooth_helper.uuid_with_prefix_custom_base(CHARACTERISTIC_INPUT_FORMAT_UUID)
        data = self.associated_device.char_read(char_uuid)
        return data

    def write_input_command(self, command):
        char_uuid = bluetooth_helper.uuid_with_prefix_custom_base(CHARACTERISTIC_INPUT_COMMAND_UUID)
        self.associated_device.char_write(char_uuid, command)

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

    def write_color_index(self, index, connect_id):
        output_command = OutputCommand.command_write_rgb_light_index(index, connect_id)
        self.write_output_command(output_command.data)

    def write_data(self, data, connect_id):
        output_command = OutputCommand.command_with_direct_write_through_data(data, connect_id)
        self.write_output_command(output_command.data)

    def write_output_command(self, command):
        char_uuid = bluetooth_helper.uuid_with_prefix_custom_base(CHARACTERISTIC_OUTPUT_COMMAND_UUID)
        self.associated_device.char_write(char_uuid, command)

    def subscribe_to_char(self, uuid, callback):
        self.associated_device.subscribe(uuid, callback)
        
    def unsubscribe_from_char(self, uuid):
        self.associated_device.unsubscribe(uuid)
        
    
        
