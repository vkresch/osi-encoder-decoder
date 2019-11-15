# OSI encoder / decoder
The encoder enables to encode multiple OSI messages into one file. The decoder can parse the generated file and output it in a human readable xml-like *.osi format.

## Usage

#### Encode
Encode ten OSI messages in the file `test_scenario.txt` which change the dimensions and the x-position of a stationary object over time:
```python
from osi3.osi_sensorview_pb2 import SensorView

def main():
    """Initialize SensorView"""
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

        with open("test_scenario.txt", "ab") as f:
            f.write(string_buffer + b"$$__$$")
 
if __name__ == "__main__":
    main()
```
Type in the terminal:
```bash
$ python3 encodeOSI.py
```

#### Decode
Decode the generated OSI scenario.
```python
from decodeOSI import OSIScenario

if __name__ == "__main__":
    scenario = OSIScenario()
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
    scenario.bin2osi(name="test1.osi")
    scenario.bin2osi(name="test2.osi", index=1)
    scenario.bin2osi(name="test3.osi", interval=(6, 10))
```
Type in the terminal:
```bash
$ python3 decodeOSI.py
```

#### Requirements

OSI >= 3.1.2
