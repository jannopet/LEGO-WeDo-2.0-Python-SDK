
from wedo2.input_output.data_format import DataFormat
from wedo2.input_output.input_format import InputFormat, InputFormatUnit
from wedo2.services.lego_service import LegoService
from enum import Enum


SERVICE_TILT_SENSOR_NAME = "Tilt Sensor"

class TiltSensorDirection(Enum):
    TILT_SENSOR_DIRECTION_NEUTRAL = 0
    TILT_SENSOR_DIRECTION_BACKWARD = 3
    TILT_SENSOR_DIRECTION_RIGHT = 5
    TILT_SENSOR_DIRECTION_LEFT = 7
    TILT_SENSOR_DIRECTION_FORWARD = 9
    TILT_SENSOR_DIRECTION_UNKNOWN = 10


class TiltSensorMode(Enum):
    TILT_SENSOR_MODE_ANGLE = 0
    TILT_SENSOR_MODE_TILT = 1
    TILT_SENSOR_MODE_CRASH = 2
    TILT_SENSOR_MODE_UNKNOWN = 4

class TiltSensorAngle(object):
    x = 0
    y = 0

    def __str__(self):
        return "[{0}, {1}]".format(self.x, self.y)

class TiltSensor(LegoService):

    tilt_sensor_angle_zero = TiltSensorAngle()

    def __init__(self, connect_info, io):
        super(TiltSensor, self).__init__(connect_info, io)
        self.tilt_sensor_mode = TiltSensorMode(self.get_default_input_format().mode).value
        self.add_valid_data_formats()
        self.io.write_input_format(self.get_default_input_format(), connect_info.connect_id)

    def create_service(connect_info, io):
        return TiltSensor(connect_info, io)

    def get_service_name(self):
        return SERVICE_TILT_SENSOR_NAME

    def get_default_input_format(self):
        return InputFormat.input_format(self.connect_info.connect_id, self.connect_info.type_id,
                                        TiltSensorMode.TILT_SENSOR_MODE_TILT.value, 1, InputFormatUnit.INPUT_FORMAT_UNIT_SI, True)

    def tilt_sensor_angle_make(self, x, y):
        angle = TiltSensorAngle()
        angle.x = x
        angle.y = y
        return angle
        
    def get_direction(self):
        if self.input_format != None:
            if self.input_format.mode != TiltSensorMode.TILT_SENSOR_MODE_TILT.value:
                return TiltSensorDirection.TILT_SENSOR_DIRECTION_UNKNOWN
            else:
                direction_int = self.get_number_from_value_data(self.io.read_value_for_connect_id(self.connect_info.connect_id))
                if direction_int != None:
                    if direction_int < 10:
                        return TiltSensorDirection(direction_int)
                    else:
                        return TiltSensorDirection.TILT_SENSOR_DIRECTION_UNKNOWN
                else:
                    return TiltSensorDirection.TILT_SENSOR_DIRECTION_NEUTRAL
        
        return TiltSensorDirection.TILT_SENSOR_DIRECTION_UNKNOWN

    def get_angle(self):
        if self.input_format.mode != TiltSensorMode.TILT_SENSOR_MODE_ANGLE.value:
            return self.tilt_sensor_angle_zero
            
        data_set_numbers = self.get_numbers_from_value_data_set(self.io.read_value_for_connect_id(self.connect_info.connect_id))
        if len(data_set_numbers) == 2:
            return self.tilt_sensor_angle_make(data_set_numbers[0], data_set_numbers[1])

        return self.tilt_sensor_angle_zero

    def set_tilt_sensor_mode(self, mode):
        self.update_current_input_format_with_new_mode(mode.value)
        self.tilt_sensor_mode = mode.value

    def add_valid_data_formats(self):
        self.add_valid_data_format(DataFormat.create("Angle", TiltSensorMode.TILT_SENSOR_MODE_ANGLE.value,
                                                     InputFormatUnit.INPUT_FORMAT_UNIT_RAW.value, 1, 2))
        self.add_valid_data_format(DataFormat.create("Angle", TiltSensorMode.TILT_SENSOR_MODE_ANGLE.value,
                                                     InputFormatUnit.INPUT_FORMAT_UNIT_PERCENTAGE.value, 1, 2))
        self.add_valid_data_format(DataFormat.create("Angle", TiltSensorMode.TILT_SENSOR_MODE_ANGLE.value,
                                                     InputFormatUnit.INPUT_FORMAT_UNIT_SI.value, 4, 2))
    
        self.add_valid_data_format(DataFormat.create("Tilt", TiltSensorMode.TILT_SENSOR_MODE_TILT.value,
                                                     InputFormatUnit.INPUT_FORMAT_UNIT_RAW.value, 1, 1))
        self.add_valid_data_format(DataFormat.create("Tilt", TiltSensorMode.TILT_SENSOR_MODE_TILT.value,
                                                     InputFormatUnit.INPUT_FORMAT_UNIT_PERCENTAGE.value, 1, 1))
        self.add_valid_data_format(DataFormat.create("Tilt", TiltSensorMode.TILT_SENSOR_MODE_TILT.value,
                                                     InputFormatUnit.INPUT_FORMAT_UNIT_SI.value, 4, 1))

