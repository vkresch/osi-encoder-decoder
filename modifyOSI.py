from osi3.osi_sensorview_pb2 import SensorView
from decodeOSI import OSITrace

def main():
    """Initialize SensorView"""
    scenario = OSITrace()
    scenario.from_file(path="test_scenario.txt")
    sv = scenario.get_messages() # Create an iterator for messages
    f = open("test_scenario_changes.txt", "ab")
    
    for message in sv:

        sensorview = message
        sv_ground_truth = sensorview.global_ground_truth

        # Set a different version number
        sv_ground_truth.version.version_major = 2
        sv_ground_truth.version.version_minor = 0 
        sv_ground_truth.version.version_patch = 0   

        bytes_buffer = sensorview.SerializeToString()

        f.write(bytes_buffer)
        f.write(b"$$__$$")
    
    f.close()
 
if __name__ == "__main__":
    main()