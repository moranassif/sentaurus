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


if __name__ == "__main__":
    p = PltParser(r"C:\Users\Moran\Documents\transient_MSET_inst_MSET_1_to_2_des.plt")