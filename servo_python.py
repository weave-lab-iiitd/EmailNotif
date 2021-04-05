import subprocess as s
import pyfirmata
import time

board = pyfirmata.Arduino('/dev/cu.usbmodem1201')
#print(board)

#s.call(['notify-send','foo','bar'])

"""
val: 20 stop
val: 23, slow rotation, anti-clkw
val: 167-168 fast rot, anti-clkw
val: 1-2 fast rot, clockw
cal: 17-18, slow rot, clockw

"""


"""
while True:
    board.digital[13].write(1)
    time.sleep(1)
    board.digital[13].write(0)
    time.sleep(1)
"""
#from gi.repository import Notify

def my_callback_func():
    pass

it = pyfirmata.util.Iterator(board)
it.start()

servo_pin = board.get_pin('d:9:s')
#servo_pin.write(0)
#servo_pin.write(23)
#time.sleep(1)
#servo_pin.write(20)
#time.sleep(1)
#servo_pin.write(90)

"""
while True:
    servo_pin.write(17)
    time.sleep(0.0428)
    servo_pin.write(20)
    time.sleep(2)
"""
count = 1
for i in range(0,10):
    
    servo_pin.write(17)
    time.sleep(0.0428)
    servo_pin.write(20)
    time.sleep(3)
    print("Received new email, count: ", count)
    count += 1

"""
# One time initialization of libnotify
Notify.init("My Program Name")

# Create the notification object
summary = "Calls"
body = "Missed Call from Mom!"
notification = Notify.Notification.new(
    summary,
    body, # Optional
)

notification.add_action(
    "action_click",
    "Reply to Message",
    my_callback_func,
    None # Arguments
)
"""


# Actually show on screen
#notification.show()
