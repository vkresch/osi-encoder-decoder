# OSI encoder / decoder
The encoder enables to encode multiple OSI messages into one file. The decoder can parse the generated file and output it in a human readable json-like format.

## Usage

#### Encode with seperator
Encode ten OSI messages in the file `test_trace.txt` which change the dimensions and the x-position of a stationary object over time:
```python
from osi3.osi_sensorview_pb2 import SensorView
import struct

def main():
    """Initialize SensorView"""
    f = open("test_trace.txt", "ab")
    sensorview = SensorView()

    sv_ground_truth = sensorview.global_ground_truth
    sv_ground_truth.version.version_major = 3
    sv_ground_truth.version.version_minor = 0
    sv_ground_truth.version.version_patch = 0

    sv_ground_truth.timestamp.seconds = 0
    sv_ground_truth.timestamp.nanos = 0

    moving_object = sv_ground_truth.moving_object.add()
    moving_object.id.value = 114

    # Generate 10 OSI messages for 9 seconds
    for i in range(10):

        # Increment the time
        sv_ground_truth.timestamp.seconds += 1
        sv_ground_truth.timestamp.nanos += 100000

        moving_object.vehicle_classification.type = 2
        
        moving_object.base.dimension.length = 5
        moving_object.base.dimension.width = 2
        moving_object.base.dimension.height = 1

        moving_object.base.position.x = 0.0 + i
        moving_object.base.position.y = 0.0 
        moving_object.base.position.z = 0.0

        moving_object.base.orientation.roll = 0.0
        moving_object.base.orientation.pitch = 0.0
        moving_object.base.orientation.yaw = 0.0 
        

        """Serialize SensorData which can be send"""
        string_buffer = sensorview.SerializeToString()
        f.write(string_buffer)
        f.write(b'$$__$$')

    f.close()
 
if __name__ == "__main__":
    main()
```
Type in the terminal:
```bash
$ python3 encodeOSI.py
```

#### Decode with seperator
Decode the generated OSI trace.
```python
from decodeOSI import OSITrace

if __name__ == "__main__":
    trace = OSITrace()
    trace.from_file(path="test_trace.txt")

    # Print all messages
    sv = trace.get_messages()
    for i in sv:
        print(i)

    # Print the osi message in a interval (here from first to ninth)
    sv = trace.get_messages_in_index_range(0, 10)
    for i in sv:
        print(i)

    # Print the osi message by index (here the first)
    sv = trace.get_message_by_index(0)
    print(sv)

    # Save output into readable osi files
    trace.osi2read(name="test1.txth")
    trace.osi2read(name="test2.txth", index=1)
    trace.osi2read(name="test3.txth", interval=(6, 10))
```
Type in the terminal:
```bash
$ python3 decodeOSI.py
```

#### Convert from seperator trace to length defined trace

Type in the terminal:
```bash
$ python3 txt2osi.py -f small_test.txt
```

#### Encode without seperator
Encode ten OSI messages in the file `test_trace.txt` which change the dimensions and the x-position of a stationary object over time:
```python
from osi3.osi_sensorview_pb2 import SensorView
import struct

def main():
    """Initialize SensorView"""
    f = open("test_trace.txt", "ab")
    
    sensorview = SensorView()

    sv_ground_truth = sensorview.global_ground_truth
    sv_ground_truth.version.version_major = 3
    sv_ground_truth.version.version_minor = 0
    sv_ground_truth.version.version_patch = 0

    sv_ground_truth.timestamp.seconds = 0
    sv_ground_truth.timestamp.nanos = 0

    moving_object = sv_ground_truth.moving_object.add()
    moving_object.id.value = 114

    # Generate 10 OSI messages for 9 seconds
    for i in range(10):

        # Increment the time
        sv_ground_truth.timestamp.seconds += 1
        sv_ground_truth.timestamp.nanos += 100000

        moving_object.vehicle_classification.type = 2
        
        moving_object.base.dimension.length = 5
        moving_object.base.dimension.width = 2
        moving_object.base.dimension.height = 1

        moving_object.base.position.x = 0.0 + i
        moving_object.base.position.y = 0.0 
        moving_object.base.position.z = 0.0

        moving_object.base.orientation.roll = 0.0
        moving_object.base.orientation.pitch = 0.0
        moving_object.base.orientation.yaw = 0.0 

        """Serialize SensorData which can be send"""
        bbuffer = sensorview.SerializeToString()
        f.write(struct.pack("<L", len(bbuffer)) + bbuffer)

    f.close()
 
if __name__ == "__main__":
    main()
```
Type in the terminal:
```bash
$ python3 newencodeOSI.py
```

#### Decode without seperator
Decode the generated OSI trace.
```python
from newdecodeOSI import OSITrace

if __name__ == "__main__":
    trace = OSITrace()
    trace.from_file(path="test_trace_new.txt")

    # Print all messages
    sv = trace.get_messages()
    for i in sv:
        print(i)

    # Print the osi message in a interval (here from first to ninth)
    sv = trace.get_messages_in_index_range(0, 10)
    for i in sv:
        print(i)

    # Print the osi message by index (here the first)
    sv = trace.get_message_by_index(0)
    print(sv)

    # Save output into readable osi files
    trace.osi2read(name="test4.txth")
    trace.osi2read(name="test5.txth", index=1)
    trace.osi2read(name="test6.jstxthon", interval=(6, 10))
```
Type in the terminal:
```bash
$ python3 newdecodeOSI.py
```

#### Requirements
[OSI](https://github.com/OpenSimulationInterface/open-simulation-interface) >= 3.1.2
