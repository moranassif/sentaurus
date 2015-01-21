__author__ = 'Moran'
import os
from parsers import PltParser


class TransitionsHandler(object):
    """
    Handle a directory of sentaurus transition results
    """
    def __init__(self, directory_path):
        self._directory_path = directory_path
        transitions = [x for x in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, x))]
        # Get the plt file for each transition
        self._plt_parsers = {}
        for transition in transitions:
            plt_path = [x for x in os.listdir(os.path.join(directory_path, transition)) if x.endswith(".plt")][0]
            self._plt_parsers[transition] = PltParser(os.path.join(directory_path, transition, plt_path))

    def export_currents_and_voltages(self, directory):
        """
        Export all currents and voltages of the transitions to csv files
        :param directory: The directory to export to
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
        contacts = ["source_con", "drain1_con", "drain2_con", "JG1", "JG2"]
        for transition, plt_parser in self._plt_parsers.iteritems():
            file_path = os.path.join(directory, "%s.csv" % transition)
            voltages = [x + " InnerVoltage" for x in contacts]
            currents = [x + " TotalCurrent" for x in contacts]
            plt_parser.export_to_csv(file_path, ["time"] + voltages + currents)