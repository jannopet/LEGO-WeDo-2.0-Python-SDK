

from wedo2.bluetooth.connect_info import ConnectInfo
from wedo2.services.lego_service import LegoService
from enum import Enum

class PiezoTonePlayerNote(Enum):
    PIEZO_NOTE_C = 1    # C
    PIEZO_NOTE_CIS = 2  # C#
    PIEZO_NOTE_D = 3    # D
    PIEZO_NOTE_DIS = 4  # D#
    PIEZO_NOTE_E = 5    # E
    PIEZO_NOTE_F = 6    # F
    PIEZO_NOTE_FIS = 7  # F#
    PIEZO_NOTE_G = 8    # G
    PIEZO_NOTE_GIS = 9  # G#
    PIEZO_NOTE_A = 10   # A
    PIEZO_NOTE_AIS = 11 # A#
    PIEZO_NOTE_B = 12   # B

PIEZO_TONE_MAX_FREQUENCY = 1500
PIEZO_TONE_MAX_DURATION = 65536

SERVICE_PIEZO_TONE_PLAYER_NAME = "Piezo"

class PiezoTonePlayer(LegoService):

    def __init__(self, connect_info, io):
        super(PiezoTonePlayer, self).__init__(connect_info, io)

    def create_service(connect_info, io):
        return PiezoTonePlayer(connect_info, io)

    def get_service_name(self):
        return SERVICE_PIEZO_TONE_PLAYER_NAME

    def play_frequency(self, frequency, duration):
        if frequency > PIEZO_TONE_MAX_FREQUENCY:
            # LDSDKLogger.w("cannot play freq")
            frequency = PIEZO_TONE_MAX_FREQUENCY

        if duration > PIEZO_TONE_MAX_DURATION:
            # LDSDKLogger.w("cannot play piezo tone")
            duration = PIEZO_TONE_MAX_DURATION

        self.io.write_piezo_tone_frequency(round(frequency), duration, self.connect_info.connect_id)

    def play_note(self, note, octave, duration):
        if octave > 6:
            # LSDKLogger.w("invalid octave")
            print("Invalid octave")
        if octave == 6 and note.value > PiezoTonePlayerNote.PIEZO_NOTE_FIS.value:
            # LSDKLogger.w("cannot play note")
            print("Cannot play note")

        base = 440.0
        octaves_above_middle = octave - 4
        half_steps_away_from_base = note.value - PiezoTonePlayerNote.PIEZO_NOTE_A.value + (octaves_above_middle * 12)
        frequency = base * pow(pow(2.0, 1.0 / 12), half_steps_away_from_base)
        rounded_freq = round(frequency)

        self.play_frequency(rounded_freq, duration)

    def stop_playing(self):
        self.io.write_piezo_tone_stop(self.connect_info.connect_id)
        
        
