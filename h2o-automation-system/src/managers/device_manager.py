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
        for device_id, settings in self.config['devices'].items():
            self.devices[device_id] = ModbusClient(**settings)

    def get_device(self, device_id):
        return self.devices.get(device_id)

# Beispiel für die Verwendung des DeviceManagers
if __name__ == '__main__':
    config_path = 'path/to/your/sensors_config.json'
    manager = DeviceManager(config_path)
    radar_sensor = manager.get_device('radar_sensor')
    turbidity_sensor = manager.get_device('turbidity_sensor')
    ph_sensor = manager.get_device('ph_sensor')
