import serial
import getch
import time
import pygame
from pygame.locals import *

MICRO = 1000000

# Open a serial connection to the machine
printer_ser = serial.Serial('COM5', baudrate=115200, timeout=1)
# joystick_ser = serial.Serial('COM13', baudrate=115200, timeout=1)

JOG_COMMAND_PREFIX_LEN = 7
FEED_RATE = 600
STEP = 2
# STEP = (FEED_RATE // 600)  # https://github.com/gnea/grbl/issues/837
LED_MODE = False
LED_POWER = 1000
BUTTON_DELAY = 0.1
ALARM_IS_SET = False

ENABLE_MOTION = False


def auto_home():
    time.sleep(2)
    t0 = time.time()
    response = printer_ser.write("$H\n".encode())  # AutoHome
    print(response)
    response = printer_ser.write("G10 P0 L20 X0 Y0 Z0\n".encode())
    print(response)
    response = printer_ser.write(("G1 F600 M3 s" + str(LED_POWER) + "\n").encode())
    print(response)
    response = printer_ser.write("G1 M3 s0\n".encode())
    print(response)

    response = printer_ser.write("?\n".encode())

    while str(response).isdigit() or "ok" not in response:
        response = printer_ser.readline().decode()
        print(response)

    t1 = time.time()
    print("Auto-homing time: " + str(t1 - t0))
    # time.sleep(5)


def print_menu():
    print("HELLO THERE!")
    print("To move UP and DOWN press: Z and X keyboards respectively.")
    print("To move BACK and FORTH press: S and W keyboards respectively.")
    print("To move LEFT and RIGHT press: A and D keyboards respectively.")


def get_state():
    response = printer_ser.write("?\n".encode())
    line = printer_ser.readline().decode()

    while line == "ok\r\n" or line.isdigit():
        line = printer_ser.readline().decode()
    state = line.split("|")[0]

    return state[1:]


def move_left(step=0):
    global current_pos_x
    global GC_MOVE_COMMAND
    # movement_line += "x" + str(current_pos_x + step) + " "
    # current_pos_x += step
    movement_line += "x" + str(step) + " "


def move_right(step=0):
    global current_pos_x
    global GC_MOVE_COMMAND
    # movement_line += "x" + str(current_pos_x - step) + " "
    # current_pos_x -= step
    movement_line += "x-" + str(step) + " "


def move_up(step=0):
    global current_pos_z
    global GC_MOVE_COMMAND
    # movement_line += "z" + str(current_pos_z + step) + " "
    # current_pos_z += step
    movement_line += "z" + str(step) + " "


def move_down(step=0):
    global current_pos_z
    global GC_MOVE_COMMAND
    # movement_line += "z" + str(current_pos_z - step) + " "
    # current_pos_z -= step
    movement_line += "z-" + str(step) + " "


def move_front(step=0):
    global current_pos_y
    global GC_MOVE_COMMAND
    # movement_line += "y" + str(current_pos_y + step) + " "
    # current_pos_y += step
    movement_line += "y" + str(step) + " "


def move_back(step=0):
    global current_pos_y
    global GC_MOVE_COMMAND
    # movement_line += "y" + str(current_pos_y - step) + " "
    # current_pos_y -= step
    movement_line += "y-" + str(step) + " "


def set_feed_rate(feed_rate):
    global GC_MOVE_COMMAND
    movement_line += " F" + str(feed_rate) + "\n"


def send_move():
    global GC_MOVE_COMMAND
    global prev_movement_line
    print(movement_line)
    # if prev_movement_line is not movement_line and get_state() == "Jog":
    #     change_direction()
    prev_movement_line = movement_line
    printer_ser.write(movement_line.encode())
    response = printer_ser.readline().decode()
    # print(response)
    return response


