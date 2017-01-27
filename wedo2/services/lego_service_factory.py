
from wedo2.services import generic_service
from generic_service import GenericService
from wedo2.services import motion_sensor
from motion_sensor import MotionSensor
from wedo2.services import tilt_sensor
from tilt_sensor import TiltSensor
from wedo2.services import piezo_tone_player
from piezo_tone_player import PiezoTonePlayer
from wedo2.services import motor
from motor import Motor
from wedo2.services import current_sensor
from current_sensor import CurrentSensor
from wedo2.services import voltage_sensor
from voltage_sensor import VoltageSensor
from wedo2.services import rgb_light
from rgb_light import RGBLight
from wedo2.device import connect_info
from connect_info import IOType


class LegoServiceFactory:

    def create(connect_info, io, lego_device):
        if io == None or connect_info == None:
            # LDSDKLogger.e("Cannot instantiate service...")
            return None

        result = None
        type_enum = connect_info.get_type_enum()

        if type_enum == IOType.IO_TYPE_GENERIC:
            result = GenericService.create_service(connect_info, io)
            
        elif type_enum == IOType.IO_TYPE_MOTION_SENSOR:
            result = MotionSensor.create_service(connect_info, io)
            
        elif type_enum == IOType.IO_TYPE_TILT_SENSOR:
            result = TiltSensor.create_service(connect_info, io)
            
        elif type_enum == IOType.IO_TYPE_PIEZO_TONE_PLAYER:
            result = PiezoTonePlayer.create_service(connect_info, io)
            
        elif type_enum == IOType.IO_TYPE_MOTOR:
            result = Motor.create_service(connect_info, io)
            
        elif type_enum == IOType.IO_TYPE_CURRENT:
            result = CurrentSensor.create_service(connect_info, io)
            
        elif type_enum == IOType.IO_TYPE_VOLTAGE:
            result = VoltageSensor.create_service(connect_info, io)
            
        elif type_enum == IOType.IO_TYPE_RGB_LIGHT:
            result = RGBLight.create_service(connect_info, io)
            
        else:
            result = GenericService.create_service(connect_info, io)

        result.set_device(device)

        return result
    


