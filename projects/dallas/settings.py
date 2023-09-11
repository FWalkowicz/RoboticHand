import json, uuid, re, os

# Function to validate ip choice
def validate_ip_port(ip_port):
    ip_pattern = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    port_pattern = r"^\d+$"

    ip, port = ip_port.split(":")
    if not re.match(ip_pattern, ip):
        return False
    if not re.match(port_pattern, port):
        return False
    return True

# Function to validate device_type choice
def validate_device_choice(choice):
    valid_choices = ["1", "2", "3"]
    return choice in valid_choices

# Mapping of device type choices to actual types
device_type_mapping = {
    "1": "Thermometer", # type: ignore
    "2": "Accelerometer", # type: ignore
    "3": "Gyroscope" # type: ignore
}

# Check if config.json exists and load existing data
config = {}
if os.path.exists("./dallas/config.json"):  # type: ignore
    with open("./dallas/config.json", "r") as config_file:
        config = json.load(config_file)

# If device_id already exists, use it, otherwise generate a new one
if "DEVICE_ID" in config:
    device_id = config["DEVICE_ID"]
else:
    device_id = str(uuid.uuid4())

# Get input from the user
if "IP" in config:
    config_ip = config["IP"]
    choice = input(f"The IP field already exists with value '{config_ip}'. Do you want to change it? (y/n): ").lower()
    if choice == 'y':
        ip_port = input("Enter IP address and port (format: xxx.xxx.xxx.xxx:port): ")
        while not validate_ip_port(ip_port):
            print("Invalid IP address or port format. Please try again.")
            ip_port = input("Enter IP address and port (format: xxx.xxx.xxx.xxx:port): ")
    if choice == 'n':
        ip_port = config["IP"]
else:
    ip_port = input("Enter IP address and port (format: xxx.xxx.xxx.xxx:port): ")
    while not validate_ip_port(ip_port):
        print("Invalid IP address or port format. Please try again.")
        ip_port = input("Enter IP address and port (format: xxx.xxx.xxx.xxx:port): ")

if "SSID" in config:
    config_ssid = config["SSID"]
    choice = input(f"The SSID field already exists with value '{config_ssid}'. Do you want to change it? (y/n): ").lower()
    if choice == 'y':
        ssid = input("Enter SSID: ")
    if choice == 'n':
        ssid = config["SSID"]
else:
    ssid = input("Enter SSID: ")

if "PASSWORD" in config:
    config_password = config["PASSWORD"]
    choice = input(f"The password field already exists with value '{config_password}'. Do you want to change it? (y/n): ").lower()
    if choice == 'y':
        password = input("Enter password: ")
    if choice == 'n':
        password = config["PASSWORD"]
else:
    password = input("Enter password: ")

if "DEVICE_NAME" in config:
    config_name = config["DEVICE_NAME"]
    choice = input(f"The device_name field already exists with value '{config_name}'. Do you want to change it? (y/n): ").lower()
    if choice == 'y':
        device_name = input("Enter device name: ")
    if choice == 'n':
        device_name = config["DEVICE_NAME"]
else:
    device_name = input("Enter device name: ")

if "DEVICE_TYPE" in config:
    config_type = config["DEVICE_TYPE"]
    choice = input(f"The device_type field already exists with value '{config_type}'. Do you want to change it? (y/n): ").lower()
    if choice == 'y':
        print("Choose a device type:")
        print("1. Thermometer")
        print("2. Accelerometer")
        print("3. Gyroscope")
        choice = input("Enter the number of your choice: ")
        while not validate_device_choice(choice):
            print("Invalid choice. Please choose a valid number.")
            choice = input("Enter the number of your choice: ")
        device_type = device_type_mapping[choice]
    if choice == 'n':
        device_type = config["DEVICE_TYPE"]
else:
    print("Choose a device type:")
    print("1. Thermometer")
    print("2. Accelerometer")
    print("3. Gyroscope")
    choice = input("Enter the number of your choice: ")
    while not validate_device_choice(choice):
        print("Invalid choice. Please choose a valid number.")
        choice = input("Enter the number of your choice: ")
    device_type = device_type_mapping[choice]

# Create a dictionary to store the configuration
config = {
    "IP": ip_port,  # type: ignore
    "SSID": ssid,  # type: ignore
    "PASSWORD": password,  # type: ignore
    "DEVICE_NAME": device_name,  # type: ignore
    "DEVICE_TYPE": device_type,  # type: ignore
    "DEVICE_ID": device_id,  # type: ignore
}

# Save the configuration to config.json
with open("./dallas/config.json", "w") as config_file:
    json.dump(config, config_file, indent=4)  # type: ignore

print("Configuration saved to config.json")
