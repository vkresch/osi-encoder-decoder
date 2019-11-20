from osi3.osi_sensorview_pb2 import SensorView
import struct
import sys

def main():
    """Initialize SensorView"""
    f = open("test_scenario_new.txt", "ab")
    sensorview = SensorView()

    sv_ground_truth = sensorview.global_ground_truth
    sv_ground_truth.version.version_major = 3
    sv_ground_truth.version.version_minor = 0
    sv_ground_truth.version.version_patch = 0

    sv_ground_truth.timestamp.seconds = 4
    sv_ground_truth.timestamp.nanos = 54999999

    stationary_object = sv_ground_truth.stationary_object.add()
    stationary_object.id.value = 114

    for i in range(11):
        
        stationary_object.base.dimension.length = 3 + i
        stationary_object.base.dimension.width = 0.5 + i
        stationary_object.base.dimension.height = 0.89 + i

        stationary_object.base.position.x = 0.0 + i
        stationary_object.base.position.y = 0.0 
        stationary_object.base.position.z = 0.0

        stationary_object.base.orientation.roll = 0.0
        stationary_object.base.orientation.pitch = 0.0
        stationary_object.base.orientation.yaw = 0.0 

        stationary_object.classification.type = 1
        stationary_object.classification.material = 0
        stationary_object.classification.density = 0
        stationary_object.classification.color = 0

        """Serialize SensorData which can be send"""
        string_buffer = sensorview.SerializeToString()
        f.write(struct.pack("<L", len(string_buffer)) + string_buffer)   

    f.close()
 
if __name__ == "__main__":
    main()