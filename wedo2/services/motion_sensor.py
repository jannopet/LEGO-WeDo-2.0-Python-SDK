
from wedo2.services.lego_service import LegoService
from wedo2.bluetooth.connect_info import ConnectInfo
from wedo2.input_output.data_format import DataFormat
from wedo2.bluetooth.bluetooth_io import BluetoothIO
from wedo2.input_output.input_format import InputFormat, InputFormatUnit
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
        self.io.write_input_format(self.get_default_input_format(), connect_info.connect_id)

    def create_service(connect_info, io):
        return MotionSensor(connect_info, io)

    def get_service_name(self):
        return SERVICE_MOTION_SENSOR_NAME

    def get_default_input_format(self):
        return InputFormat.input_format(self.connect_info.connect_id, self.connect_info.type_id,
                                       0, 1, InputFormatUnit.INPUT_FORMAT_UNIT_SI, True)

    def add_valid_data_formats(self):
        self.add_valid_data_format(DataFormat.create("Detect", MotionSensorMode.MOTION_SENSOR_MODE_DETECT.value,
                                   InputFormatUnit.INPUT_FORMAT_UNIT_RAW.value, 1, 1))
        self.add_valid_data_format(DataFormat.create("Detect", MotionSensorMode.MOTION_SENSOR_MODE_DETECT.value,
                                   InputFormatUnit.INPUT_FORMAT_UNIT_PERCENTAGE.value, 1, 1))
        self.add_valid_data_format(DataFormat.create("Detect", MotionSensorMode.MOTION_SENSOR_MODE_DETECT.value,
                                   InputFormatUnit.INPUT_FORMAT_UNIT_SI.value, 4, 1))
        self.add_valid_data_format(DataFormat.create("Count", MotionSensorMode.MOTION_SENSOR_MODE_COUNT.value,
                                   InputFormatUnit.INPUT_FORMAT_UNIT_RAW.value, 4, 1))
        self.add_valid_data_format(DataFormat.create("Count", MotionSensorMode.MOTION_SENSOR_MODE_COUNT.value,
                                   InputFormatUnit.INPUT_FORMAT_UNIT_PERCENTAGE.value, 1, 1))
        self.add_valid_data_format(DataFormat.create("Count", MotionSensorMode.MOTION_SENSOR_MODE_COUNT.value,
                                   InputFormatUnit.INPUT_FORMAT_UNIT_SI.value, 4, 1))

    def get_distance(self):
        if self.get_motion_sensor_mode() != MotionSensorMode.MOTION_SENSOR_MODE_DETECT:
            return MAX_DISTANCE
        number = self.get_number_from_value_data(self.io.read_value_for_connect_id(self.connect_info.connect_id))
        if number != None:
            return number
        else:
            return MAX_DISTANCE

    def get_count(self):
        if self.get_motion_sensor_mode() != MotionSensorMode.MOTION_SENSOR_MODE_COUNT:
            return 0

        number = self.get_number_from_value_data(self.io.read_value_for_connect_id(self.connect_info.connect_id))
        if number != None:
            return number
        else:
            return 0
            

    def get_motion_sensor_mode(self):
        return MotionSensorMode(self.get_input_format_mode())

    def set_motion_sensor_mode(self, motion_sensor_mode):
        self.update_current_input_format_with_new_mode(motion_sensor_mode.value)

