import serial
import time
import pygame
from pygame.locals import *

JOG_COMMAND_PREFIX_LEN = 7
MICRO = 1000000
joystick_idle = False
PRINT_MODE = False


# LED configurations
TOGGLE_LED = False
LED_MODE = False
LED_POWER = 1000
BUTTON_DELAY = 0.01
ALARM_IS_SET = False

# Movement configurations
FEED_RATE = 1800 # STEP = ~(FEED_RATE // 600)  # https://github.com/gnea/grbl/issues/837
STEP_SIZE = 0.3  # step size will change the DUP bug for some reason
PREV_MOVEMENT_VECTOR = [0, 0, 0]
MOVEMENT_VECTOR = [0, 0, 0]
GC_MOVE_COMMAND = ""
X_INDEX = 0
Y_INDEX = 1
Z_INDEX = 2


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


def apply_movement():
    global MOVEMENT_VECTOR
    global GC_MOVE_COMMAND
    GC_MOVE_COMMAND += " X" + str(MOVEMENT_VECTOR[X_INDEX])
    GC_MOVE_COMMAND += " Y" + str(MOVEMENT_VECTOR[Y_INDEX])
    GC_MOVE_COMMAND += " Z" + str(MOVEMENT_VECTOR[Z_INDEX])


def apply_led_toggle():
    global LED_MODE
    global LED_POWER
    global GC_MOVE_COMMAND
    LED_MODE = not LED_MODE
    if LED_MODE:
        GC_MOVE_COMMAND += " M3 S" + str(LED_POWER)
    else:
        GC_MOVE_COMMAND += " M3 S0"


def set_feed_rate(feed_rate):
    global GC_MOVE_COMMAND
    GC_MOVE_COMMAND += " F" + str(feed_rate) + "\n"


def send_move():
    global GC_MOVE_COMMAND
    # print(GC_MOVE_COMMAND)
    printer_ser.write(GC_MOVE_COMMAND.encode())
    response = printer_ser.readline().decode()
    print(response)
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
        GC_MOVE_COMMAND += " M3 s0"
        # printer_ser.write("$j=g91 x0 M3 s0 f800\n".encode())
        # response = printer_ser.readline().decode()
        # print(response.strip())
    else:
        GC_MOVE_COMMAND += " M3 s" + str(LED_POWER)
        # printer_ser.write("$j=g91 x0 M3 s1000 f800\n".encode())
        # response = printer_ser.readline().decode()
        # print(response.strip())
    # LED_MODE = not LED_MODE
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
    printer_ser.flushInput()
    printer_ser.flushOutput()
    res = printer_ser.write('\x85\r\n'.encode())

    # time.sleep(1)
    print("Cleared Jog Buffer ! \n")


def change_direction():
    clear_commands_queue()
    time.sleep(0.02)


# Open a serial connection to the machine
printer_ser = serial.Serial('COM5', baudrate=115200, timeout=1)
# Init UI screen
pygame.init()
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

# print_file('initialize.gcode', 0.5)
printer_ser.flushInput()
auto_home()
print_menu()






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
        GC_MOVE_COMMAND = "$J=G91 "
        if keys[K_a]:  # Move LEFT
            MOVEMENT_VECTOR[X_INDEX] += STEP_SIZE
        elif keys[K_d]:  # Move RIGHT
            MOVEMENT_VECTOR[X_INDEX] -= STEP_SIZE
        if keys[K_w]:  # Move FORWARD
            MOVEMENT_VECTOR[Y_INDEX] += STEP_SIZE
        elif keys[K_s]:  # Move BACK
            MOVEMENT_VECTOR[Y_INDEX] -= STEP_SIZE
        if keys[K_z]:  # Move UP
            MOVEMENT_VECTOR[Z_INDEX] += STEP_SIZE
        elif keys[K_x]:  # Move DOWN
            MOVEMENT_VECTOR[Z_INDEX] -= STEP_SIZE
        if keys[K_1]:  # Turning LED on and off
            TOGGLE_LED = not TOGGLE_LED

        if PREV_MOVEMENT_VECTOR != MOVEMENT_VECTOR:
            print(PREV_MOVEMENT_VECTOR, MOVEMENT_VECTOR)
            # clear_commands_queue()


    # Exit
    if keys[K_q]:
        break
    if keys[K_ESCAPE]:
        response = printer_ser.write("~\n".encode())
        print(response)

    # Apply movement
    if MOVEMENT_VECTOR[X_INDEX] or MOVEMENT_VECTOR[Y_INDEX] or MOVEMENT_VECTOR[Z_INDEX] or TOGGLE_LED is True:

        # Apply axis changes
        apply_movement()
        # Toggle led state
        if TOGGLE_LED:
            apply_led_toggle()
            TOGGLE_LED = False
        # Set Feed rate
        set_feed_rate(FEED_RATE)
        send_move()
        # Reset values
        PREV_MOVEMENT_VECTOR[X_INDEX] = MOVEMENT_VECTOR[X_INDEX]
        PREV_MOVEMENT_VECTOR[Y_INDEX] = MOVEMENT_VECTOR[Y_INDEX]
        PREV_MOVEMENT_VECTOR[Z_INDEX] = MOVEMENT_VECTOR[Z_INDEX]
        MOVEMENT_VECTOR = [0, 0, 0]
        joystick_idle = True



    # Based on the recommended implementation of jog mode:
    # https://github.com/gnea/grbl/blob/master/doc/markdown/jogging.md
    # while joystick is in use -> send commands to the buffer, elsewhere -> clear the commands buffer
    # to reach minimal latency.
    elif joystick_idle:
        PREV_MOVEMENT_VECTOR = [0, 0, 0]
        joystick_idle = False
        time.sleep(0.01)
        clear_commands_queue()
        print_full_response()

    # Delay for button press
    # time.sleep(BUTTON_DELAY)
    pygame.event.pump()
# Close the serial connection
printer_ser.close()

# $X

"""
Computing the axis step, acceleration and velocity


"""






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