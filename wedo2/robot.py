
import pygatt
from wedo2.services.lego_service_factory import LegoServiceFactory
from wedo2.services.motor import Motor, MotorDirection
from wedo2.bluetooth.bluetooth_io import BluetoothIO
from wedo2.bluetooth import bluetooth_helper
from wedo2.bluetooth.connect_info import ConnectInfo, IOType
from wedo2.services.piezo_tone_player import PiezoTonePlayer, PiezoTonePlayerNote
from wedo2.services.rgb_light import RGBLightMode, Color


#HUB_CHARACTERISTIC_ATTACHED_IO = "0x1527"

class Robot:

    def __init__(self):
        self.adapter = pygatt.BGAPIBackend()
        try:
            self.adapter.start()
            print("Press the Smarthub power button")
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
        print("Connection ended")

    
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


    # MOTOR COMMANDS

    def turn_motor_left(self, power):
        motor = self.find_service(1)
        if motor != None:
            if self.power_is_positive(power):
                motor.run(MotorDirection.MOTOR_DIRECTION_LEFT, power)
        else:
            print("Motor is not available")

    def turn_motor_right(self, power):
        motor = self.find_service(1)
        if motor != None:
            if self.power_is_positive(power):
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

    def power_is_positive(self, power):
        if power >= 0:
            return True
        else:
            print("Invalid motor power value: motor power should be a positive value")
            return False


    # PIEZO TONE PLAYER COMMANDS

    """
    Takes three arguments: number of note (1 = C, 2 = C#, 3 = D, ..., 12 = B)
                           number of octave (1..6)
                           duration (0..65536 milliseconds)
    For example,
    to play a E note of 4th octave for 2 seconds, the command would be
    play_note(5, 4, 2000)
    """
    def play_note(self, note, octave, duration):
        piezo_tone_player = self.find_service(22)
        if piezo_tone_player != None:
            if note > 0 and note <= 12:
                if duration > 0:
                    piezo_tone_player.play_note(PiezoTonePlayerNote(note), octave, duration)
                else:
                    print("Invalid duration value: duration should be a positive number")
            else:
                print("Invalid note value: note value should be between 1 and 12")
        else:
            print("Piezo tone player is not available")

    """
    Takes two arguments: frequency (0..1500 Hz)
                         duration (0..65536 milliseconds)
    """
    def play_frequency(self, frequency, duration):
        piezo_tone_player = self.find_service(22)
        if piezo_tone_player != None:
            if frequency > 0 and duration > 0:
                piezo_tone_player.play_frequency(frequency, duration)
            else:
                print("Invalid values: frequency and duration should both be positive values")

    def stop_playing(self):
        piezo_tone_player = self.find_service(22)
        if piezo_tone_player != None:
            piezo_tone_player.stop_playing()
        else:
            print("Piezo tone player is not available")


    # RGB LIGHT COMMANDS

    def set_rgb_light_mode_to_discrete(self):
        rgb_light = self.find_service(23)
        if rgb_light != None:
            rgb_light.set_rgb_mode(RGBLightMode(0))

    def set_rgb_light_mode_to_absolute(self):
        rgb_light = self.find_service(23)
        if rgb_light != None:
            rgb_light.set_rgb_mode(RGBLightMode(1))

    def change_color_index(self, index):
        rgb_light = self.find_service(23)
        if rgb_light != None:
            rgb_light.set_color_index(index)

    def change_color(self, red, green, blue):
        rgb_light = self.find_service(23)
        if rgb_light != None:
            rgb_light.set_color(Color.rgb(red, green, blue))

    
