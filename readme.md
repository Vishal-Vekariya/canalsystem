# Rideau Canal Skateway Monitoring System

## Scenario Description

The Rideau Canal Skateway in Ottawa is a globally recognized attraction and UNESCO World Heritage Site. It attracts millions of visitors annually, but its ice conditions and weather factors must be constantly monitored to ensure skater safety. 

The National Capital Commission (NCC) requires a **real-time monitoring system** to:
1. Simulate IoT sensors to monitor ice conditions and weather factors at three key locations (Dow's Lake, Fifth Avenue, and the NAC).
2. Process incoming sensor data to detect unsafe conditions in real time.
3. Store aggregated results in Azure Blob Storage for analysis and decision-making.

This project leverages **Azure IoT Hub**, **Azure Stream Analytics**, and **Azure Blob Storage** to build a scalable and reliable monitoring solution.

---

# System Architecture

The Rideau Canal Skateway Monitoring System is structured as follows:

1. **IoT Sensor Simulation**:
   - Sensors at three locations simulate real-time data every 10 seconds, including:
     - Ice Thickness (cm)
     - Surface Temperature (°C)
     - Snow Accumulation (cm)
     - External Temperature (°C)
   - JSON payloads are sent to **Azure IoT Hub**.

2. **Azure IoT Hub**:
   - Acts as the central message broker, receiving data from simulated IoT sensors and forwarding it to **Azure Stream Analytics**.

3. **Azure Stream Analytics**:
   - Processes sensor data in real time and performs the following:
     - Aggregates data over 5-minute tumbling windows for each location.
     - Calculates average ice thickness and maximum snow accumulation.
   - Outputs processed data to **Azure Blob Storage**.

4. **Azure Blob Storage**:
   - Stores aggregated data in a structured format for further analysis and historical recordkeeping.

## System Diagram

```mermaid
graph TD
    subgraph IoT Sensors
        A[Dow's Lake] --> B[Azure IoT Hub]
        C[Fifth Avenue] --> B
        D[NAC] --> B
    end
    
    B --> E[Azure Stream Analytics]
    E --> F[Azure Blob Storage]
```
---

# Implementation Details

### 1. IoT Sensor Simulation

The **IoT Sensor Simulation** generates JSON payloads every 10 seconds. Each payload includes the following attributes:

| Attribute          | Description                                  |
|--------------------|----------------------------------------------|
| `location`         | Location of the sensor (e.g., Dow's Lake).  |
| `iceThickness`     | Thickness of the ice in centimeters.        |
| `surfaceTemperature` | Temperature of the ice surface in Celsius. |
| `snowAccumulation` | Snow accumulation on the ice in centimeters.|
| `externalTemperature` | Ambient temperature in Celsius.           |
| `timestamp`        | UTC timestamp of the data.                  |

### Example JSON Payload

```json
{
  "location": "Dow's Lake",
  "iceThickness": 27,
  "surfaceTemperature": -1,
  "snowAccumulation": 8,
  "externalTemperature": -4,
  "timestamp": "2024-11-23T12:00:00Z"
}
```


---

## Prerequisites

Before running the IoT sensor simulation scripts (`fifth_avenue.py`, `dows_lake.py`, `nac.py`), ensure Python is installed on your system. If Python is not installed, follow the steps below to install Python on a Linux system.

### Installing Python on Linux

1. **Update the System**:
   - Open a terminal and update your package manager:
     ```bash
     sudo apt update && sudo apt upgrade
     ```

2. **Check for Existing Python Installation**:
   - Verify if Python is already installed:
     ```bash
     python3 --version
     ```
   - If Python is installed, you will see the version number. If not, proceed to the next step.

3. **Install Python**:
   - Install Python 3 using the package manager:
     ```bash
     sudo apt install python3
     ```

4. **Install pip (Python Package Manager)**:
   - Ensure `pip`, the Python package manager, is installed for managing dependencies:
     ```bash
     sudo apt install python3-pip
     ```

5. **Verify the Installation**:
   - Check the installed versions of Python and pip:
     ```bash
     python3 --version
     pip3 --version
     ```

---

# Connecting Azure IoT Hub with Azure Stream Analytics to Process Streaming Data

---

## Step 1: Set Up Azure IoT Hub

### 1. Create an IoT Hub

1. Log in to the **[Azure Portal](https://portal.azure.com/)**.
2. Search for **IoT Hub** in the search bar and click **Create**.
3. Configure the IoT Hub:
   - **Subscription**: Select your subscription.
   - **Resource Group**: Choose an existing resource group or create a new one.
   - **Region**: Select your desired region (e.g., `Canada Central`).
   - **Tier**: Select **Free Tier** for testing purposes (if available).
   - **Name**: Provide a unique name for your IoT Hub (e.g., `RideauCanalIoTHub`).
4. Click **Review + Create**, then click **Create** to deploy the IoT Hub.

---

### 2. Register a Device

1. Open your IoT Hub in the Azure Portal.
2. Go to the **Devices** section and click **+ Add Device**.
3. Provide the following:
   - **Device ID**: Enter a unique identifier for the device (e.g., `FifthAvenueSensor`).
   - **Authentication Type**: Use `Symmetric Key`.
4. Click **Save**.
5. Once the device is created, click on the device name and copy its **Primary Connection String**. You will use this string in the Python script.

---

### 3. Install Required Libraries

To simulate IoT sensor data, install the **azure-iot-device** Python library:

```bash
pip install azure-iot-device
```

---

### 4. Run Python Scripts to Simulate Sensor Data

Use the Python script below to simulate telemetry data for a sensor. Replace the `CONNECTION_STRING` with the connection string copied earlier.

### Python Script (Fifth Avenue Sensor)

```python
import time
import random
from azure.iot.device import IoTHubDeviceClient, Message

# Replace with your IoT Hub device connection string
CONNECTION_STRING = "HostName=your-iot-hub.azure-devices.net;DeviceId=your-device-id;SharedAccessKey=your-key"

def get_telemetry():
    return {
        "location": "Fifth Avenue",
        "iceThickness": round(random.uniform(15.0, 35.0), 2),
        "surfaceTemperature": round(random.uniform(-5.0, 5.0), 2),
        "snowAccumulation": round(random.uniform(0.0, 15.0), 2),
        "externalTemperature": round(random.uniform(-10.0, 10.0), 2),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

def main():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    try:
        print("Sending telemetry...")
        while True:
            telemetry = get_telemetry()
            message = Message(str(telemetry))
            client.send_message(message)
            print(f"Sent: {message}")
            time.sleep(10)
    except KeyboardInterrupt:
        print("Stopped sending messages.")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
```

---

### 5. Run the Script

1. Save the script to a file, e.g., `fifth_avenue.py`.
2. Run the script to start sending telemetry data:
   ```bash
   python3 fifth_avenue.py
   ```

---

## Step 2. Creating Azure Blob Storage and Container

1. In the **[Azure Portal](https://portal.azure.com/)**, search for **Storage Accounts** and click **+ Create**.
2. Configure the Storage Account:
   - Provide a **unique name**, select your **resource group** and **region**, choose **Standard Performance**, and **LRS** redundancy.
   - Click **Review + Create** and then **Create**.
3. Once created, open the Storage Account, go to **Containers**, and click **+ Container**.
4. Enter a container name (e.g., `iosoutput`), set **Public Access Level** to `Private`, and click **Create**.


## Step 3: Create and Configure a Stream Analytics Job

### 1. Create the Stream Analytics Job

1. In the Azure Portal, search for **Stream Analytics Jobs** and click **Create**.
2. Configure the job:
   - **Name**: Provide a name for your job (e.g., `RideauCanalAnalytics`).
   - **Subscription**: Select your subscription.
   - **Resource Group**: Select the same resource group as your IoT Hub.
   - **Hosting Environment**: Choose **Cloud**.
3. Click **Review + Create**, then click **Create** to deploy the job.

---

### 2. Define Input

1. Open the Stream Analytics job and go to the **Inputs** section.
2. Click **+ Add Input** and select **IoT Hub** as the input source.
3. Provide the following details:
   - **Input Alias**: `Input`
   - **IoT Hub Namespace**: Select your IoT Hub.
   - **IoT Hub Policy Name**: Use `iothubowner`.
   - **Consumer Group**: Use `$Default` or create a new one.
   - **Serialization Format**: Select `JSON`.
4. Save the input configuration.

---

### 3. Define Output

1. Go to the **Outputs** section and click **+ Add Output**.
2. Select **Blob Storage** as the output destination.
3. Provide the following details:
   - **Output Alias**: `Output`
   - **Storage Account**: Select your Azure Storage Account.
   - **Container**: Create or choose an existing container for storing results.
   - **Path Pattern**: Optionally, define a folder structure, e.g., `output/{date}/{time}`.
4. Save the output configuration.

---

### 4. Write the Stream Analytics Query

1. Open the **Query** tab of the Stream Analytics job.
2. Replace the default query with the following:

```sql
SELECT
    location AS Location,
    AVG(iceThickness) AS AverageIceThickness,
    MAX(snowAccumulation) AS MaximumSnowAccumulation,
    System.Timestamp AS EventTime
INTO
    BlobOutput
FROM
    IoTHubInput
GROUP BY
    location,
    TumblingWindow(second, 60)
```

---

### 5. Start the Stream Analytics Job

1. Save the query.
2. Click **Start** to begin processing data in real time.

---

## Step 4: Verify the Output

### 1. Monitor the Stream Analytics Job

1. Navigate to the **Monitoring** tab of the job.
2. Check the metrics to ensure data is being processed.

### 2. Check Blob Storage

1. Open your Azure Storage Account in the Azure Portal.
2. Navigate to the container you specified in the output configuration.
3. Verify that processed data is being stored in JSON format. Each file contains aggregated data.

--- 

## Usage Instructions

### Running the IoT Sensor Simulation

1. **Set Up Python Environment**:
   - Ensure Python 3 is installed. 
   - Install required dependencies:
     ```bash
     pip install azure-iot-device
     ```

2. **Run Simulation Scripts**:
   - Navigate to the directory containing the IoT simulation scripts.
   - Run each simulation script in separate terminals for different locations:
     ```bash
     python3 fifth_avenue.py
     python3 dows_lake.py
     python3 nac.py
     ```
   - Verify messages are being sent to the IoT Hub in the Azure Portal.

---

## Configuring Azure Services

1. **Set Up IoT Hub**:
   - Create an IoT Hub in the Azure Portal and register devices (`fifth_avenue`, `dows_lake`, `nac`).
   - Copy device connection strings and replace them in the simulation scripts.

2. **Create Blob Storage and Container**:
   - Create a storage account and container (`iosstorage1999`) to store the processed results. 

3. **Configure and Start Stream Analytics Job**:
   - Create a Stream Analytics Job with IoT Hub as input and Blob Storage as output.
   - Use the provided query to calculate metrics and store results in Blob Storage:

     ```sql
     select 
input. location AS Locations,
AVG(input. iceThickness) AS AveragelceThickness,
MAX(input. snowAccumu1ation) AS maximumsnowAccumu1ation,
System. Timestamp AS EventTime
INTO
[output]
FRC*I
[input]
GROUP BY
input. location,
Tumblingwindow(second , 60)
     ```
   - Start the Stream Analytics job.

---

## Accessing Stored Data

1. **View Processed Data in Blob Storage**:
   - Open the Blob Storage account in the Azure Portal.
   - Navigate to the `iosstorage1999` container.
   - Locate files organized by timestamp, e.g.:
     ```
     iosstorage1999/
       iotoutput/
         O_019b6651163441 bfb6fb9f1ab72d1d60_1 .json.json
         019b6651163441 bfb6fb9f1ab72d1d60_1 .json.json
     ```

2. **Download or Analyze Files**:
   - Download JSON files for further analysis or visualization in tools like Power BI or Excel. 


---

## Challenges Faced

1. **Data Synchronization**:
   - Ensuring consistent timestamps across simulated sensors was complex.
   - Solution: Used Python’s `time.sleep` to maintain timing intervals.

2. **IoT Hub Message Routing**:
   - Initial routing misconfigurations caused delays in data delivery.
   - Solution: Updated IoT Hub endpoints and verified routing rules.

3. **Query Optimization**:
   - Ensuring efficient query execution in Azure Stream Analytics required iterative testing.
   - Solution: Simplified SQL queries and used proper indexing.

---

## Results

```json
  { "Locations":"NAC",
    "AverageIceThickness":25.186,
    "MaximumSnowAccumulation":8.83,
    "EventTime":"2024-11-27T00:18:00.0000000Z"
  }
  ```

- The aggregated metrics consist of:
- The average ice thickness.
- The maximum snow accumulation.
- The event's timestamp.

## Authors

- **Vishal Vekariya**
- **Arish Kakadiya**
- **Fattehali Sunasara**

---
