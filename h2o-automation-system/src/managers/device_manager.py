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
        modbus_config = {
            'port': self.config['modbus_port'],
            'baudrate': self.config['modbus_baudrate'],
            'parity': self.config['modbus_parity'],
            'stopbits': self.config['modbus_stopbits'],
            'bytesize': self.config['modbus_bytesize'],
            'timeout': self.config['modbus_timeout']
        }

        for device_config in self.config['devices']:
            device_id = device_config['device_id']
            self.devices[device_id] = ModbusClient(self, device_id, **modbus_config)

            for register in device_config['registers']:
                # Hier können Sie Logik hinzufügen, um die Registerkonfigurationen zu verarbeiten.
                # Zum Beispiel könnten Sie diese Informationen nutzen, um Polling-Intervalle zu planen.
                pass

    def get_device(self, device_id):
        return self.devices.get(device_id)

# Beispiel für die Verwendung des DeviceManagers
if __name__ == '__main__':
    config_path = '../../config/sensors_config.json'
    manager = DeviceManager(config_path)
    radar_sensor = manager.get_device(1)
    turbidity_sensor = manager.get_device(2)
    ph_sensor = manager.get_device(3)

    for device_id in manager.devices:
        device = manager.get_device(device_id)
        print(f"Testing device {device_id}")
        for reg in manager.config['devices'][device_id - 1]['registers']:  # Indexierung sollte 0-basiert sein
            result = device.read_register(reg['address'], reg['length'], reg['format'])
            print(f"Read from {reg['name']}: {result}")