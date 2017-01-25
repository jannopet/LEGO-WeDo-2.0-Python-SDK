
from wedo2.input_output import lego_service
from lego_service import LegoService
from wedo2.device import connect_info
from wedo2.input_output import data_format
from data_format import DataFormat
from wedo2.input_output import io
from wedo2.input_output import input_format
from input_format import InputFormat
from input_format import InputFormatUnit
from enum import Enum

SERVICE_MOTION_SENSOR_NAME = "Motion Sensor"
MAX_DISTANCE = 10
MIN_DISTANCE = 0

class MotionSensorMode(Enum):
    MOTION_SENSOR_MODE_DETECT = 0
    MOTION_SENSOR_MODE_COUNT = 1
    MOTION_SENSOR_MODE_UNKNOWN = 2


class MotionSensor(LegoService):

    def __init__(self, connect_info, io):
        super(MotionSensor, self).__init__(connect_info, io)
        self.add_valid_data_formats()
        self.input_format = None    # So that self.input_format != None would be checkable

    def create_service(connect_info, io):
        return MotionSensor(connect_info, io)

    def get_service_name(self):
        return SERVICE_MOTION_SENSOR_NAME

    def get_default_input_format(self):
        return InputFormat.inputFormat(self.connect_info.connect_id, self.connect_info.type_id,
                                       0, 1, InputFormatUnit.INPUT_FORMAT_UNIT_SI, True)

    def add_valid_data_formats(self):
        self.add_valid_data_format(DataFormat.create("Detect", MotionSensorMode.MOTION_SENSOR_MODE_DETECT.value,
                                   InputFormatUnit.INPUT_FORMAT_UNIT_RAW, 1, 1))
        self.add_valid_data_format(DataFormat.create("Detect", MotionSensorMode.MOTION_SENSOR_MODE_DETECT.value,
                                   InputFormatUnit.INPUT_FORMAT_UNIT_PERCENTAGE, 1, 1))
        self.add_valid_data_format(DataFormat.create("Detect", MotionSensorMode.MOTION_SENSOR_MODE_DETECT.value,
                                   InputFormatUnit.INPUT_FORMAT_UNIT_SI, 4, 1))
        self.add_valid_data_format(DataFormat.create("Count", MotionSensorMode.MOTION_SENSOR_MODE_COUNT.value,
                                   InputFormatUnit.INPUT_FORMAT_UNIT_RAW, 4, 1))
        self.add_valid_data_format(DataFormat.create("Count", MotionSensorMode.MOTION_SENSOR_MODE_COUNT.value,
                                   InputFormatUnit.INPUT_FORMAT_UNIT_PERCENTAGE, 1, 1))
        self.add_valid_data_format(DataFormat.create("Count", MotionSensorMode.MOTION_SENSOR_MODE_COUNT.value,
                                   InputFormatUnit.INPUT_FORMAT_UNIT_SI, 4, 1))

    def get_distance(self):
        if self.get_motion_sensor_mode() != MotionSensorMode.MOTION_SENSOR_MODE_DETECT:
            return 0

        number = self.get_number_from_value_data()
        if number != None:
            return number   # number.floatValue() in Java
        else:
            return 0

    def get_count(self):
        if self.get_motion_sensor_mode() != MotionSensorMode.MOTION_SENSOR_MODE_COUNT:
            return 0

        number = self.get_number_from_value_data()
        if number != None:
            return number   # number.intValue() in Java
        else:
            return 0
            

    def get_motion_sensor_mode(self):
        return MotionSensorMode(self.get_input_format_mode())

    def set_motion_sensor_mode(self, motion_sensor_mode):
        self.update_current_input_format_with_new_mode(motion_sensor_mode.value)

   # def handle_updated_value_data(self, value_data):

    # def __eq__(self, obj){return super.equals(o)}


