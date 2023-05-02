
""" Based on the current installation logic"""

import time
import pygame
from pygame.locals import *
import UIcontroller as uic

QUIT_GAME = False
PRINT_MODE = False
IS_JOYSTICK_IDLE = False

PENDING_TIME = 10
LAST_TIME_STAMP = 0
FILES_PATHS = ["spiral.gcode", "square.gcode", "two spirals.gcode"]
CURRENT_FILE_PATH_INDEX = 0
CURRENT_FILE_PATH = ""
FILE_TO_PRINT = None

STEP_SIZE = 0.3
LED_MODE = False
LED_POWER = 1000
FEED_RATE = 1800

# Movement vector
JOG_COMMAND_PREFIX_LEN = 7
GC_MOVE_COMMAND = "$J=G91 "
MOVEMENT_VECTOR = [0, 0, 0]
TOGGLE_LED = False
X_INDEX = 0
Y_INDEX = 1
Z_INDEX = 2


# UI msg
PRINTING_MSG ="מדפיס כעת..."
INSTRUCTIONS_MSG = "השתמשו בלחצנים להזזת המנורה"
PLEASE_WAIT = "אנא המתן"
WELCOME = "ברוכים הבאים!"
MOVE_MSG = "זוז!"
END_PRINTING_MSG = "מסיים הדפסה"


def auto_home():
    print("currently autohoming")
    time.sleep(1)
    print("finished autohoming")


def listen_to_movement_keys(keys):
    global TOGGLE_LED

    # listen to Movement keys
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


def listen_to_print_buttons(keys):
    global CURRENT_FILE_PATH
    if keys[K_i]:
        CURRENT_FILE_PATH = "spiral.gcode"
    elif keys[K_o]:
        CURRENT_FILE_PATH = "square.gcode"
    elif keys[K_p]:
        CURRENT_FILE_PATH = "two spirals.gcode"


def listen_to_sys_keys(keys):
    global PRINT_MODE
    global QUIT_GAME
    if keys[K_0]:
        auto_home()
    if keys[K_l]:
        pass
    if keys[K_q]:
        if PRINT_MODE:
            print("stopped in the middle!")
            exit_print_mode()
        QUIT_GAME = True


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
    time.sleep(0.2)


def set_feed_rate():
    global GC_MOVE_COMMAND
    GC_MOVE_COMMAND += " F" + str(FEED_RATE) + "\n"


def send_move():
    global GC_MOVE_COMMAND
    # printer_ser.write(GC_MOVE_COMMAND.encode())
    # response = printer_ser.readline().decode()
    print(GC_MOVE_COMMAND)


def reset_command_values():
    global MOVEMENT_VECTOR
    global IS_JOYSTICK_IDLE
    MOVEMENT_VECTOR = [0, 0, 0]
    IS_JOYSTICK_IDLE = True


def clear_commands_queue():
    # printer_ser.flushInput()
    # printer_ser.flushOutput()
    # res = printer_ser.write('\x85\r\n'.encode())
    # time.sleep(1)
    print("Cleared Jog Buffer ! \n")


def exit_print_mode():
    global CURRENT_FILE_PATH
    global PRINT_MODE
    global FILE_TO_PRINT
    # clear the current file, exit print mode
    PRINT_MODE = False
    CURRENT_FILE_PATH = ""
    FILE_TO_PRINT.close()
    FILE_TO_PRINT = None
    print("-- finished printing file: " + CURRENT_FILE_PATH)


def print_current_file():
    global CURRENT_FILE_PATH
    global PRINT_MODE
    global FILE_TO_PRINT

    if not PRINT_MODE:
        auto_home()
        # time.sleep(0.5)
        PRINT_MODE = True
        FILE_TO_PRINT = open(CURRENT_FILE_PATH, 'r')
        print("-- starts printing file: " + CURRENT_FILE_PATH)

    line = FILE_TO_PRINT.readline()
    if not line:
        # clear the current file, exit print mode
        exit_print_mode()
    else:
        time.sleep(0.5)
        print(line.strip())


