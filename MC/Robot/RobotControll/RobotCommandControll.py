import requests
import time
with open('command.txt', 'r') as file:
    for line in file:
        words = line.strip().split()
        if words:
            command = words[0]
            arguments = words[1:]

            if command == 'init':
                response = requests.put('http://192.168.1.33:8000/init')
                time.sleep(0.5)
            elif command == 'move':
                response = requests.put('http://192.168.1.33:8000/engines/{}?mode_angle={}'.format(arguments[0], arguments[1]))
                if response.status_code != 200:
                    print(response.text)
                time.sleep(0.5)
            else:
                print('Unknow command')
            