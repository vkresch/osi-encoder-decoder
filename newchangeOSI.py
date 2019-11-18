from osi3.osi_sensorview_pb2 import SensorView
from decodeOSI import OSIScenario
import struct

def main():
    """Initialize SensorView"""
    scenario = OSIScenario()
    scenario.from_file(path="test_scenario.txt")
    sv = scenario.get_messages() # Create an iterator for messages
    f = open("test_scenario_new_converted.txt", "ab")
    
    for message in sv:
        string_buffer = message.SerializeToString()
        f.write(struct.pack("L", len(string_buffer)) + string_buffer) 
    
    f.close()
 
if __name__ == "__main__":
    main()