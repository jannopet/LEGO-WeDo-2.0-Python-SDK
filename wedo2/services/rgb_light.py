
from wedo2.device import io
from wedo2.input_output import data_format
from data_format import DataFormat
from wedo2.input_output import input_format
from input_format import InputFormat
from input_format import InputFormatUnit
from wedo2.utils import byte_utils
from wedo2.services import lego_service
from lego_service import LegoService
from enum import Enum

# A (possibly) temporary class for representing colors
class Color(object):

    def __init__(self, a, r, g, b):
        self.a = a  # alpha
        self.r = r  # red
        self.g = g  # green
        self.b = b  # blue

    def rgb(r, g, b):
        return Color(0xFF, r, g, b)

    def argb(a, r, g, b):
        return Color(a, r, g, b)

    

class RGBLightMode(Enum):
    RGB_LIGHT_MODE_DISCRETE = 0
    RGB_LIGHT_MODE_ABSOLUTE = 1
    RGB_LIGHT_MODE_UNKNOWN = 2

SERVICE_RGB_LIGHT_NAME = "RGB Light"

class RGBLight(LegoService):

    def __init__(connect_info, io):
        super(RGBLight, self).__init__(connect_info, io)
        self.add_valid_data_formats()
        self.color = None
        self.color_index = 0

    def create_service(connect_info, io):
        return RGBLight(connect_info, io)

    def get_service_name(self):
        return SERVICE_RGB_LIGHT_NAME

    def get_default_input_format(self):
        return InputFormat.input_format(self.connect_info.connect_id, self.connect_info.type_id,
                                        RGBLightMode.RGB_LIGHT_MODE_DISCRETE.value, 1,
                                        InputFormatUnit.INPUT_FORMAT_UNIT_RAW, True)

    def set_color(self, rgb_color):
        if self.get_rgb_mode() == RGBLightMode.RGB_LIGHT_MODE_ABSOLUTE:
            self.color = rgb_color
            # Solution for now - needs to be checked later on
            red = rgb_color.r
            green = rgb_color.g
            blue = rgb_color.b

            self.io.write_color(red, green, blue, self.connect_info.connect_id)
        else:
            # LDSDKLogger.w("Ignoring attempt to set RGB color...")

    def get_default_color(self):
        # Solution for now - needs to be checked later on
        return Color.argb(0xFF, 0x00, 0x00, 0xFF)

    def get_rgb_mode(self):
        return RGBLightMode(self.get_input_format_mode())

    def set_rgb_mode(self, rgb_mode):
        self.update_current_input_format_with_new_mode(rgb_mode.value)

    def set_color_index(self, index):
        if self.get_rgb_mode() == RGBLight_mode.RGB_LIGHT_MODE_DISCRETE:
            self.color_index = index
            self.io.write_color_index(index, self.connect_info.connect_id)
        else:
            # LDSDKLogger.w("Ignoring attempt to set RGB color index ...")

    def get_default_color_index(self):
        return 3

    def switch_off(self):
        if self.get_rgb_mode() == RGBLightMode.RGB_LIGHT_MODE_ABSOLUTE:
            # Solution for now - needs to be checked later on
            self.set_color(Color.rgb(0, 0, 0))
        elif self.get_rgb_mode() == RGBLightMode.RGB_LIGHT_MODE_DISCRETE:
            self.set_color_index(0)
        else:
            # LDSDKLogger.w("Cannot switch off RGB - unknown mode ...")

    def switch_to_default_color(self):
        if self.get_rgb_mode() == RGBLightMode.RGB_LIGHT_MODE_ABSOLUTE:
            self.set_color(self.get_default_color())
        elif self.get_rgb_mode() == RGBLightMode.RGB_LIGHT_MODE_DISCRETE:
            self.set_color_index(self.get_default_color_index())
        else:
            # LDSDKLogger.w("Cannot switch to default color - unknown mode ...")

    # def handle_updated_value_data(self, value_data)

    def color_from_data(self, data):
        if len(data) == 3:
            red = data[0]
            green = data[1]
            blue = data[2]
            # Solution for now - needs to be checked later on
            return Color.rgb(red, green, blue)

        # LDSDKLogger.w("Cannot create color from data ...")
        return None

    def add_valid_data_formats(self):
        return None        
    

    # def __eq__
    

    
    
    