def print_file(file_name, delay_rate=1.5):
    global PRINT_MODE
    PRINT_MODE = True

    t0 = time.time()
    with open(file_name, 'r') as file:
        for line in file:
            response = printer_ser.write(line.encode())
            response = printer_ser.readline()
            if not str(response).isdigit():
                response = response.decode()
                time.sleep(delay_rate)
                print(response.strip())
                print(line.strip())
            if "ALARM:1" in str(response):
                global ALARM_IS_SET
                ALARM_IS_SET = True
                PRINT_MODE = False
                print("ALARM:1 - error has occurred!")
                break

    t1 = time.time()
    print("printing time: " + str(t1-t0))
    time.sleep(4)
    PRINT_MODE = False


def toggle_led():
    global LED_MODE
    global LED_POWER
    global GC_MOVE_COMMAND
    print("toggled")
    if LED_MODE:
        # movement_line += " M3 s0"
        printer_ser.write("$j=g91 x0 M3 s0 f800\n".encode())
        response = printer_ser.readline().decode()
        print(response.strip())
    else:
        # movement_line += " M3 s" + str(LED_POWER)
        printer_ser.write("$j=g91 x0 M3 s1000 f800\n".encode())
        response = printer_ser.readline().decode()
        print(response.strip())
    LED_MODE = not LED_MODE
    time.sleep(80000 / MICRO)
    # time.sleep(0.01)


def print_status():
    printer_ser.write("?\n".encode())
    print_full_response()


def print_full_response():
    response = printer_ser.readlines()
    for l in response:
        print(l.decode().strip())


def clear_commands_queue():
    # if get_state() == "Jog":
        # res = printer_ser.write("!\n".encode())
    res = printer_ser.write('\x85\r\n'.encode())

    # time.sleep(1)
    print(res)
    print("Cleared Jog Buffer ! \n")


def change_direction():
    clear_commands_queue()
    time.sleep(0.1)


pygame.init()
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
# https://www.geeksforgeeks.org/python-display-text-to-pygame-window/


# print_file('initialize.gcode', 0.5)
printer_ser.flushInput()
# Wait for a key press


joystick_idle = False
PRINT_MODE = False
# keys = pygame.key.get_pressed()

auto_home()
print_menu()
prev_movement_line = ""
GC_MOVE_COMMAND = ""

while True:
    keys = pygame.key.get_pressed()
    """ Case an error occurred: reset and auto home"""
    if keys[K_b]:
        response = printer_ser.write("$RST\n".encode())
        print(response)
        print_full_response()
        ALARM_IS_SET = False

    """ Printing a file """
    if keys[K_p]:
        # auto_home()
        print_file("spiral.gcode", 4)

    if keys[K_0]:
        response = printer_ser.write("$H\n".encode())
        print(response)
        response = printer_ser.write("G10 P0 L20 X0 Y0 Z0\n".encode())
        print(response)

    if keys[K_l]:
        print_status()

    if PRINT_MODE is False:
        """ Making action """
        # movement_line = "G1 "
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
        elif keys[K_x]:
            move_down(STEP)

        # Turning on and off led
        if keys[K_1]:
            toggle_led()



    # Exit
    if keys[K_q]:
        break
    if keys[K_ESCAPE]:
        response = printer_ser.write("~\n".encode())
        print(response)

    # Apply movement
    if len(GC_MOVE_COMMAND) > JOG_COMMAND_PREFIX_LEN:
        set_feed_rate(FEED_RATE)
        send_move()
        joystick_idle = True

    # Based on the recommended implementation of jog mode:
      # https://github.com/gnea/grbl/blob/master/doc/markdown/jogging.md
    # while joystick is in use -> send commands to the buffer, elsewhere -> clear the commands buffer
    # to reach minimal latency.
    elif joystick_idle:
        joystick_idle = False
        time.sleep(0.1)
        # if get_state() == "Jog":
        clear_commands_queue()
        # else:
        #     print(get_state())
        print_full_response()

    # Delay for button press debounce
    time.sleep(BUTTON_DELAY)
    pygame.event.pump()
# Close the serial connection
printer_ser.close()

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