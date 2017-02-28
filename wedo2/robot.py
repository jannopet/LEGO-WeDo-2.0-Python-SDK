
import pygatt
from wedo2.services.lego_service_factory import LegoServiceFactory
from wedo2.services.motor import Motor, MotorDirection
from wedo2.bluetooth.bluetooth_io import BluetoothIO
from wedo2.bluetooth import bluetooth_helper
from wedo2.bluetooth.connect_info import ConnectInfo, IOType


#HUB_CHARACTERISTIC_ATTACHED_IO = "0x1527"

class Robot:

    def __init__(self):
        self.adapter = pygatt.BGAPIBackend()
        try:
            self.adapter.start()
            devices = self.adapter.scan()
            device_address = devices[0]['address']
            print(device_address)
            device = None
            while True:
                try:
                    device = self.adapter.connect(device_address)
                    self.device = device
                    break
                except:
                    print("Trying to connect to device...")
            self.io = BluetoothIO(self.device)
            self.services = self.populate_available_services(self.io)
        except:
            print("Robot instance was not correctly initalized")
            
    def stop(self):
        self.adapter.stop()
        print("Connection to robot finished")

    
    def find_attached_io(self):
        uuid = bluetooth_helper.uuid_with_prefix_custom_base(HUB_CHARACTERISTIC_ATTACHED_IO)
        data = self.device.char_read(uuid)
        return handle_attached_io_data(data)

    def handle_attached_io_data(data):
        services = set()
        if len(data) < 2:
            print("Something went wrong when retrieving attached io data")

        connect_id = data[0:1][0]
        attached = data[1:2][0]

        if attached == 1:
            hub_index = data[2:3][0]
            io_type = data[3:4][0]
            # We could also get information about hardware and firmware here (revision)

            connect_info = ConnectInfo(connect_id, hub_index, io_type)

            service = LegoServiceFactory.create(connect_info, self.io)
            services.add(service)

        return services

    def populate_available_services(self, io):
        services = set()
        motor_info = ConnectInfo(2, 1, 1)
        piezo_info = ConnectInfo(5, 4, 22)
        rgb_info = ConnectInfo(6, 5, 23)
        
        motor = LegoServiceFactory.create(motor_info, io)
        piezo_tone_player = LegoServiceFactory.create(piezo_info, io)
        rgb_light = LegoServiceFactory.create(rgb_info, io)

        services.add(motor)
        services.add(piezo_tone_player)
        services.add(rgb_light)
        return services

    def find_service(self, io_type):
        for service in self.services:
            if service.connect_info.type_id == io_type:
                return service
        return None

    def turn_motor_left(self, power):
        motor = self.find_service(1)
        if motor != None:
            motor.run(MotorDirection.MOTOR_DIRECTION_LEFT, power)
        else:
            print("Motor is not available")

    def turn_motor_right(self, power):
        motor = self.find_service(1)
        if motor != None:
            motor.run(MotorDirection.MOTOR_DIRECTION_RIGHT, power)
        else:
            print("Motor is not available")

    def motor_brake(self):
        motor = self.find_service(1)
        if motor != None:
            motor.brake()
        else:
            print("Motor is not available")

    def motor_drift(self):
        motor = self.find_service(1)
        if motor != None:
            motor.drift()
        else:
            print("Motor is not available")

        

    
