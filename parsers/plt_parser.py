__author__ = 'Moran'
import re


class PltParser(object):
    """
    A parser for plt files
    """
    def __init__(self, file_path):
        """
        :param file_path: The path to the plt file
        """
        self._file_path = file_path
        with open(file_path, "rb") as f:
            data = f.read()
        datasets_re = re.search("datasets\s+=\s+\[(?P<sets_list>[^\]]+)\]", data)
        data_re = re.search("Data\s+\{(?P<data_list>[^}]+)\}", data)
        sets_list = re.findall('"([\w ]+)"', datasets_re.group("sets_list"))
        data_list = data_re.group("data_list").split()
        # Round robin the datas
        self._data_sets = {}
        index = 0
        for value in data_list:
            key = sets_list[index % len(sets_list)]
            values_list = self._data_sets.setdefault(key, [])
            values_list.append(value)
            index += 1

    def get_data_set(self, data_set_name):
        """
        Gets the values of the given data sets
        :param data_set_name: The name of the data set to look for
        :return: A list of the data set values
        """
        return self._data_sets[data_set_name]

    def export_to_csv(self, csv_path, data_sets=None):
        """
        Writes te plt to a csv format
        :param csv_path: A path to write the csv file
        :param data_sets: The data sets to export, if not given, export all data sets
        """
        if not data_sets:
            data_sets = self._data_sets.keys()
        with open(csv_path, "wb") as csv_file:
            for data_set in data_sets:
                data = ",".join([data_set] + self._data_sets[data_set]) + "\n"
                csv_file.write(data)



if __name__ == "__main__":
    p = PltParser(r"C:\Users\Moran\Documents\transient_MSET_inst_MSET_1_to_2_des.plt")