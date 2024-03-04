import json
import yaml
from custom_modules.netbox_connector import NetboxDevice
from custom_modules.log import logger

# Load the configuration from the YAML file
with open('netbox_inventory.yml', 'r') as file:
    config = yaml.safe_load(file)

netbox_query = config['netbox_query']
path = netbox_query['path']
action = netbox_query['action']
search_params = netbox_query.get('search_params', {})

# Establish a connection to Netbox
NetboxDevice.create_connection()

# Fetch the devices
devices = NetboxDevice.get_netbox_objects(path, action=action, **search_params)
logger.info('Netbox generator successfully created')

# Organize devices hierarchically
hierarchy = {}

for device in devices:
    site_name = device.site.slug if device.site else "Unknown"
    role_name = device.device_role.slug if device.device_role else "Unknown"
    manufacturer_name = device.device_type.manufacturer.slug if device.device_type.manufacturer else "Unknown"
    device_type_name = device.device_type.slug if device.device_type else "Unknown"

    # Initialize dictionaries as needed
    if site_name not in hierarchy:
        hierarchy[site_name] = {}
    if role_name not in hierarchy[site_name]:
        hierarchy[site_name][role_name] = {}
    if manufacturer_name not in hierarchy[site_name][role_name]:
        hierarchy[site_name][role_name][manufacturer_name] = {}
    if device_type_name not in hierarchy[site_name][role_name][manufacturer_name]:
        hierarchy[site_name][role_name][manufacturer_name][device_type_name] = []

    # Append the device to the appropriate list
    hierarchy[site_name][role_name][manufacturer_name][device_type_name].append({
        "name": device.name,
        "primary_ip": device.primary_ip.address.split('/')[0] if device.primary_ip else "no_ip"
    })
logger.info('Hierarchical organizing completed')

# Формируем итоговый инвентарь
inventory = {'hierarchy': hierarchy}

logger.info('Creating JSON file...')
with open('../inventories/prod/all_devices.json', 'w') as f:
    json.dump(inventory, f, indent=4)