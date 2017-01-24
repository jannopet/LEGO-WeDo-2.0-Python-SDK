from abc import ABCMeta, abstractmethod

class IO(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def write_input_format(self, new_format, connect_id):
        pass

    @abstractmethod
    def read_input_format_for_connect_id(self, connect_id):
        pass

    @abstractmethod
    def write_motor_power(self, *args)
    
    @abstractmethod
    def write_piezo_tone_frequency(self, frequency, duration, connect_id):
        pass

    @abstractmethod
    def write_piezo_tone_stop(self, connect_id):
        pass

    @abstractmethod
    def write_color(self, red, green, blue, connect_id):
        pass

    @abstractmethod
    def write_color_index(self, index, connect_id):
        pass

    @abstractmethod
    def write_data(self, data, connect_id):
        pass

    @abstractmethod
    def read_value_for_connect_id(self, connect_id):
        pass

    @abstractmethod
    def reset_state_for_connect_id(connect_id):
        pass

    

    
