
from wedo2.services.generic_service import GenericService
from wedo2.services.motion_sensor import MotionSensor
from wedo2.services.tilt_sensor import TiltSensor
from wedo2.services.piezo_tone_player import PiezoTonePlayer 
from wedo2.services.motor import Motor
from wedo2.services.current_sensor import CurrentSensor
from wedo2.services.voltage_sensor import VoltageSensor
from wedo2.services.rgb_light import RGBLight
from wedo2.bluetooth.connect_info import ConnectInfo, IOType


class LegoServiceFactory:

    def create(connect_info, io):
        if io == None or connect_info == None:
            print("Cannot instantiate service")
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

        return result
    


