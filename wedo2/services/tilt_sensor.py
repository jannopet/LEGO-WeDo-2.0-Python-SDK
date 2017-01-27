
from wedo2.input_output import data_format
from data_format import DataFormat
from wedo2.input_output import input_format
from input_format import InputFormat
from input_format import InputFormatUnit
from wedo2.services import lego_service
from lego_service import LegoService
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

class TiltSensorCrash(object):
    x = 0
    y = 0
    z = 0

    def __str__(self):
        return "[{0}, {1}, {2}]".format(self.x, self.y, self.z)

class TiltSensor(LegoService):

    tilt_sensor_angle_zero = TiltSensorAngle()
    tilt_sensor_crash_zero = TiltSensorCrash()

    def __init__(self, connect_info, io):
        super(TiltSensor, self).__init__(connect_info, io)
        self.tilt_sensor_mode = TiltSensorMode(self.get_default_input_format().mode).value
        self.add_valid_data_formats()

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

    def tilt_sensor_angle_equal_to_angle(self, angle1, angle2):
        acceptable_diff = 0.01
        # Should (angle1.x - angle2.x) be an absolute value ??
        return (angle1.x - angle2.x < acceptable_diff and angle1.y - angle2.y < acceptable_diff)

    def tilt_sensor_crash_make(self, x, y, z):
        crash = TiltSensorCrash()
        crash.x = x
        crash.y = y
        crash.z = z
        return crash

    def tilt_sensor_crash_equal_to_crash(self, crash1, crash2):
        return (crash1.x == crash2.x and crash1.y == crash2.y and crash1.z == crash2.z)

    def get_direction(self):
        if self.input_format != None:
            if self.input_format.mode != TiltSensorMode.TILT_SENSOR_MODE_TILT.value:
                return TiltSensorDirection.TILT_SENSOR_DIRECTION_UNKNOWN

        direction_int = self.get_number_from_value_data()
        if direction_int < 10:
            return TiltSensorDirection(direction_int)
        else:
            return TiltSensorDirection.TILT_SENSOR_DIRECTION_UNKNOWN

    def get_angle(self):
        if self.input_format.mode != TiltSensorMode.TILT_SENSOR_MODE_ANGLE.value:
            return self.tilt_sensor_angle_zero

        data_set_numbers = self.get_numbers_from_value_data_set()
        if len(data_set_numbers) == 2:
            return self.tilt_sensor_angle_make(data_set_numbers[0], data_set_numbers[1])

        return self.tilt_sensor_angle_zero

    def get_crash(self):
        if self.input_format.mode != TiltSensorMode.TILT_SENSOR_MODE_CRASH.value:
            return self.tilt_sensor_crash_zero

        data_set_numbers = self.get_numbers_from_value_data_set()
        if len(data_set_numbers) == 3:
            return self.tilt_sensor_crash_make(data_set_numbers[0], data_set_numbers[1], data_set_numbers[2])

        return self.tilt_sensor_crash_zero

    def add_valid_data_formats(self):
        self.add_valid_data_format(DataFormat.create("Angle", TiltSensorMode.TILT_SENSOR_MODE_ANGLE.value,
                                                     InputFormatUnit.INPUT_FORMAT_UNIT_RAW, 1, 2))
        self.add_valid_data_format(DataFormat.create("Angle", TiltSensorMode.TILT_SENSOR_MODE_ANGLE.value,
                                                     InputFormatUnit.INPUT_FORMAT_UNIT_PERCENTAGE, 1, 2))
        self.add_valid_data_format(DataFormat.create("Angle", TiltSensorMode.TILT_SENSOR_MODE_ANGLE.value,
                                                     InputFormatUnit.INPUT_FORMAT_UNIT_SI, 4, 2))
    
        self.add_valid_data_format(DataFormat.create("Tilt", TiltSensorMode.TILT_SENSOR_MODE_TILT.value,
                                                     InputFormatUnit.INPUT_FORMAT_UNIT_RAW, 1, 1))
        self.add_valid_data_format(DataFormat.create("Tilt", TiltSensorMode.TILT_SENSOR_MODE_TILT.value,
                                                     InputFormatUnit.INPUT_FORMAT_UNIT_PERCENTAGE, 1, 1))
        self.add_valid_data_format(DataFormat.create("Tilt", TiltSensorMode.TILT_SENSOR_MODE_TILT.value,
                                                     InputFormatUnit.INPUT_FORMAT_UNIT_SI, 4, 1))

        self.add_valid_data_format(DataFormat.create("Crash", TiltSensorMode.TILT_SENSOR_MODE_CRASH.value,
                                                     InputFormatUnit.INPUT_FORMAT_UNIT_RAW, 1, 3))
        self.add_valid_data_format(DataFormat.create("Crash", TiltSensorMode.TILT_SENSOR_MODE_CRASH.value,
                                                     InputFormatUnit.INPUT_FORMAT_UNIT_PERCENTAGE, 1, 3))
        self.add_valid_data_format(DataFormat.create("Crash", TiltSensorMode.TILT_SENSOR_MODE_CRASH.value,
                                                     InputFormatUnit.INPUT_FORMAT_UNIT_SI, 4, 3))

     
    # def handle_updated_value_data(value_data)

    # def handle_updated_input_format(input_format)
