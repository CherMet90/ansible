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

# Organize devices dynamically into groups
inventory = {'all': {'children': {}}}

for device in devices:
    if device.device_type.manufacturer.slug == 'noname':
        continue
    logger.info(f'Processing {device.display}...')
    site_name = device.site.slug if device.site else "Unknown"
    role_name = device.device_role.slug if device.device_role else "Unknown"
    manufacturer_name = device.device_type.manufacturer.slug if device.device_type.manufacturer else "Unknown"
    device_type_name = device.device_type.slug if device.device_type else "Unknown"

    # Fetch interfaces for the given device
    interfaces = NetboxDevice.get_netbox_objects('dcim.interfaces', action='filter', device_id=device.id)
    device_interfaces = []
    for interface in interfaces:
        device_interfaces.append({
            "name": interface.name,
            "type": interface.type.value,
            "mode": interface.mode and str(interface.mode.value),
        })

    device_info = {
        "ansible_host": device.primary_ip.address.split('/')[0] if device.primary_ip else "no_ip",
        "interfaces": device_interfaces,
    }

    # Add device to groups
    groups = [site_name, role_name, manufacturer_name, device_type_name]
    for group in groups:
        # Sanitize the group name
        group = group.replace('-', '_')
        if group not in inventory['all']['children']:
            inventory['all']['children'][group] = {'hosts': {}}
        inventory['all']['children'][group]['hosts'][device.display] = device_info

logger.info('Dynamic hierarchical organizing completed')

# Write the inventory into a YAML file
inventory_path = '../inventories/prod/all_devices.yml'
with open(inventory_path, 'w') as f:
    yaml.dump(inventory, f, allow_unicode=True, sort_keys=False)
logger.info('Ansible inventory YAML file created successfully')