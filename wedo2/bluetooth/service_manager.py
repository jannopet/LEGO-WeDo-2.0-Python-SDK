
from wedo2.bluetooth import bluetooth_helper
from wedo2.bluetooth.connect_info import ConnectInfo
from wedo2.services.lego_service_factory import LegoServiceFactory

HUB_CHARACTERISTIC_ATTACHED_IO = "0x1527"


class ServiceManager:

    def __init__(self, io):
        self.io = io
        self.services = set()
        self.services_data = {}
        self.find_available_services()

    def find_available_services(self):
        attached_io_uuid = bluetooth_helper.uuid_with_prefix_custom_base(HUB_CHARACTERISTIC_ATTACHED_IO)
        self.io.subscribe_to_char(attached_io_uuid, self.handle_attached_io_data)
        
        # End subscription when the service for port 6 (RGB LED light) has been found
        while 6 not in self.services_data.keys():
            pass
            
        self.io.unsubscribe_from_char(attached_io_uuid)
        self.create_services(self.services_data)

    def create_services(self, services_data):
        for connect_id in services_data.keys():
            connect_info = services_data[connect_id]
            service = LegoServiceFactory.create(connect_info, self.io)
            self.services.add(service)

    def find_service(self, io_type):
        for service in self.services:
            if service.connect_info.type_id == io_type.value:
                return service
        return None

    def handle_attached_io_data(self, handle, data):
        if len(data) < 2:
            print("Something went wrong when retrieving attached io data")

        connect_id = data[0:1][0]
        attached = data[1:2][0]
        
        if attached == 1:
            hub_index = data[2:3][0]
            io_type = data[3:4][0]
            connect_info = ConnectInfo(connect_id, hub_index, io_type)
            
            self.services_data[connect_id] = connect_info
