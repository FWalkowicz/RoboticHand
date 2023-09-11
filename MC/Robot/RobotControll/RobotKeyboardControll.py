import requests
import keyboard

angle1 = 90
angle2 = 90
angle3 = 90
angle4 = 90

while True:
    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_DOWN:
        if event.name == 'q':
            break
        elif event.name == 'w':
            angle1 += 5
            response = requests.put('http://192.168.1.33:8000/engines/0?mode_angle={}'.format(angle1))
            print(response.text)
        elif event.name == 's':
            angle1 -= 5
            response = requests.put('http://192.168.1.33:8000/engines/0?mode_angle={}'.format(angle1))
            print(response.text)
        elif event.name == 'e':
            angle2 += 5
            response = requests.put('http://192.168.1.33:8000/engines/1?mode_angle={}'.format(angle2))  
            print(response.text)
        elif event.name == 'd':
            angle2 -= 5
            response = requests.put('http://192.168.1.33:8000/engines/1?mode_angle={}'.format(angle2))
            print(response.text)
        elif event.name == 'r':
            angle3 += 5
            response = requests.put('http://192.168.1.33:8000/engines/3?mode_angle={}'.format(angle3))
            print(response.text)
        elif event.name == 'f':
            angle3 -= 5
            response = requests.put('http://192.168.1.33:8000/engines/3?mode_angle={}'.format(angle3))
            print(response.text)
        elif event.name == 't':
            angle4 += 5
            response = requests.put('http://192.168.1.33:8000/engines/2?mode_angle={}'.format(angle4))  
            print(response.text)
        elif event.name == 'g':
            angle4 -= 5
            requests.put('http://192.168.1.33:8000/engines/2?mode_angle={}'.format(angle4))
            print(response.text)
        elif event.name == 'i':
            angle1 = 90
            angle2 = 90
            angle3 = 90
            angle4 = 90
            response = requests.put('http://192.168.1.33:8000/init')
