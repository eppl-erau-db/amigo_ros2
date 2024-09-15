#ignore this it is only to check something 


import keyboard  

def on_key_event(event):
    if event.name == 'up':
        print("Up arrow pressed")
    elif event.name == 'down':
        print("Down arrow pressed")
    elif event.name == 'left':
        print("Left arrow pressed")
    elif event.name == 'right':
        print("Right arrow pressed")


print("Press the arrow keys. Press 'Esc' to exit.")
keyboard.hook(on_key_event)
keyboard.wait('esc')
