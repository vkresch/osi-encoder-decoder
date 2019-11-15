from osi3.osi_sensorview_pb2 import SensorView
from decodeOSI import OSIScenario

def main():
    """Initialize SensorView"""
    scenario = OSIScenario()
    scenario.from_file(path="test_scenario.txt")
    sv = scenario.get_messages() # Create an iterator for messages
    for message in sv:

        sensorview = message
        sv_ground_truth = sensorview.global_ground_truth
        sv_ground_truth.version.version_major = 2
        sv_ground_truth.version.version_minor = 0 
        sv_ground_truth.version.version_patch = 0 

        string_buffer = sensorview.SerializeToString()

        with open("test_scenario_changes.txt", "ab") as f:
            f.write(string_buffer + b"$$__$$")       
 
if __name__ == "__main__":
    main()