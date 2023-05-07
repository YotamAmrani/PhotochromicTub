import serial
import getch
import time
import pygame
from pygame.locals import *

MICRO = 1000000

# Open a serial connection to the machine
ser = serial.Serial('COM5', baudrate=115200, timeout=1)
JOG_COMMAND_PREFIX_LEN = 7
FEED_RATE = 600
STEP = 2
# STEP = (FEED_RATE // 600)  # https://github.com/gnea/grbl/issues/837
LED_MODE = False
BUTTON_DELAY = 0.1


# Boarders Limits:
current_pos_x = 0
current_pos_y = 0
current_pos_z = 0
STATE = "idle"
STATE_UPDATED = False
X_END_LIMIT = 130
Y_END_LIMIT = 100
Z_END_LIMIT = 100

X_START_ALARM = False
Y_START_ALARM = False
Z_START_ALARM = False
X_END_ALARM = False
Y_END_ALARM = False
Z_END_ALARM = False


def get_position():
    ser.write("?\n".encode())
    response = ""
    for l in ser.readlines():
        if "|" in l.decode():
            response = l.decode()
    m_pos = response.split("|")[1]
    m_pos = m_pos.split(":")[1]
    positions = m_pos.split(",")
    positions = [float(p) for p in positions]
    print("System Mpos: ")
    print(positions)
    print("Script Positions: ")
    print([current_pos_x,current_pos_y,current_pos_z])
    return positions


def get_state():
    response = ser.write("?\n".encode())
    line = ser.readline().decode()

    while line == "ok\r\n" or line.isdigit():
        line = ser.readline().decode()
    state = line.split("|")[0]

    return state[1:]


def move_left(step):
    global current_pos_x
    global GC_MOVE_COMMAND
    current_pos_x += step
    movement_line += "x" + str(step) + " "


def move_right(step):
    global current_pos_x
    global GC_MOVE_COMMAND
    current_pos_x -= step
    movement_line += "x-" + str(step) + " "


def move_up(step):
    global current_pos_z
    global GC_MOVE_COMMAND
    current_pos_z += step
    movement_line += "z" + str(step) + " "


def move_down(step):
    global current_pos_z
    global GC_MOVE_COMMAND
    current_pos_z -= step
    movement_line += "z-" + str(step) + " "


def move_front(step):
    global current_pos_y
    global GC_MOVE_COMMAND
    current_pos_y += step
    movement_line += "y" + str(step) + " "


def move_back(step):
    global current_pos_y
    global GC_MOVE_COMMAND
    current_pos_y -= step
    movement_line += "y-" + str(step) + " "


def set_feed_rate(feed_rate):
    global GC_MOVE_COMMAND
    movement_line += " F" + str(feed_rate) + "\n"


def send_move():
    global GC_MOVE_COMMAND
    print(movement_line)
    ser.write(movement_line.encode())
    response = ser.readline().decode()
    return response


def auto_home():
    time.sleep(2)
    t0 = time.time()
    response = ser.write("$H\n".encode())  # AutoHome
    print(response)
    response = ser.write("G10 P0 L20 X0 Y0 Z0\n".encode())
    print(response)

    response = ser.write("?\n".encode())

    while str(response).isdigit() or "ok" not in response:
        response = ser.readline().decode()
        # print(response)

    t1 = time.time()
    print("Auto-homing time: " + str(t1 - t0))


def print_file(file_name, delay_rate=1.5):
    global PRINT_MODE
    PRINT_MODE = True

    t0 = time.time()

    with open(file_name, 'r') as file:
        for line in file:
            ser.write(line.encode())
            response = ser.readline().decode()
            time.sleep(delay_rate)
            print(response.strip())
            print(line.strip())
    t1 = time.time()
    print("printing time: " + str(t1-t0))
    time.sleep(4)
    PRINT_MODE = False


def toggle_led():
    global LED_MODE
    print("toggled")
    if LED_MODE:
        ser.write("g1 M3 s0 f800\n".encode())
        response = ser.readline().decode()
        print(response.strip())
    else:
        ser.write("g1 M3 s1000 f800\n".encode())
        response = ser.readline().decode()
        print(response.strip())
    LED_MODE = not LED_MODE
    time.sleep(80000 / MICRO)
    # time.sleep(0.01)


def print_status():
    ser.write("?\n".encode())
    print_full_response()


def print_full_response():
    response = ser.readlines()
    for l in response:
        print(l.decode().strip())


def print_menu():
    print("HELLO THERE!")
    print("To move UP and DOWN press: Z and X keyboards respectively.")
    print("To move BACK and FORTH press: S and W keyboards respectively.")
    print("To move LEFT and RIGHT press: A and D keyboards respectively.")


pygame.init()
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
# https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
ser.flushInput()


""" Init the System"""
PRINT_MODE = False
JOYSTICK_IS_IDLE = False
auto_home()
print_menu()

""" Run the main loop """
while True:
    keys = pygame.key.get_pressed()

    """ Printing a file """
    if keys[K_p]:
        print_file("spiral.gcode")

    if keys[K_0]:
        response = ser.write("G10 P0 L20 X0 Y0 Z0\n".encode())
        print(response)

    if keys[K_l]:
        print_status()
        # get_position()
        print(get_state())

    """ Making action - User interface """
    if PRINT_MODE is False:
        if keys[K_1]:
            toggle_led()

        GC_MOVE_COMMAND = "$J=G91 "
        if keys[K_a]:
            move_left(STEP)
        elif keys[K_d]:
            move_right(STEP)
        if keys[K_w]:
            move_front(STEP)
        elif keys[K_s]:
            move_back(STEP)
        if keys[K_z]:
            move_up(STEP)
        if keys[K_x]:
            move_down(STEP)

        STATE_UPDATED = False

    # Exit
    if keys[K_q]:
        break
    if keys[K_ESCAPE]:
        response = ser.write("~\n".encode())
        print(response)

    # Apply movement
    if len(GC_MOVE_COMMAND) > JOG_COMMAND_PREFIX_LEN:
        set_feed_rate(FEED_RATE)
        send_move()

    # Update the current state
    elif not STATE_UPDATED:
        STATE_UPDATED = True
        STATE = get_state()
        print(State)

    # Delay for button press de-bounce
    time.sleep(BUTTON_DELAY)
    pygame.event.pump()
# Close the serial connection
ser.close()

# $X











# if keys[K_r]:
#     ser.write((chr(24) + "\n").encode())
# if keys[K_t]:
#     ser.write("$slp\n".encode())
# if keys[K_y]:
#     ser.write("$x\n".encode())

# key = bytes.decode(getch.getch())
# if key == 'w':
#     move_front(STEP)
# elif key == 's':
#     move_back(STEP)
#
# # Z axis
# if key == 'z':
#     move_up(STEP)
# elif key == 'x':
#     move_down(STEP)