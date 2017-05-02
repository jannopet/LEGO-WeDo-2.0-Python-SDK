import pygatt
from wedo2.services.lego_service_factory import LegoServiceFactory
from wedo2.services.motor import Motor, MotorDirection
from wedo2.bluetooth.bluetooth_io import BluetoothIO
from wedo2.bluetooth import bluetooth_helper
from wedo2.bluetooth.connect_info import ConnectInfo, IOType
from wedo2.services.piezo_tone_player import PiezoTonePlayer, PiezoTonePlayerNote
from wedo2.services.rgb_light import RGBLightMode
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
            device_name = devices[0]['name']
            print("Connecting to device '{}'".format(device_name))
            device = None
            while True:
                try:
                    device = self.adapter.connect(self.device_address)
                    self.device = device
                    break
                except:
                    print("Trying to connect to device. Try pressing the Smarthub power button again")
                    
            self.io = BluetoothIO(self.device)
            self.service_manager = ServiceManager(self.io)
            input("Press Enter to continue")
        except Exception as e:
            print(str(e))
            print("Smarthub instance was not correctly initialized")
       
            
    def disconnect(self):
        self.adapter.stop()
        print("Connection ended")

    # MOTOR COMMANDS

    """
    Takes one argument: power (-100..100)
    The sign of the power decides the direction, in which the motor will
    start to turn: negative values turn motor counterclockwise
                   positive values turn motor clockwise
    """
    def turn_motor(self, power):
        motor = self.service_manager.find_service(IOType.IO_TYPE_MOTOR)
        if motor != None:
            if power >= 0:
                motor.run(MotorDirection.MOTOR_DIRECTION_RIGHT, power)
            else:
                motor.run(MotorDirection.MOTOR_DIRECTION_LEFT, abs(power))
        else:
            print("Motor is not available")

    """
    Makes the motor instantly stop
    """
    def motor_brake(self):
        motor = self.service_manager.find_service(IOType.IO_TYPE_MOTOR)
        if motor != None:
            motor.brake()
        else:
            print("Motor is not available")

    """
    Stops the motor from turning, but not instantly - inertia can still keep
    it going for a small amount of time
    """
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

    """
    If Smarthub is currently playing a tone, it will stop playing it
    """
    def stop_playing(self):
        piezo_tone_player = self.service_manager.find_service(IOType.IO_TYPE_PIEZO_TONE_PLAYER)
        if piezo_tone_player != None:
            piezo_tone_player.stop_playing()
        else:
            print("Piezo tone player is not available")


    # RGB LIGHT COMMANDS

    """
    Changes the RGB Light to Discrete Mode, which makes it possible to use
    function change_color_index(index)
    This is also the default mode for RGB Light
    """
    def set_rgb_light_mode_to_discrete(self):
        rgb_light = self.service_manager.find_service(IOType.IO_TYPE_RGB_LIGHT)
        if rgb_light != None:
            rgb_light.set_rgb_mode(RGBLightMode(0))
        else:
            print("RGB Light is not available")

    """
    Changes the RGB Light to Absolute Mode, which makes it possible to use
    function change_color( red, green, blue )
    """
    def set_rgb_light_mode_to_absolute(self):
        rgb_light = self.service_manager.find_service(IOType.IO_TYPE_RGB_LIGHT)
        if rgb_light != None:
            rgb_light.set_rgb_mode(RGBLightMode(1))
        else:
            print("RGB Light is not available")

    """
    Changes Smarthub LED light color according to a predefined index
    Takes one argument: index (0..10), where
       0 - No Light
       1 - Pink
       2 - Purple
       3 - Dark Blue
       4 - Light Blue
       5 - Light Green
       6 - Dark Green
       7 - Yellow
       8 - Orange
       9 - Red
      10 - White
    """
    def change_color_index(self, index):
        rgb_light = self.service_manager.find_service(IOType.IO_TYPE_RGB_LIGHT)
        if rgb_light != None:
            rgb_light.set_color_index(index)
        else:
            print("RGB Light is not available")

    """
    Changes Smarthub LED light color with RGB values
    Takes three arguments: red (0..255)
                           green (0..255)
                           blue (0..255)
    """
    def change_color(self, red, green, blue):
        rgb_light = self.service_manager.find_service(IOType.IO_TYPE_RGB_LIGHT)
        if rgb_light != None:
            rgb_light.set_color(red, green, blue)
        else:
            print("RGB Light is not available")


    # TILT SENSOR COMMANDS

    """
    Changes the Tilt Sensor to Discrete Mode, which will make function get_tilt()
    return an Enum value as the current tilt direction
    """
    def set_tilt_mode_to_direction(self):
        tilt_sensor = self.service_manager.find_service(IOType.IO_TYPE_TILT_SENSOR)
        if tilt_sensor != None:
            tilt_sensor.set_tilt_sensor_mode(TiltSensorMode.TILT_SENSOR_MODE_TILT)
        else:
            print("Tilt Sensor is not available")

    """
    Changes the Tilt Sensor to Angle Mode, which will make function get_tilt()
    return a tuple (x, y) as the current tilt of the Tilt Sensor
    """
    def set_tilt_mode_to_angle(self):
        tilt_sensor = self.service_manager.find_service(IOType.IO_TYPE_TILT_SENSOR)
        if tilt_sensor != None:
            tilt_sensor.set_tilt_sensor_mode(TiltSensorMode.TILT_SENSOR_MODE_ANGLE)
        else:
            print("Tilt Sensor is not available")

    """
    Depending on the current mode (Tilt or Angle), will return either
    1) an Enum value of TiltSensorDirection, where:
       0 - No Tilt
       3 - Tilted backward
       5 - Tilted to the right
       7 - Tilted to the left
       9 - Tilted forward
      10 - Unknown Tilt
      
    2) a tuple (x, y), where
       x - the angle at which the Tilt Sensor is tilted left (-45..0 degrees)
           or right (0..45 degrees)
       y - the angle at which the Tilt Sensor is tilted backward (-45..0 degrees)
           or forward (0..45 degrees)                                         
    """
    def get_tilt(self):
        tilt_sensor = self.service_manager.find_service(IOType.IO_TYPE_TILT_SENSOR)
        if tilt_sensor != None:
            if tilt_sensor.tilt_sensor_mode == TiltSensorMode.TILT_SENSOR_MODE_TILT.value:
                direction = tilt_sensor.get_direction().value
                return direction
            elif tilt_sensor.tilt_sensor_mode == TiltSensorMode.TILT_SENSOR_MODE_ANGLE.value:
                angle = tilt_sensor.get_angle()
                return (angle.x, angle.y)
            else:
                print("Unknown Tilt Sensor mode.")
        else:
            print("Tilt Sensor is not available")


    # MOTION SENSOR COMMANDS

    """
    Changes the Motion Sensor to Detect Mode, which makes it possible to use
    function get_object_distance()
    This is also the default mode for Motion Sensor
    """
    def set_motion_sensor_to_detect(self):
        motion_sensor = self.service_manager.find_service(IOType.IO_TYPE_MOTION_SENSOR)
        if motion_sensor != None:
            motion_sensor.set_motion_sensor_mode(MotionSensorMode.MOTION_SENSOR_MODE_DETECT)
        else:
            print("Motion Sensor is not available")

    """
    Changes the Motion Sensor to Count Mode, which makes it possible to use
    function get_object_count()
    From the moment it is changed to Count Mode, Smarthub will start counting
    the objects which have moved in front of it
    """
    def set_motion_sensor_to_count(self):
        motion_sensor = self.service_manager.find_service(IOType.IO_TYPE_MOTION_SENSOR)
        if motion_sensor != None:
            motion_sensor.set_motion_sensor_mode(MotionSensorMode.MOTION_SENSOR_MODE_COUNT)
        else:
            print("Motion Sensor is not available")

    """
    Returns the distance of the object in front of the Motion Sensor
    Returns a value between 0 and 9, and if no object is seen, returns 10
    """
    def get_object_distance(self):
        motion_sensor = self.service_manager.find_service(IOType.IO_TYPE_MOTION_SENSOR)
        if motion_sensor != None:
            distance = motion_sensor.get_distance()
            return distance
        else:
            print("Motion Sensor is not available")
            return None

    """
    Returns the count of objects which have moved in front of the Motion Sensor.
    The counting starts when Motion Sensor is set to Count Mode.
    """
    def get_motion_count(self):
        motion_sensor = self.service_manager.find_service(IOType.IO_TYPE_MOTION_SENSOR)
        if motion_sensor != None:
            count = motion_sensor.get_count()
            return count
        else:
            print("Motion Sensor is not available")
            return None


    # VOLTAGE AND CURRENT COMMANDS

    """
    Returns the voltage of the Smarthub battery in millivolts
    """
    def get_voltage(self):
        voltage_sensor = self.service_manager.find_service(IOType.IO_TYPE_VOLTAGE)
        if voltage_sensor != None:
            voltage = voltage_sensor.get_value_as_millivolts()
            return round(voltage, 2)
        else:
            print("Voltage sensor is not available")
            return None

    """
    Returns the current of the Smarthub battery in milliamps
    """
    def get_current(self):
        current_sensor = self.service_manager.find_service(IOType.IO_TYPE_CURRENT)
        if current_sensor != None:
            current = current_sensor.get_value_as_milliamps()
            return round(current, 2)
        else:
            print("Current sensor is not available")
            return None

        
