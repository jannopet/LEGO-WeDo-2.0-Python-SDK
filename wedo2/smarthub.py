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
from wedo2.bluetooth.service_manager import ServiceManager


class Smarthub:

    def __init__(self):
        self.adapter = pygatt.BGAPIBackend()
        try:
            self.adapter.start()
            print("Press the Smarthub power button")
            devices = self.adapter.scan()
            devices = sorted(devices, key=lambda k: k['rssi'], reverse=True)
            self.device_address = devices[0]['address']
            print(self.device_address)
            device = None
            while True:
                try:
                    device = self.adapter.connect(self.device_address)
                    self.device = device
                    break
                except:
                    print("Trying to connect to device...")
                    
            self.io = BluetoothIO(self.device)
            self.service_manager = ServiceManager(self.io)
            
        except Exception as e:
            print(str(e))
            print("Robot instance was not correctly initalized")
       
            
    def disconnect(self):
        self.adapter.stop()
        print("Connection ended")

    # MOTOR COMMANDS

    def turn_motor(self, power):
        motor = self.service_manager.find_service(IOType.IO_TYPE_MOTOR)
        if motor != None:
            if power >= 0:
                motor.run(MotorDirection.MOTOR_DIRECTION_RIGHT, power)
            else:
                motor.run(MotorDirection.MOTOR_DIRECTION_LEFT, abs(power))
        else:
            print("Motor is not available")

    def turn_motor_left(self, power):
        motor = self.service_manager.find_service(IOType.IO_TYPE_MOTOR)
        if motor != None:
            if self.power_is_positive(power):
                motor.run(MotorDirection.MOTOR_DIRECTION_LEFT, power)
        else:
            print("Motor is not available")

    def turn_motor_right(self, power):
        motor = self.service_manager.find_service(IOType.IO_TYPE_MOTOR)
        if motor != None:
            if self.power_is_positive(power):
                motor.run(MotorDirection.MOTOR_DIRECTION_RIGHT, power)
        else:
            print("Motor is not available")

    def motor_brake(self):
        motor = self.service_manager.find_service(IOType.IO_TYPE_MOTOR)
        if motor != None:
            motor.brake()
        else:
            print("Motor is not available")

    def motor_drift(self):
        motor = self.service_manager.find_service(IOType.IO_TYPE_MOTOR)
        if motor != None:
            motor.drift()
        else:
            print("Motor is not available")
            

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
        piezo_tone_player = self.service_manager.find_service(IOType.IO_TYPE_PIEZO_TONE_PLAYER)
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
        piezo_tone_player = self.service_manager.find_service(IOType.IO_TYPE_PIEZO_TONE_PLAYER)
        if piezo_tone_player != None:
            if frequency > 0 and duration > 0:
                piezo_tone_player.play_frequency(frequency, duration)
            else:
                print("Invalid values: frequency and duration should both be positive values")

    def stop_playing(self):
        piezo_tone_player = self.service_manager.find_service(IOType.IO_TYPE_PIEZO_TONE_PLAYER)
        if piezo_tone_player != None:
            piezo_tone_player.stop_playing()
        else:
            print("Piezo tone player is not available")


    # RGB LIGHT COMMANDS

    def set_rgb_light_mode_to_discrete(self):
        rgb_light = self.service_manager.find_service(IOType.IO_TYPE_RGB_LIGHT)
        if rgb_light != None:
            rgb_light.set_rgb_mode(RGBLightMode(0))
        else:
            print("RGB Light is not available")

    def set_rgb_light_mode_to_absolute(self):
        rgb_light = self.service_manager.find_service(IOType.IO_TYPE_RGB_LIGHT)
        if rgb_light != None:
            rgb_light.set_rgb_mode(RGBLightMode(1))
        else:
            print("RGB Light is not available")

    def change_color_index(self, index):
        rgb_light = self.service_manager.find_service(IOType.IO_TYPE_RGB_LIGHT)
        if rgb_light != None:
            rgb_light.set_color_index(index)
        else:
            print("RGB Light is not available")

    def change_color(self, red, green, blue):
        rgb_light = self.service_manager.find_service(IOType.IO_TYPE_RGB_LIGHT)
        if rgb_light != None:
            rgb_light.set_color(Color.rgb(red, green, blue))
        else:
            print("RGB Light is not available")


    # TILT SENSOR COMMANDS

    def set_tilt_mode_to_direction(self):
        tilt_sensor = self.service_manager.find_service(IOType.IO_TYPE_TILT_SENSOR)
        if tilt_sensor != None:
            tilt_sensor.set_tilt_sensor_mode(TiltSensorMode.TILT_SENSOR_MODE_TILT)
        else:
            print("Tilt Sensor is not available")

    def set_tilt_mode_to_angle(self):
        tilt_sensor = self.service_manager.find_service(IOType.IO_TYPE_TILT_SENSOR)
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
        tilt_sensor = self.service_manager.find_service(IOType.IO_TYPE_TILT_SENSOR)
        if tilt_sensor != None:
            if tilt_sensor.tilt_sensor_mode == TiltSensorMode.TILT_SENSOR_MODE_TILT.value:
                direction = tilt_sensor.get_direction()
                return direction
            elif tilt_sensor.tilt_sensor_mode == TiltSensorMode.TILT_SENSOR_MODE_ANGLE.value:
                angle = tilt_sensor.get_angle()
                return (angle.x, angle.y)
            else:
                print("Unknown Tilt Sensor mode.")
        else:
            print("Tilt Sensor is not available")


    # MOTION SENSOR COMMANDS

    def set_motion_sensor_to_detect(self):
        motion_sensor = self.service_manager.find_service(IOType.IO_TYPE_MOTION_SENSOR)
        if motion_sensor != None:
            motion_sensor.set_motion_sensor_mode(MotionSensorMode.MOTION_SENSOR_MODE_DETECT)
        else:
            print("Motion Sensor is not available")

    def set_motion_sensor_to_count(self):
        motion_sensor = self.service_manager.find_service(IOType.IO_TYPE_MOTION_SENSOR)
        if motion_sensor != None:
            motion_sensor.set_motion_sensor_mode(MotionSensorMode.MOTION_SENSOR_MODE_COUNT)
        else:
            print("Motion Sensor is not available")

    def get_object_distance(self):
        motion_sensor = self.service_manager.find_service(IOType.IO_TYPE_MOTION_SENSOR)
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
        motion_sensor = self.service_manager.find_service(IOType.IO_TYPE_MOTION_SENSOR)
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
