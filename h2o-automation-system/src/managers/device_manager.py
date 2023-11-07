import sys
sys.path.append('../libs')  # Fügt das Verzeichnis libs zum PYTHONPATH hinzu
import json
from modbus_lib import ModbusClient

class DeviceManager:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.devices = {}
        self.init_devices()

    def load_config(self, config_path):
        with open(config_path, 'r') as file:
            return json.load(file)

    def init_devices(self):
        for device_config in self.config['devices']:
            device_id = device_config['device_id']
            self.devices[device_id] = ModbusClient(**device_config)

    def get_device(self, device_id):
        return self.devices.get(device_id)

# Example usage of DeviceManager
if __name__ == '__main__':
    config_path = '../../config/sensors_config.json'
    manager = DeviceManager(config_path)
    # Loop through the devices and read the registers as per configuration
    for device_id, device in manager.devices.items():
        print(f"Testing device {device_id}")
        for reg in device.config['registers']:
            result = device.read_register(reg['address'], reg['length'], reg['format'])
            print(f"Read from {reg['name']}: {result}")