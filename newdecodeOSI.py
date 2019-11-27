"""
Module to handle and manage OSI scenarios.
"""
from collections import deque
import time

from osi3.osi_sensorview_pb2 import SensorView
from osi3.osi_groundtruth_pb2 import GroundTruth
from osi3.osi_sensordata_pb2 import SensorData
import struct
import lzma

MESSAGES_TYPE = {
    "SensorView": SensorView,
    "GroundTruth": GroundTruth,
    "SensorData": SensorData
}


class OSITrace:
    """This class wrap OSI data. It can import and decode OSI scenarios."""

    def __init__(self, show_progress=True, path=None, type_name="SensorView"):
        self.scenario_file = None
        self.message_offsets = None
        self.type_name = type_name
        self.timestep_count = 0
        self.show_progress = show_progress
        self.retrieved_scenario_size = 0

        if path is not None and type_name is not None:
            self.from_file(path)

    def from_file(self, path, type_name="SensorView", max_index=-1):
        """Import a scenario from a file"""
        if path.lower().endswith(('.lzma', '.xz')):
            self.scenario_file = lzma.open(path, "rb")
        else:
            self.scenario_file = open(path, "rb")

        self.type_name = type_name

    def get_messages(self):
        self.scenario_file.seek(0)
        serialized_message = self.scenario_file.read()
        INT_LENGTH =  len(struct.pack("<L", 0))
        message_length = 0

        messages = []
        i = 0
        while i < len(serialized_message):
            message = MESSAGES_TYPE[self.type_name]()
            message_length = struct.unpack("<L", serialized_message[i:INT_LENGTH+i])[0]
            message.ParseFromString(serialized_message[i+INT_LENGTH:i+INT_LENGTH+message_length])
            i += message_length + INT_LENGTH
            messages.append(message)
        return messages

    def get_message_by_index(self, index):
        return self.get_messages()[index]

    def get_messages_in_index_range(self, begin, end):
        return self.get_messages()[begin:end]        

    def osi2read(self, name, interval=None, index=None):
        with open(name, 'a') as f:

            if interval is None and index is None:
                for i in self.get_messages():
                    f.write(str(i))
            
            if interval is not None and index is None:
                if type(interval) == tuple and len(interval) == 2 and interval[0]<interval[1]:
                    for i in self.get_messages_in_index_range(interval[0], interval[1]):
                        f.write(str(i))
                else:
                    raise Exception("Argument 'interval' needs to be a tuple of length 2! The first number must be smaller then the second.")

            if interval is None and index is not None:
                if type(index) == int:
                    f.write(str(scenario.get_message_by_index(0)))
                else:
                    raise Exception("Argument 'index' needs to be of type 'int'")

            if interval is not None and index is not None:
                raise Exception("Arguments 'index' and 'interval' can not be set both")


if __name__ == "__main__":
    scenario = OSITrace()
    # scenario.from_file(path="test_trace.osi")
    scenario.from_file(path="test_trace.osi")

    sv = scenario.get_messages()
    for m in sv:
        print(m)

    # sv = scenario.get_message_by_index(3) 
    # print(sv)

    # for i in sv:
    #     print(i)

    # sv = scenario.get_message_by_index(0)
    # print(sv)

    # sv = scenario.get_messages()
    # for i in sv:
    #     print(i)

    # scenario.osi2read(name="test_scenario_converted.txth")
    # scenario.osi2read(name="test1.txth", index=1)
    # scenario.osi2read(name="test2.txth", interval=(6, 10))

    # scenario.osi2read(name="test4.txth", index=0.2)
    # scenario.osi2read(name="test5.txth", interval=(4, 3))
    