def set_screen(ui_controller):
    ui_controller.set_bg_color()
    ui_controller.draw_frame_rectangle()
    ui_controller.set_header(WELCOME)
    ui_controller.set_instruction(INSTRUCTIONS_MSG)


def run_game(ui_controller):
    global PRINT_MODE
    global TOGGLE_LED
    global CURRENT_FILE_PATH
    global CURRENT_FILE_PATH_INDEX
    global QUIT_GAME

    TOGGLE_LED = False
    set_screen(ui_controller)
    last_time_stamp = time.time()

    while not QUIT_GAME:

        # ui_controller.draw_animation()
        keys = pygame.key.get_pressed()

        if keys[K_c]:
            ui_controller.clean_text()

        listen_to_sys_keys(keys)            # Listen to system keys (i.e. quit, etc..)
        if not CURRENT_FILE_PATH:           # Listen to print keys
            listen_to_print_buttons(keys)
        listen_to_movement_keys(keys)       # Listen to movement keys

        # Apply movement - in case there was a change
        if MOVEMENT_VECTOR[X_INDEX] or MOVEMENT_VECTOR[Y_INDEX] or MOVEMENT_VECTOR[Z_INDEX] or TOGGLE_LED is True:
            last_time_stamp = time.time()
            time.sleep(0.3)  # TODO: to remove!
            if PRINT_MODE:
                ui_controller.set_instruction(uic.CLEAN_MSG)
                ui_controller.set_instruction(END_PRINTING_MSG)
                pygame.display.update()
                time.sleep(0.3)  # TODO: to remove!
                exit_print_mode()
            else:
                apply_movement()        # Apply movement
                ui_controller.set_instruction(uic.CLEAN_MSG)
                pygame.display.update()
                ui_controller.set_instruction(MOVE_MSG)
                if TOGGLE_LED:          # Apply led changes
                    apply_led_toggle()
                    TOGGLE_LED = False
                set_feed_rate()         # Apply feed rate
                send_move()             # Send GCODE command
                reset_command_values()  # reset G-code values for the next command

        # clear the command buffer when joystick is idle (only once)
        elif IS_JOYSTICK_IDLE:
            global IS_JOYSTICK_IDLE
            IS_JOYSTICK_IDLE = False
            time.sleep(0.01)
            clear_commands_queue()

        elif CURRENT_FILE_PATH:
            if not PRINT_MODE:
                ui_controller.set_instruction(uic.CLEAN_MSG)
                ui_controller.set_instruction("קובץ נבחר..")
                pygame.display.update()
                time.sleep(0.2)  # TODO: to remove!
            else:
                ui_controller.set_instruction(uic.CLEAN_MSG)
                ui_controller.set_instruction(PRINTING_MSG)
            # time.sleep(0.5)
            print_current_file()  # entered print mode
            last_time_stamp = time.time()

        if keys[K_i] or keys[K_o] or keys[K_p] and CURRENT_FILE_PATH:
            print("Currently printing please wait!")
            ui_controller.set_instruction(uic.CLEAN_MSG)
            ui_controller.set_instruction(PLEASE_WAIT)

        if time.time() - last_time_stamp > PENDING_TIME and not PRINT_MODE:
            ui_controller.set_instruction(uic.CLEAN_MSG)
            ui_controller.set_instruction("עבר הזמן!")
            CURRENT_FILE_PATH_INDEX += 1
            CURRENT_FILE_PATH = FILES_PATHS[CURRENT_FILE_PATH_INDEX % len(FILES_PATHS)]
            print_current_file()  # entered print mode

        if not CURRENT_FILE_PATH and not IS_JOYSTICK_IDLE:  # clear msg after 1 second
            if time.time() - last_time_stamp > 0.5:
                ui_controller.set_instruction(uic.CLEAN_MSG)

        pygame.display.update()
        pygame.event.pump()

    pygame.quit()

# -------------------------------------------------------

def main():
    # init serial connection
    # printer_ser = serial.Serial('COM5', baudrate=115200, timeout=1)
    # init pygame  main screen
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    ui_controller = uic.UiProperties(screen)
    # auto home
    auto_home()
    run_game(ui_controller)


main()

