
class DataFormat:

    def __init__(self, mode_name, mode, unit,
                 number_of_bytes, number_of_datasets):
        self.mode_name = mode_name
        self.mode = mode
        self.unit = unit
        self.dataset_size = number_of_bytes
        self.dataset_count = number_of_datasets


    def create(mode_name, mode, unit, number_of_bytes, number_of_datasets):
        return DataFormat(mode_name, mode, unit, number_of_bytes, number_of_datasets)

    def get_mode_name(self):
        return self.mode_name

    def get_mode(self):
        return self.mode

    def get_unit(self):
        return self.unit

    def dataset_size(self):
        return self.dataset_size

    def dataset_count(self):
        return self.dataset_count

    def __str__(self): # VAADATA SIIN MEETODI unit.name() VÄLJAKUTSE ÜLE !!!
        return "DataFormat{" \
                "mode_name='" + str(self.mode_name) + '\'' \
                ", unit='" + str(self.unit.name()) + '\'' \
                ", dataSetSize=" + str(self.dataset_size) + "" \
                ", dataSetCount=" + str(self.dataset_count) + '}'

    # Eeldan hetkel, et see on piisav, et toimida samamoodi nagu equals java-s toimib
    def __eq__(self, obj):
        """Override the default Equals behaviour"""
        if isinstance(obj, self.__class__):
            return self.__dict__ == obj.__dict__
        return NotImplemented

    def __ne__(self, obj):
        """Define a non-equality test"""
        if isinstance(obj, self.__class__):
            return not self.__eq__(obj)
        return NotImplemented

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        return hash(tuple(sorted(self.__dict__.items())))

    def hash_code(self):
        result = self.mode
        unit_value = 0
        if self.unit != None:
            unit_value = self.unit.hashCode()
        result = 31 * result + unit_value
        return result

   

