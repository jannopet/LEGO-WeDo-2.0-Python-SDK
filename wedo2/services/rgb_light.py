
from wedo2.bluetooth.bluetooth_io import BluetoothIO
from wedo2.input_output.data_format import DataFormat
from wedo2.input_output.input_format import InputFormat, InputFormatUnit
from wedo2.utils import byte_utils
from wedo2.services.lego_service import LegoService
from enum import Enum
    
class RGBLightMode(Enum):
    RGB_LIGHT_MODE_DISCRETE = 0
    RGB_LIGHT_MODE_ABSOLUTE = 1
    RGB_LIGHT_MODE_UNKNOWN = 2

SERVICE_RGB_LIGHT_NAME = "RGB Light"

class RGBLight(LegoService):

    def __init__(self, connect_info, io):
        super(RGBLight, self).__init__(connect_info, io)
        self.add_valid_data_formats()

    def create_service(connect_info, io):
        return RGBLight(connect_info, io)

    def get_service_name(self):
        return SERVICE_RGB_LIGHT_NAME

    def get_default_input_format(self):
        return InputFormat.input_format(self.connect_info.connect_id, self.connect_info.type_id,
                                        RGBLightMode.RGB_LIGHT_MODE_DISCRETE.value, 1,
                                        InputFormatUnit.INPUT_FORMAT_UNIT_RAW, True)

    def set_color(self, red, green, blue):
        if self.get_rgb_mode() == RGBLightMode.RGB_LIGHT_MODE_ABSOLUTE:
            self.io.write_color(red, green, blue, self.connect_info.connect_id)
        else:
            print("Cannot change color with RGB values. RGB Light is not set to Absolute Mode.")

    def get_rgb_mode(self):
        return RGBLightMode(self.get_input_format_mode())

    def set_rgb_mode(self, rgb_mode):
        self.update_current_input_format_with_new_mode(rgb_mode.value)

    def set_color_index(self, index):
        if self.get_rgb_mode() == RGBLightMode.RGB_LIGHT_MODE_DISCRETE:
            self.io.write_color_index(index, self.connect_info.connect_id)
        else:
            print("Cannot change color with indexed values. RGB Light is not set to Discrete Mode")

    def get_default_color_index(self):
        return 3

    def switch_off(self):
        if self.get_rgb_mode() == RGBLightMode.RGB_LIGHT_MODE_ABSOLUTE:
            self.set_color(0, 0, 0)
        elif self.get_rgb_mode() == RGBLightMode.RGB_LIGHT_MODE_DISCRETE:
            self.set_color_index(0)
        else:
            print("Cannot switch off RGB - unknown mode")

    def switch_to_default_color(self):
        if self.get_rgb_mode() == RGBLightMode.RGB_LIGHT_MODE_ABSOLUTE:
            self.set_color(0, 255, 255)
        elif self.get_rgb_mode() == RGBLightMode.RGB_LIGHT_MODE_DISCRETE:
            self.set_color_index(self.get_default_color_index())
        else:
            print("Cannot switch to default color - unknown mode")
            

    def color_from_data(self, data):
        if len(data) == 3:
            red = data[0]
            green = data[1]
            blue = data[2]
            return Color.rgb(red, green, blue)

        return None

    def add_valid_data_formats(self):
        self.add_valid_data_format(DataFormat.create("Discrete", RGBLightMode.RGB_LIGHT_MODE_DISCRETE.value,
                                                     InputFormatUnit.INPUT_FORMAT_UNIT_RAW, 1, 1)) 
        self.add_valid_data_format(DataFormat.create("Discrete", RGBLightMode.RGB_LIGHT_MODE_DISCRETE.value,
                                                     InputFormatUnit.INPUT_FORMAT_UNIT_PERCENTAGE, 1, 1))
        self.add_valid_data_format(DataFormat.create("Discrete", RGBLightMode.RGB_LIGHT_MODE_DISCRETE.value,
                                                     InputFormatUnit.INPUT_FORMAT_UNIT_SI, 4, 1)) 
        self.add_valid_data_format(DataFormat.create("Absolute", RGBLightMode.RGB_LIGHT_MODE_ABSOLUTE.value,
                                                     InputFormatUnit.INPUT_FORMAT_UNIT_RAW, 1, 3)) 
        self.add_valid_data_format(DataFormat.create("Absolute", RGBLightMode.RGB_LIGHT_MODE_ABSOLUTE.value,
                                                     InputFormatUnit.INPUT_FORMAT_UNIT_PERCENTAGE, 1, 3))
        self.add_valid_data_format(DataFormat.create("Absolute", RGBLightMode.RGB_LIGHT_MODE_ABSOLUTE.value,
                                                     InputFormatUnit.INPUT_FORMAT_UNIT_SI, 4, 3)) 

