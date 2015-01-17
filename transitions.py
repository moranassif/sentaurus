__author__ = 'Moran'
from tools.transitions_handler import TransitionsHandler

transitions_directory = r"D:\Users\Moran\Scratchpad\transitions results"
handler = TransitionsHandler(transitions_directory)
handler.export_currents_and_voltages(r"D:\Users\Moran\Scratchpad\csvs")