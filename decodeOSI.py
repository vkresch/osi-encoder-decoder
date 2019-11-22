"""
Module to handle and manage OSI scenarios.
"""
from collections import deque
import time
import lzma

from osi3.osi_sensorview_pb2 import SensorView
from osi3.osi_groundtruth_pb2 import GroundTruth
from osi3.osi_sensordata_pb2 import SensorData


SEPARATOR = b'$$__$$'
SEPARATOR_LENGTH = len(SEPARATOR)
BUFFER_SIZE = 1000000


def get_size_from_file_stream(file_object):
    """
    Return a file size from a file stream given in parameters
    """
    current_position = file_object.tell()
    file_object.seek(0, 2)
    size = file_object.tell()
    file_object.seek(current_position)
    return size


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

    # Open and Read text file

    def from_file(self, path, type_name="SensorView", max_index=-1):
        """Import a scenario from a file"""
        if path.lower().endswith(('.lzma', '.xz')):
            self.scenario_file = lzma.open(path, "rb")
        else:
            self.scenario_file = open(path, "rb")

        self.type_name = type_name
        self.timestep_count = self.retrieve_message_offsets(max_index)

    def retrieve_message_offsets(self, max_index):
        """
        Retrieve the offsets of all the messages of the scenario and store them
        in the `message_offsets` attribute of the object

        It returns the number of discovered timesteps
        """
        scenario_size = get_size_from_file_stream(self.scenario_file)

        if max_index == -1:
            max_index = float('inf')

        buffer_deque = deque(maxlen=2)

        self.message_offsets = [0]
        eof = False

        self.scenario_file.seek(0)

        while not eof and len(self.message_offsets) <= max_index:
            found = -1  # SEP offset in buffer
            buffer_deque.clear()

            while found == -1 and not eof:
                new_read = self.scenario_file.read(BUFFER_SIZE)
                buffer_deque.append(new_read)
                buffer = b"".join(buffer_deque)
                found = buffer.find(SEPARATOR)
                eof = len(new_read) != BUFFER_SIZE

            buffer_offset = self.scenario_file.tell() - len(buffer)
            message_offset = found + buffer_offset + SEPARATOR_LENGTH
            self.message_offsets.append(message_offset)

            self.scenario_file.seek(message_offset)

            while eof and found != -1:
                buffer = buffer[found + SEPARATOR_LENGTH:]
                found = buffer.find(SEPARATOR)

                buffer_offset = scenario_size - len(buffer)

                message_offset = found + buffer_offset + SEPARATOR_LENGTH

                if message_offset >= scenario_size:
                    break
                self.message_offsets.append(message_offset)

        if eof:
            self.retrieved_scenario_size = scenario_size
        else:
            self.retrieved_scenario_size = self.message_offsets[-1]
            self.message_offsets.pop()

        return len(self.message_offsets)

    def get_message_by_index(self, index):
        """
        Get a message by its index. Try first to get it from the cache made
        by the method ``cache_messages_in_index_range``.
        """
        return next(self.get_messages_in_index_range(index, index+1))

    def get_messages(self):
        return self.get_messages_in_index_range(0, len(self.message_offsets))

    def get_messages_in_index_range(self, begin, end):
        """
        Yield an iterator over messages of indexes between begin and end included.
        """
        self.scenario_file.seek(self.message_offsets[begin])
        abs_first_offset = self.message_offsets[begin]
        abs_last_offset = self.message_offsets[end] \
            if end < len(self.message_offsets) \
            else self.retrieved_scenario_size

        rel_message_offsets = [
            abs_message_offset - abs_first_offset
            for abs_message_offset in self.message_offsets[begin:end]
        ]

        message_sequence_len = abs_last_offset - \
            abs_first_offset - SEPARATOR_LENGTH
        serialized_messages_extract = self.scenario_file.read(
            message_sequence_len)

        for rel_index, rel_message_offset in enumerate(rel_message_offsets):
            rel_begin = rel_message_offset
            rel_end = rel_message_offsets[rel_index + 1] - SEPARATOR_LENGTH \
                if rel_index + 1 < len(rel_message_offsets) \
                else message_sequence_len
            message = MESSAGES_TYPE[self.type_name]()
            serialized_message = serialized_messages_extract[rel_begin:rel_end]
            message.ParseFromString(serialized_message)
            yield message

        self.scenario_file.close()

    def txt2json(self, name, interval=None, index=None):
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
    scenario.from_file(path="test_scenario.txt")

    scenario2 = OSITrace()
    scenario2.from_file(path="test_scenario_changes.txt")

    # sv = scenario.get_messages_in_index_range(0, 1)
    # for i in sv:
    #     print(i)

    # sv = scenario.get_message_by_index(0)
    # print(sv)

    # sv = scenario.get_messages()
    # for i in sv:
    #     print(i)

    scenario.txt2json(name="test_scenario.json")
    scenario2.txt2json(name="test_scenario_changes.json")
    # scenario.txt2json(name="test1.json", index=1)
    # scenario.txt2json(name="test2.json", interval=(6, 10))

    # scenario.txt2json(name="test4.json", index=0.2)
    # scenario.txt2json(name="test5.json", interval=(4, 3))
    