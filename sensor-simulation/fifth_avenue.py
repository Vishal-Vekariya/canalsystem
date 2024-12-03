import time
import random
from azure.iot.device import IoTHubDeviceClient, Message

# Replace with your IoT Hub device connection string for Fifth Avenue
CONNECTION_STRING = "HostName=canalsystem.azure-devices.net;DeviceId=fifth_avenue;SharedAccessKey=L9M8N+flnp8BZXfTf3Q/U737qThpbZyt5DVIAI2J7cI="

def get_telemetry():
    return {
        "location": "fifth avenue",
        "iceThickness": round(random.uniform(15.0, 35.0), 2),
        "surfaceTemperature": round(random.uniform(-5.0, 5.0), 2),
        "snowAccumulation": round(random.uniform(0.0, 15.0), 2),
        "externalTemperature": round(random.uniform(-10.0, 10.0), 2),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

def main():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    try:
        print("Sending telemetry for Fifth Avenue...")
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
