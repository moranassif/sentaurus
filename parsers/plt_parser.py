__author__ = 'Moran'
import re


def find_index_of_closets_value(values, value_to_look_for):
    """
    Finds the index of the value which is closest to the value given
    :param values: A list of values to look into
    :param value_to_look_for: The value to look for
    :return: Index inside the list
    """
    closest_index = 0
    # Init to some value
    closest_distance = max(abs(value_to_look_for), abs(values[0]))
    for index, value in enumerate(values):
        distance = abs(value - value_to_look_for)
        if distance < closest_distance:
            closest_index = index
            closest_distance = distance
    return closest_index


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
            values_list.append(float(value))
            index += 1

    def get_data_set(self, data_set_name):
        """
        Gets the values of the given data sets
        :param data_set_name: The name of the data set to look for
        :return: A list of the data set values
        """
        return self._data_sets[data_set_name]

    def export_to_csv(self, csv_path, data_sets=None, data_sets_operations=None):
        """
        Writes te plt to a csv format
        :param csv_path: A path to write the csv file
        :param data_sets: The data sets to export, if not given, export all data sets
        :param data_sets_operations: If a tuple is given, parse it as (operation, data set1, data set2) and
               print of example data_set1*data_set2
        """
        if not data_sets:
            data_sets = self._data_sets.keys()
        with open(csv_path, "wb") as csv_file:
            for data_set in data_sets:
                data = [data_set] + [str(x) for x in self._data_sets[data_set]]
                csv_file.write(",".join(data) + "\n")
            for operation, operand1, operand2 in data_sets_operations:
                data1 = self._data_sets[operand1]
                data2 = self._data_sets[operand2]
                data = ["%s %s %s" % (operand1, operation, operand2)] + \
                       [str(eval("%s %s %s" % (couple[0], operation, couple[1]))) for couple in zip(data1, data2)]
                csv_file.write(",".join(data) + "\n")

    def calc_rise_time(self, contact, start_time):
        """
        Calculate the rise time of the voltage of the
        contact from after the given time
        :param contact: The contact to check
        :param start_time: The time to start looking for the 10% of the final value
        :return: Rise time is seconds
        """
        # The percentage from and to of the rise time calculations
        # for example 0.1 of the final value to 0.9 of it
        from_percent = 0.1
        to_percent = 0.9
        times = self.get_data_set("time")
        assert times[0] <= start_time < times[-1]
        # The index to start looking from
        starting_index = find_index_of_closets_value(self.get_data_set("time"), start_time)
        # Get relevant voltages
        voltages = self.get_data_set("%s InnerVoltage" % contact)[starting_index:]
        final_voltage = voltages[-1]
        from_index = find_index_of_closets_value(voltages, from_percent * final_voltage)
        to_index = find_index_of_closets_value(voltages[from_index:], to_percent * final_voltage)
        rise_time = times[starting_index+from_index+to_index] - times[starting_index+from_index]
        return rise_time

if __name__ == "__main__":
    p = PltParser(r"D:\Users\Moran\Scratchpad\transitions results\3_to_1\transient_MSET_inst_MSET_3_to_1_des.plt")
    print(p.calc_rise_time("source_con", 1e-11))