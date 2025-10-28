# SENSOR SIMULATION USING ASYNCIO
 
 This project is used for simulating Serial Communication Sensors For Testing and Processing using Asynchronous Programming


 ## Program Structure
1. **Sensor**
2. **Sensor Manager**
3. **KeyPressHandler**
4. **SerialWriter**
5. **SerialReader**
6. **SerialApp**

# Prerequisites 

- comOcom model emulate [(https://sourceforge.net/projects/com0com/)]
- Python 3.1x

# Installation Instructions

1. Download and Install com0com model emulator
2. Install Python 3.1x
3. Install Requirements using following command

    ```sh
    pip install -r Requirements.txt
    ```sh
# Configuration of Software

1. Setup Sensor Configuration and Serial Port Configuration in SerialConfig.yaml files.
2. Under Sensors add the required simulator sensor with parameters sensorname,min_value,max_value,Unit.
3. Add as many sensor you would like to simulate
4. Next comfigure Communcation port with parameters, Read_port, Write_Port and Data Interval.
4.  Finally, Configure Virtual Serial port.Open, com0com emualate, Setup com10, com11 (Virtual Port Pair3), select only emulate baud rate option (This wil virtualise Com port 10 and 11) and select apply 


# Running the Software

1. open Command Prompt in administrator mode.
2. Navigate to the Sensor Simulator folder
3. Run python script
´´´sh
    python SerialApp.py
´´´sh

