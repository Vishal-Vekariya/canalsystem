import time
import random
from azure.iot.device import IoTHubDeviceClient, Message

# Replace your IoT Hub device connection string for Dow's Lake
CONNECTION_STRING = "HostName=canalsystem.azure-devices.net;DeviceId=dows_lake;SharedAccessKey=IFYn8V37iNOHcdkYTNMogtdq+hisg52nCkrAv1+szm8="

def get_telemetry():
    return {
        "location": "Dow's Lake",
        "iceThickness": round(random.uniform(15.0, 35.0), 2),
        "surfaceTemperature": round(random.uniform(-5.0, 5.0), 2),
        "snowAccumulation": round(random.uniform(0.0, 15.0), 2),
        "externalTemperature": round(random.uniform(-10.0, 10.0), 2),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

def main():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    try:
        print("Sending telemetry for Dow's Lake...")
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
