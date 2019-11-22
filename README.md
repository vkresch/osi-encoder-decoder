# OSI encoder / decoder
The encoder enables to encode multiple OSI messages into one file. The decoder can parse the generated file and output it in a human readable json-like format.

## Usage

#### Encode with seperator
Encode ten OSI messages in the file `test_scenario.txt` which change the dimensions and the x-position of a stationary object over time:
```python
from osi3.osi_sensorview_pb2 import SensorView

def main():
    """Initialize SensorView"""
    f = open("test_scenario.txt", "ab")
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

        f.write(string_buffer)
        f.write(b"$$__$$")

    f.close()
 
if __name__ == "__main__":
    main()
```
Type in the terminal:
```bash
$ python3 encodeOSI.py
```

#### Decode with seperator
Decode the generated OSI scenario.
```python
from decodeOSI import OSITrace

if __name__ == "__main__":
    scenario = OSITrace()
    scenario.from_file(path="test_scenario.txt")

    # Print all messages
    sv = scenario.get_messages()
    for i in sv:
        print(i)

    # Print the osi message in a interval (here from first to ninth)
    sv = scenario.get_messages_in_index_range(0, 10)
    for i in sv:
        print(i)

    # Print the osi message by index (here the first)
    sv = scenario.get_message_by_index(0)
    print(sv)

    # Save output into readable osi files
    scenario.txt2json(name="test1.json")
    scenario.txt2json(name="test2.json", index=1)
    scenario.txt2json(name="test3.json", interval=(6, 10))
```
Type in the terminal:
```bash
$ python3 decodeOSI.py
```

#### Convert from seperator scenario to length defined scenario

Type in the terminal:
```bash
$ python3 txt2osi.py -f small_test.txt
```

#### Encode without seperator
Encode ten OSI messages in the file `test_scenario.txt` which change the dimensions and the x-position of a stationary object over time:
```python
from osi3.osi_sensorview_pb2 import SensorView
import struct

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
```
Type in the terminal:
```bash
$ python3 newencodeOSI.py
```

#### Decode without seperator
Decode the generated OSI scenario.
```python
from newdecodeOSI import OSITrace

if __name__ == "__main__":
    scenario = OSITrace()
    scenario.from_file(path="test_scenario_new.txt")

    # Print all messages
    sv = scenario.get_messages()
    for i in sv:
        print(i)

    # Print the osi message in a interval (here from first to ninth)
    sv = scenario.get_messages_in_index_range(0, 10)
    for i in sv:
        print(i)

    # Print the osi message by index (here the first)
    sv = scenario.get_message_by_index(0)
    print(sv)

    # Save output into readable osi files
    scenario.osi2json(name="test4.json")
    scenario.osi2json(name="test5.json", index=1)
    scenario.osi2json(name="test6.json", interval=(6, 10))
```
Type in the terminal:
```bash
$ python3 newdecodeOSI.py
```

#### Requirements

OSI >= 3.1.2
