import serial
import time
import pygame
from pygame.locals import *


# Constant variables:
FEED_RATE = 1200  # STEP = ~(FEED_RATE // 600)  # https://github.com/gnea/grbl/issues/837
STEP_SIZE = 0.5  # step size will change the DUP bug for some reason
LED_POWER = 1000
JOG_COMMAND_PREFIX_LEN = 7
GC_MOVE_COMMAND = "$J=G91 "
BUTTON_DELAY = 0.01
X_INDEX = 0
Y_INDEX = 1
Z_INDEX = 2
TOGGLE_LED_INDEX = 3  # set to 1 when need to be toggled
PENDING_TIME = 120  # in seconds


def auto_home(printer_ser):
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


def print_full_response(printer_ser):
    response = printer_ser.readlines()
    for l in response:
        print(l.decode().strip())


def print_status(printer_ser):
    printer_ser.write("?\n".encode())
    print_full_response(printer_ser)


def main():
    # Open a serial connection to the machine
    printer_ser = serial.Serial('COM5', baudrate=115200, timeout=1)

    # Init UI screen
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    # clock = pygame.time.Clock()

    # init system
    # print_file('initialize.gcode', 0.5)
    # printer_ser.flushInput()
    auto_home(printer_ser)
    print_menu()
    run(printer_ser, screen)


def get_pressed_keys(keys, movement_vector):
    """ Making action """
    global X_INDEX
    global Y_INDEX
    global Z_INDEX
    global TOGGLE_LED_INDEX
    global STEP_SIZE

    if keys[K_a]:  # Move LEFT
        movement_vector[X_INDEX] += STEP_SIZE
    elif keys[K_d]:  # Move RIGHT
        movement_vector[X_INDEX] -= STEP_SIZE
    if keys[K_w]:  # Move FORWARD
        movement_vector[Y_INDEX] += STEP_SIZE
    elif keys[K_s]:  # Move BACK
        movement_vector[Y_INDEX] -= STEP_SIZE
    if keys[K_z]:  # Move UP
        movement_vector[Z_INDEX] += STEP_SIZE
    elif keys[K_x]:  # Move DOWN
        movement_vector[Z_INDEX] -= STEP_SIZE
    if keys[K_1]:  # Turning LED on and off
        movement_vector[TOGGLE_LED_INDEX] = int(not movement_vector[TOGGLE_LED_INDEX])


def apply_movement(movement_vector):
    global GC_MOVE_COMMAND
    global LED_POWER

    gcode_command = GC_MOVE_COMMAND
    gcode_command += " X" + str(movement_vector[X_INDEX])
    gcode_command += " Y" + str(movement_vector[Y_INDEX])
    gcode_command += " Z" + str(movement_vector[Z_INDEX])
    gcode_command += " Z" + str(movement_vector[Z_INDEX])

    return gcode_command


def apply_led_toggle(gcode_command, led_mode):
    global LED_POWER
    led_mode = not led_mode
    if led_mode:
        gcode_command += " M3 S" + str(LED_POWER)
    else:
        gcode_command += " M3 S0"
    return gcode_command, led_mode


def set_feed_rate(gcode_command):
    gcode_command += " F" + str(FEED_RATE) + "\n"
    return gcode_command


def send_move(printer_ser, gcode_command):
    printer_ser.write(gcode_command.encode())
    response = printer_ser.readline().decode()
    return response


def print_file(printer_ser, file_name, delay_rate=1.5):

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
                print("ALARM:1 - error has occurred!")
                break

    t1 = time.time()
    print("printing time: " + str(t1-t0))
    time.sleep(4)


def run(printer_ser,screen):
    quit_app = False
    is_print_mode = False
    joystick_idle = False
    last_response = "ok"
    movement_vector = [0, 0, 0, 0]
    prev_movement_vector = [0, 0, 0, 0]
    led_mode = False
    timer = time.time()

    while not quit_app:
        global timer
        global prev_movement_vector
        global is_print_mode
        global joystick_idle

        keys = pygame.key.get_pressed()
        get_pressed_keys(keys, movement_vector)

        # SPECIAL CASES
        if keys[K_0]:
            response = printer_ser.write("$H\n".encode())
            print(response)
            response = printer_ser.write("G10 P0 L20 X0 Y0 Z0\n".encode())
            print(response)

        if keys[K_l]:
            print_status(printer_ser)

        if keys[K_q]:
            quit_app = True

        # APPLY MOVEMENT, VERIFY BUFFER IS NOT FULL
        if(movement_vector[X_INDEX]
                or movement_vector[Y_INDEX]
                or movement_vector[Z_INDEX]
                or movement_vector[TOGGLE_LED_INDEX]
                and "ok" in last_response):
            gcode_command = apply_movement(movement_vector)
            gcode_command, led_mode = apply_led_toggle(gcode_command, led_mode)
            gcode_command = set_feed_rate(gcode_command)
            last_response = send_move(printer_ser, gcode_command)
            prev_movement_vector = movement_vector
            joystick_idle = True
            timer = time.time()

        # IDLE - PRINT FILE
        elif abs(time.time() - timer) > PENDING_TIME:
            # BLOCKING the main loop
            print_file(printer_ser,"spiral.gcode", 4)
            time.sleep(10)
            timer = time.time()

        elif joystick_idle:
            prev_movement_vector = [0, 0, 0]
            joystick_idle = False
            time.sleep(0.01)
            clear_commands_queue()
            print_full_response()


main()
"""
        # any key was pressed?
            # is it in printing mode?
                # yes:
                    # display alarm
                # no:
                    # update movement vector
                    # set print mode to off
                    # apply movement
                # set timer to 0
        # timer is larger than X
            # enter print mode
            # print
            # exit print mode
"""












