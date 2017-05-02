
from enum import Enum

class IOType(Enum):
    IO_TYPE_MOTOR = 1
    IO_TYPE_VOLTAGE = 20
    IO_TYPE_CURRENT = 21
    IO_TYPE_PIEZO_TONE_PLAYER = 22
    IO_TYPE_RGB_LIGHT = 23
    IO_TYPE_TILT_SENSOR = 34
    IO_TYPE_MOTION_SENSOR = 35
    IO_TYPE_GENERIC = 0
    

class ConnectInfo:

    def __init__(self, connect_id, hub_index, type_id):
        self.connect_id = connect_id
        self.hub_index = hub_index  # Index of the port that the IO is attached to
        self.type_id = type_id
        self.valid_types = []
        self.populate_valid_types()

    def populate_valid_types(self):
        self.valid_types.append(IOType.IO_TYPE_MOTOR.value)
        self.valid_types.append(IOType.IO_TYPE_VOLTAGE.value)
        self.valid_types.append(IOType.IO_TYPE_CURRENT.value)
        self.valid_types.append(IOType.IO_TYPE_PIEZO_TONE_PLAYER.value)
        self.valid_types.append(IOType.IO_TYPE_RGB_LIGHT.value)
        self.valid_types.append(IOType.IO_TYPE_TILT_SENSOR.value)
        self.valid_types.append(IOType.IO_TYPE_MOTION_SENSOR.value)
        self.valid_types.append(IOType.IO_TYPE_GENERIC.value)

    def get_type_enum(self):
        if self.type_id in self.valid_types:
            return IOType(self.type_id)
        else:
            return IOType.IO_TYPE_GENERIC

    def __str__(self):
        return "ConnectInfo{" \
               ", connect_id=" + str(self.connect_id) + "" \
               ", hub_index=" + str(self.hub_index) + "" \
               ", type_id=" + str(self.type_id) + "}"

