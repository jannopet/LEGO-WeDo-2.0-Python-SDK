
from wedo2.input_output import io
from wedo2.input_output import data_format
from wedo2.input_output import input_format
from wedo2.device import connect_info
from wedo2.device import lego_device

FIRST_INTERNAL_HUB_INDEX = 50

class LegoService(object):

    def __init__(self, connect_info, io):
        assert connect_info != None, "Cannot instantiate service with null ConnectInfo"
        assert io != None, "Cannot instantiate service with null IO"

        self.connect_info = connect_info
        self.io = io
        self.valid_data_formats = set()

    def create_service(connect_info, io):
        return LegoService(connect_info, io)

    def set_device(self, device):
        self.device = device

    def is_internal_service(self):
        return self.connect_info.hub_index >= FIRST_INTERNAL_HUB_INDEX

    # didRequestConnectInfo(io){return this.connectInfo}

    def verify_data(self, *args):
        if len(args) == 1:
            data = args[0]
            # CHECK, WHETHER data != None is okay here
            if data != None and len(self.valid_data_formats) != 0:
                d_format = self.data_format_for_input_format(self.input_format)
                if d_format == None:
                    raise Exception("Did not find a valid input data format")

                self.verify_data(data, d_format)
                
        elif len(args) == 2:
            data = args[0]
            d_format = args[1]
            if len(data) != (d_format.dataset_size * d_format.dataset_count):
                raise Exception("Package sizes don't add up. Something is wrong")

    def data_format_for_input_format(self, i_format):
        for d_format in self.valid_data_formats:
            if d_format.mode == i_format.mode and d_format.unit == i_format.unit:
                if (d_format.dataset_size * d_format.dataset_count) != i_format.number_of_bytes:
                    #raise Exception("Data length doesn't add up. Something went wrong")
                    return None
                return d_format
        return None

    def get_service_name(self):
        return "Undefined"

    def get_default_input_format(self):
        return None

    def update_input_format(self, new_format):
        self.io.write_input_format(new_format, self.connect_info.connect_id)


    # Check with various services, if this works as intended
    def get_input_format_mode(self):
        if self.input_format != None:
            return self.input_format.mode
        elif self.get_default_input_format() != None:
            return self.get_default_input_format().mode
        # LDSDKLogger.d("No input format set, returning mode 0")
        return 0


    def update_current_input_format_with_new_mode(self, new_mode):
        if self.input_format != None:
            self.update_input_format(self.input_format.input_format_by_setting_mode(new_mode))
        elif self.get_default_input_format() != None:
            self.update_input_format(self.get_default_input_format().input_format_by_setting_mode(new_mode))
        else:
            # LDSDKLogger.e("tried to update input format ...")
                    

    def add_valid_data_format(self, d_format):
        assert d_format != None, "DataFormat cannot be None"
        self.valid_data_formats.add(d_format)

    def remove_valid_data_format(self, d_format):
        assert d_format != None, "DataFormat cannot be None"
        if len(self.valid_data_formats == 0):
            return
        self.valid_data_formats.remove(d_format)

    # Jällegi, siin tagastatakse valueData.clone()
    def get_value_data(self): 
        return None

    # 0 or 1 argument
    def get_number_from_value_data(self, *args):
        return None

    # 0 or 1 argument
    def get_numbers_from_value_data_set(self, *args):
        return None
    
    def get_float_from_data(data):
        return None

    def get_integer_from_data(data):
        return None

    def get_value_as_integer():
        return None

    def get_value_as_float():
        return None

    def send_read_value_request():
        return None

    def send_reset_value_request():
        return None

    def send_reset_state_request():
        return None

    def write_data(self, data):
        return None

    # didReceiveInputFormat(io, inputFormat)

    # handleUpdatedInputFormat(inputFormat)

    # didReceiveValueData(io, valueData)

    # handleUpdatedValueData(valueData)

    # registerCallbackListener(listener)

    # unregisterCallbackListener(listener)

    def __eq__(self, obj):
        return None

    def __ne__(self, obj):
        return None

    
    
        
