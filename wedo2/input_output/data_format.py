
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

    def __str__(self): 
        return "DataFormat{" \
                "mode_name='" + str(self.mode_name) + '\'' \
                ", unit='" + str(self.unit) + '\'' \
                ", dataSetSize=" + str(self.dataset_size) + "" \
                ", dataSetCount=" + str(self.dataset_count) + '}'

    # Eeldan hetkel, et see on piisav, et toimida samamoodi nagu equals java-s toimib
    def __eq__(self, obj):
        try:
            if self.mode_name != obj.mode_name: return False
            if self.mode != obj.mode: return False
            if self.unit != obj.unit: return False
            if self.dataset_size != obj.dataset_size: return False
            if self.dataset_count != obj.dataset_count: return False

            return True
        except:
            return False

    def __ne__(self, obj):
        return not self.__eq__(obj)


   

