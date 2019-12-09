from osi3.osi_sensorview_pb2 import SensorView
from newdecodeOSI import OSITrace

def main():
    """Initialize SensorView"""
    trace = OSITrace()
    trace.from_file(path="test_trace.osi")
    sv = trace.get_messages() # Create an iterator for messages
    
    for message in sv:
        print("--------------- START ---------------")

        sensorview = message
        moving_object = sensorview.global_ground_truth.moving_object
        for mv in moving_object:
            print("\nMoving Object ----------")
            print(f"id: {mv.id.value}")
            print(f"x: {mv.base.position.x}, y: {mv.base.position.y}, z: {mv.base.position.z},")

        print("---------------  END  ---------------")
    
 
if __name__ == "__main__":
    main()