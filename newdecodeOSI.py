"""
Module to handle and manage OSI traces.
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
    """This class wrap OSI data. It can import and decode OSI traces."""

    def __init__(self, show_progress=True, path=None, type_name="SensorView"):
        self.trace_file = None
        self.message_offsets = None
        self.type_name = type_name
        self.timestep_count = 0
        self.show_progress = show_progress
        self.retrieved_trace_size = 0

        if path is not None and type_name is not None:
            self.from_file(path)

    def from_file(self, path, type_name="SensorView", max_index=-1):
        """Import a trace from a file"""
        if path.lower().endswith(('.lzma', '.xz')):
            self.trace_file = lzma.open(path, "rb")
        else:
            self.trace_file = open(path, "rb")

        self.type_name = type_name

    def get_messages(self):
        self.trace_file.seek(0)
        serialized_message = self.trace_file.read()
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
                    f.write(str(trace.get_message_by_index(0)))
                else:
                    raise Exception("Argument 'index' needs to be of type 'int'")

            if interval is not None and index is not None:
                raise Exception("Arguments 'index' and 'interval' can not be set both")


if __name__ == "__main__":
    trace = OSITrace()
    # trace.from_file(path="test_trace.osi")
    trace.from_file(path="test_trace.osi")

    sv = trace.get_messages()
    for m in sv:
        print(m)

    # sv = trace.get_message_by_index(3) 
    # print(sv)

    # for i in sv:
    #     print(i)

    # sv = trace.get_message_by_index(0)
    # print(sv)

    # sv = trace.get_messages()
    # for i in sv:
    #     print(i)

    # trace.osi2read(name="test_trace_converted.txth")
    # trace.osi2read(name="test1.txth", index=1)
    # trace.osi2read(name="test2.txth", interval=(6, 10))

    # trace.osi2read(name="test4.txth", index=0.2)
    # trace.osi2read(name="test5.txth", interval=(4, 3))
    