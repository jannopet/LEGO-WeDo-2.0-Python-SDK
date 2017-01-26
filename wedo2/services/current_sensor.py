
from wedo2.services import lego_service
from lego_service import LegoService
from wedo2.input_output import input_format
from input_format import InputFormat
from input_format import InputFormatUnit


SERVICE_CURRENT_SENSOR_NAME = "Current Sensor"

class CurrentSensor(LegoService):

    def __init__(self, connect_info, io):
        super(CurrentSensor, self).__init__(connect_info, io)

    def get_service_name(self):
        return SERVICE_CURRENT_SENSOR_NAME

    def get_default_input_format(self):
        return InputFormat.input_format(self.connect_info.connect_id, self.connect_info.type_id,
                                        0, 30, InputFormatUnit.INPUT_FORMAT_UNIT_SI, True)

    def create_service(connect_info, io):
        return CurrentSensor(connect_info, io)

    def get_value_as_milliamps(self):
        if self.input_format != None:
            if self.input_format.mode == 0 and self.input_format.unit == InputFormatUnit.INPUT_FORMAT_UNIT_SI:
                return self.get_value_as_float()
            else:
                # LDSDKLogger.w("Can only retrieve milli amps from Current Sensor when ...")
                return 0
        return 0

    # def handle_updated_value_data(value_data)
