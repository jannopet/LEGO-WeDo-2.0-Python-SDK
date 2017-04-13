
import pygatt
from wedo2.services.lego_service_factory import LegoServiceFactory
from wedo2.services.motor import Motor, MotorDirection
from wedo2.bluetooth.bluetooth_io import BluetoothIO
from wedo2.bluetooth import bluetooth_helper
from wedo2.bluetooth.connect_info import ConnectInfo, IOType
from wedo2.services.piezo_tone_player import PiezoTonePlayer, PiezoTonePlayerNote
from wedo2.services.rgb_light import RGBLightMode, Color
from wedo2.services.tilt_sensor import TiltSensorMode, TiltSensorDirection, TiltSensorAngle
from wedo2.services.motion_sensor import MotionSensorMode


#HUB_CHARACTERISTIC_ATTACHED_IO = "0x1527"

class Robot:

    def __init__(self):
        self.adapter = pygatt.BGAPIBackend()
        try:
            self.adapter.start()
            print("Press the Smarthub power button")
            devices = self.adapter.scan()
            devices = sorted(devices, key=lambda k: k['rssi'], reverse=True)
            device_address = devices[0]['address']
            print(device_address)
            device = None
            while True:
                try:
                    # A0:E6:F8:1E:1B:65
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
        #motor_info = ConnectInfo(2, 1, IO_TYPE.IO_TYPE_MOTOR.value)
        piezo_info = ConnectInfo(5, 4, IOType.IO_TYPE_PIEZO_TONE_PLAYER.value)
        rgb_info = ConnectInfo(6, 5, IOType.IO_TYPE_RGB_LIGHT.value)
        tilt_info = ConnectInfo(2, 1, IOType.IO_TYPE_TILT_SENSOR.value)
        motion_info = ConnectInfo(1, 0, IOType.IO_TYPE_MOTION_SENSOR.value)
        
        #motor = LegoServiceFactory.create(motor_info, io)
        piezo_tone_player = LegoServiceFactory.create(piezo_info, io)
        rgb_light = LegoServiceFactory.create(rgb_info, io)
        tilt_sensor = LegoServiceFactory.create(tilt_info, io)
        motion_sensor = LegoServiceFactory.create(motion_info, io)

        #services.add(motor)
        services.add(piezo_tone_player)
        services.add(rgb_light)
        services.add(tilt_sensor)
        services.add(motion_sensor)
        return services

    def find_service(self, io_type):
        for service in self.services:
            if service.connect_info.type_id == io_type.value:
                return service
        return None


    # MOTOR COMMANDS

    def turn_motor_left(self, power):
        motor = self.find_service(IOType.IO_TYPE_MOTOR)
        if motor != None:
            if self.power_is_positive(power):
                motor.run(MotorDirection.MOTOR_DIRECTION_LEFT, power)
        else:
            print("Motor is not available")

    def turn_motor_right(self, power):
        motor = self.find_service(IOType.IO_TYPE_MOTOR)
        if motor != None:
            if self.power_is_positive(power):
                motor.run(MotorDirection.MOTOR_DIRECTION_RIGHT, power)
        else:
            print("Motor is not available")

    def motor_brake(self):
        motor = self.find_service(IOType.IO_TYPE_MOTOR)
        if motor != None:
            motor.brake()
        else:
            print("Motor is not available")

    def motor_drift(self):
        motor = self.find_service(IOType.IO_TYPE_MOTOR)
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
        piezo_tone_player = self.find_service(IOType.IO_TYPE_PIEZO_TONE_PLAYER)
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
        piezo_tone_player = self.find_service(IOType.IO_TYPE_PIEZO_TONE_PLAYER)
        if piezo_tone_player != None:
            if frequency > 0 and duration > 0:
                piezo_tone_player.play_frequency(frequency, duration)
            else:
                print("Invalid values: frequency and duration should both be positive values")

    def stop_playing(self):
        piezo_tone_player = self.find_service(IOType.IO_TYPE_PIEZO_TONE_PLAYER)
        if piezo_tone_player != None:
            piezo_tone_player.stop_playing()
        else:
            print("Piezo tone player is not available")


    # RGB LIGHT COMMANDS

    def set_rgb_light_mode_to_discrete(self):
        rgb_light = self.find_service(IOType.IO_TYPE_RGB_LIGHT)
        if rgb_light != None:
            rgb_light.set_rgb_mode(RGBLightMode(0))
        else:
            print("RGB Light is not available")

    def set_rgb_light_mode_to_absolute(self):
        rgb_light = self.find_service(IOType.IO_TYPE_RGB_LIGHT)
        if rgb_light != None:
            rgb_light.set_rgb_mode(RGBLightMode(1))
        else:
            print("RGB Light is not available")

    def change_color_index(self, index):
        rgb_light = self.find_service(IOType.IO_TYPE_RGB_LIGHT)
        if rgb_light != None:
            rgb_light.set_color_index(index)
        else:
            print("RGB Light is not available")

    def change_color(self, red, green, blue):
        rgb_light = self.find_service(IOType.IO_TYPE_RGB_LIGHT)
        if rgb_light != None:
            rgb_light.set_color(Color.rgb(red, green, blue))
        else:
            print("RGB Light is not available")


    # TILT SENSOR COMMANDS

    def set_tilt_mode_to_direction(self):
        tilt_sensor = self.find_service(IOType.IO_TYPE_TILT_SENSOR)
        if tilt_sensor != None:
            tilt_sensor.set_tilt_sensor_mode(TiltSensorMode.TILT_SENSOR_MODE_TILT)
        else:
            print("Tilt Sensor is not available")

    def set_tilt_mode_to_angle(self):
        tilt_sensor = self.find_service(IOType.IO_TYPE_TILT_SENSOR)
        if tilt_sensor != None:
            tilt_sensor.set_tilt_sensor_mode(TiltSensorMode.TILT_SENSOR_MODE_ANGLE)
        else:
            print("Tilt Sensor is not available")

    """
    Depending on the current mode (Tilt or Angle), will return either
    1) an Enum value of TiltSensorDirection
    2) an instance of TiltSensorAngle, which holds two variables: x and y,
       which hold information about the angle that the Tilt Sensor is holding
    """
    def get_tilt(self):
        tilt_sensor = self.find_service(IOType.IO_TYPE_TILT_SENSOR)
        if tilt_sensor != None:
            if tilt_sensor.tilt_sensor_mode == TiltSensorMode.TILT_SENSOR_MODE_TILT.value:
                direction = tilt_sensor.get_direction()
                return direction
            elif tilt_sensor.tilt_sensor_mode == TiltSensorMode.TILT_SENSOR_MODE_ANGLE.value:
                angle = tilt_sensor.get_angle()
                return angle
            else:
                print("Unknown Tilt Sensor mode.")
        else:
            print("Tilt Sensor is not available")


    # MOTION SENSOR COMMANDS

    def set_motion_sensor_to_detect(self):
        motion_sensor = self.find_service(IOType.IO_TYPE_MOTION_SENSOR)
        if motion_sensor != None:
            motion_sensor.set_motion_sensor_mode(MotionSensorMode.MOTION_SENSOR_MODE_DETECT)
        else:
            print("Motion Sensor is not available")

    def set_motion_sensor_to_count(self):
        motion_sensor = self.find_service(IOType.IO_TYPE_MOTION_SENSOR)
        if motion_sensor != None:
            motion_sensor.set_motion_sensor_mode(MotionSensorMode.MOTION_SENSOR_MODE_COUNT)
        else:
            print("Motion Sensor is not available")

    def get_object_distance(self):
        motion_sensor = self.find_service(IOType.IO_TYPE_MOTION_SENSOR)
        if motion_sensor != None:
            if motion_sensor.get_motion_sensor_mode() == MotionSensorMode.MOTION_SENSOR_MODE_DETECT:
                distance = motion_sensor.get_distance()
                return distance
            else:
                print("Cannot return a value. Motion sensor must be set to Detect Mode")
                return None
        else:
            print("Motion Sensor is not available")
            return None

    def get_motion_count(self):
        motion_sensor = self.find_service(IOType.IO_TYPE_MOTION_SENSOR)
        if motion_sensor != None:
            if motion_sensor.get_motion_sensor_mode() == MotionSensorMode.MOTION_SENSOR_MODE_COUNT:
                count = motion_sensor.get_count()
                return count
            else:
                print("Cannot return a value. Motion sensor must be set to Detect Mode")
                return None
        else:
            print("Motion Sensor is not available")
            return None
