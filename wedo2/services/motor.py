
from wedo2.input_output import io
from wedo2.services import lego_service
from lego_service import LegoService
from enum import Enum

MOTOR_MIN_SPEED = 1
MOTOR_MAX_SPEED = 100
MOTOR_POWER_BRAKE = 127
MOTOR_POWER_DRIFT = 0

MOTOR_POWER_OFFSET = 35
SERVICE_MOTOR_NAME = "Motor"

class MotorDirection(Enum):
    MOTOR_DIRECTION_DRIFTING = 0
    MOTOR_DIRECTION_LEFT = 1
    MOTOR_DIRECTION_RIGHT = 2
    MOTOR_DIRECTION_BRAKING = 3
    

class Motor(LegoService):

    def __init__(self, connect_info, io):
        super(Motor, self).__init__(connect_info, io)

    def create_service(connect_info, io):
        return Motor(connect_info, io)

    def get_service_name(self):
        return SERVICE_MOTOR_NAME

    def get_power(self):
        if self.most_recent_send_power == MOTOR_POWER_BRAKE or \
            self.most_recent_send_power == MOTOR_POWER_DRIFT:
            return 0
        return abs(self.most_recent_send_power)

    def is_braking(self):
        return self.most_recent_send_power == MOTOR_POWER_BRAKE

    def is_drifting(self):
        return self.most_recent_send_power == MOTOR_POWER_DRIFT

    def run(self, direction, power):
        if power == MOTOR_POWER_DRIFT:
            self.drift()
        else:
            converted_power = self.convert_unsigned_motor_power_to_signed(power, direction)
            self.send_power(converted_power)
            self.direction = direction

    def brake(self):
        self.send_power(MOTOR_POWER_BRAKE)
        self.direction = MotorDirection.MOTOR_DIRECTION_BRAKING

    def drift(self):
        self.send_power(MOTOR_POWER_DRIFT)
        self.direction = MotorDirection.MOTOR_DIRECTION_DRIFTING

    def send_power(self, power):
        if power == MOTOR_POWER_BRAKE or power == MOTOR_POWER_DRIFT:
            self.io.write_motor_power(power, self.connect_info.connect_id)
        else:
            offset = 0
            try:
                # device should be inherited from parent class 'LegoService'
                if self.device.device_info.firmware_revision.major_version >= 1:
                    offset = MOTOR_POWER_OFFSET
            except:
                raise Exception("NullPointerException")

            self.io.write_motor_power(power, offset, self.connect_info.connect_id)

        self.most_recent_send_power = power

        # try: handleUpdatedValueData()

    def convert_unsigned_motor_power_to_signed(self, power, direction):
        result_power = 0
        if power < MOTOR_MAX_SPEED:
            result_power = power
        else:
            result_power = MOTOR_MAX_SPEED

        if direction == MotorDirection.MOTOR_DIRECTION_LEFT:
            result_power = -result_power

        return result_power

        

        
            
