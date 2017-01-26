
from wedo2.services import lego_service
from lego_service import LegoService


SERVICE_GENERIC_NAME = "Generic IO"

class GenericService(LegoService):

    def __init__(self, connect_info, io):
        super(GenericService, self).__init__(connect_info, io)

    def get_service_name(self):
        return SERVICE_GENERIC_NAME

    def get_default_input_format(self):
        return None

    def create_service(connect_info, io):
        return GenericService(connect_info, io)

    
