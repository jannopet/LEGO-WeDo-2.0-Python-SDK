from abc import ABCMeta, abstractmethod

class IO(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def write_input_format(new_format, connect_id):
        pass

    @abstractmethod
    def read_input_format_for_connect_id(connect_id):
        pass

    @abstractmethod
    def write_motor_power(power, connect_id):
        pass

    @abstractmethod
    def write_motor_power(power, offset, connect_id):
        pass

    @abstractmethod
    def write_piezo_tone_frequency(frequency, duration, connect_id):
        pass

    @abstractmethod
    def write_piezo_tone_stop(connect_id):
        pass

    @abstractmethod
    def write_color(red, green, blue, connect_id):
        pass

    @abstractmethod
    def write_color_index(index, connect_id):
        pass

    @abstractmethod
    def write_data(data, connect_id):
        pass

    @abstractmethod
    def read_value_for_connect_id(connect_id):
        pass

    @abstractmethod
    def reset_state_for_connect_id(connect_id):
        pass

    

    
