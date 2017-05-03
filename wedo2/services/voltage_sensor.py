
from wedo2.services.lego_service import LegoService
from wedo2.input_output.input_format import InputFormat, InputFormatUnit

SERVICE_VOLTAGE_SENSOR_NAME = "Voltage Sensor"


class VoltageSensor(LegoService):

    def __init__(self, connect_info, io):
        super(VoltageSensor, self).__init__(connect_info, io)
        self.io.write_input_format(self.get_default_input_format(), connect_info.connect_id)

    def get_service_name(self):
        return SERVICE_VOLTAGE_SENSOR_NAME

    def get_default_input_format(self):
        return InputFormat.input_format(self.connect_info.connect_id, self.connect_info.type_id,
                                        0, 30, InputFormatUnit.INPUT_FORMAT_UNIT_SI, True)

    def create_service(connect_info, io):
        return VoltageSensor(connect_info, io)

    def get_value_as_millivolts(self):
        if self.input_format.mode == 0 and self.input_format.unit == InputFormatUnit.INPUT_FORMAT_UNIT_SI.value:
            return self.get_float_from_data(self.io.read_value_for_connect_id(self.connect_info.connect_id))
        else:
            return 0
