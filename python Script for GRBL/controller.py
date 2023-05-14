
""" Based on the current installation logic"""
import serial
import time
import pygame
from pygame.locals import *
import UIcontroller as uic

QUIT_GAME = False
PRINT_MODE = False
IS_JOYSTICK_IDLE = False
CURRENT_LINE_RESULT = "ok"

PENDING_TIME = 60
LAST_TIME_STAMP = 0
FILES_PATHS = ["drawings/spiral.gcode", "drawings/square.gcode", "drawings/two spirals.gcode"]
FILES_DISPLAY_MSG = ["ספירלה", "ריבוע", "שתי ספירלות"]
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
MOVEMENT_VECTOR = [0, 0, 0, 0]
LED_PREV_STATE = 0
X_INDEX = 0
Y_INDEX = 1
Z_INDEX = 2
LED_INDEX = 3


# UI msg
PRINTING_MSG ="מדפיס כעת..."
INSTRUCTIONS_MSG = "השתמשו בלחצנים להזזת המנורה"
PLEASE_WAIT_MSG = "אנא המתן..."
WELCOME = "ברוכים הבאים!"
MOVE_MSG = "זוז!"
END_PRINTING_MSG = "מסיים הדפסה"
AUTO_HOMING_MSG = "המערכת מבצעת כיול"
CURRENT_FILE_MSG = ""


def get_arrow_symbol():
    global MOVEMENT_VECTOR
    symbol = ""
    if MOVEMENT_VECTOR[X_INDEX] and MOVEMENT_VECTOR[Y_INDEX]:
        if X_INDEX > 0 and Y_INDEX > 0:
            symbol = "↖"
        elif X_INDEX > 0 and Y_INDEX < 0:
            symbol = "↙"
        elif X_INDEX < 0 and Y_INDEX > 0:
            symbol = "↗"
        elif X_INDEX < 0 and Y_INDEX < 0:
            symbol = "↘"

    elif MOVEMENT_VECTOR[X_INDEX]:
        if X_INDEX > 0:
            # symbol = "←"
            symbol = chr(33)
        else:
            # symbol = "→"
            symbol = chr(34)
    elif MOVEMENT_VECTOR[Y_INDEX]:
        if Y_INDEX > 0:
            symbol = "↑"
        else:
            symbol = "↓"

    return symbol


def auto_home(grbl_ser):
    time.sleep(2)
    t0 = time.time()
    response = grbl_ser.write("$H\n".encode())  # AutoHome
    print(response)
    response = grbl_ser.write("G10 P0 L20 X0 Y0 Z0\n".encode())
    print(response)
    response = grbl_ser.write(("G1 F600 M3 s" + str(LED_POWER) + "\n").encode())
    print(response)
    response = grbl_ser.write("G1 M3 s0\n".encode())
    print(response)

    response = grbl_ser.write("?\n".encode())

    while str(response).isdigit() or "ok" not in response:
        response = grbl_ser.readline().decode()
        print(response)

    print_full_response(grbl_ser)
    t1 = time.time()
    print("Auto-homing time: " + str(t1 - t0))


def print_full_response(grbl_ser):
    response = grbl_ser.readlines()
    for l in response:
        print(l.decode().strip())


def get_state(grbl_ser):
    response = grbl_ser.write("?\n".encode())
    line = grbl_ser.readline().decode()

    while line == "ok\r\n" or line.isdigit():
        line = grbl_ser.readline().decode()
    state = line.split("|")[0]

    return state[1:]


def listen_to_movement_keys(keys):
    global LED_PREV_STATE

    # listen to Movement keys1
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
        MOVEMENT_VECTOR[LED_INDEX] = LED_POWER
    else:
        MOVEMENT_VECTOR[LED_INDEX] = 0


def listen_to_print_buttons(keys):
    global CURRENT_FILE_PATH
    global CURRENT_FILE_MSG
    if keys[K_i]:
        CURRENT_FILE_PATH = "drawings/spiral.gcode"
        CURRENT_FILE_MSG = "ספירלה"
    elif keys[K_o]:
        CURRENT_FILE_PATH = "drawings/square.gcode"
        CURRENT_FILE_MSG = "ריבוע"
    elif keys[K_p]:
        CURRENT_FILE_PATH = "drawings/two spirals.gcode"
        CURRENT_FILE_MSG = " שתי ספירלה"


def listen_to_sys_keys(keys, grbl_ser, ui_controller):
    global PRINT_MODE
    global QUIT_GAME
    last_time_stamp = time.time()
    if keys[K_0]:
        ui_controller.set_header(AUTO_HOMING_MSG)
        ui_controller.set_instruction(PLEASE_WAIT_MSG)
        pygame.display.update()
        auto_home(grbl_ser)
        last_time_stamp += 15
    if keys[K_l]:
        pass
    if keys[K_q]:
        if PRINT_MODE:
            print("stopped in the middle!")
            exit_print_mode()
        QUIT_GAME = True
    return last_time_stamp


def apply_movement():
    global MOVEMENT_VECTOR
    global GC_MOVE_COMMAND
    GC_MOVE_COMMAND += " X" + str(MOVEMENT_VECTOR[X_INDEX])
    GC_MOVE_COMMAND += " Y" + str(MOVEMENT_VECTOR[Y_INDEX])
    GC_MOVE_COMMAND += " Z" + str(MOVEMENT_VECTOR[Z_INDEX])
    GC_MOVE_COMMAND += " M3 S" + str(MOVEMENT_VECTOR[LED_INDEX])


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


def send_move(grbl_ser):
    global GC_MOVE_COMMAND
    grbl_ser.write(GC_MOVE_COMMAND.encode())
    response = grbl_ser.readline().decode()
    # print(response)


def reset_command_values():
    global MOVEMENT_VECTOR
    global GC_MOVE_COMMAND
    global IS_JOYSTICK_IDLE
    global LED_PREV_STATE
    GC_MOVE_COMMAND = "$J=G91 "
    LED_PREV_STATE = MOVEMENT_VECTOR[LED_INDEX]
    # print("reset values!")
    MOVEMENT_VECTOR = [0, 0, 0, 0]
    IS_JOYSTICK_IDLE = True


def clear_commands_queue(grbl_ser):
    grbl_ser.flushInput()
    grbl_ser.flushOutput()
    res = grbl_ser.write('\x85\r\n'.encode())
    # time.sleep(1)
    print("Cleared Jog Buffer ! \n")
    print(res)


def exit_print_mode():
    global CURRENT_FILE_PATH
    global PRINT_MODE
    global FILE_TO_PRINT
    global CURRENT_LINE_RESULT
    # clear the current file, exit print mode
    PRINT_MODE = False
    CURRENT_FILE_PATH = ""
    CURRENT_LINE_RESULT = "ok"
    FILE_TO_PRINT.close()
    FILE_TO_PRINT = None
    print("-- finished printing file: " + CURRENT_FILE_PATH)


def print_current_file(grbl_ser):
    global CURRENT_FILE_PATH
    global PRINT_MODE
    global FILE_TO_PRINT
    global CURRENT_LINE_RESULT

    if not PRINT_MODE:
        # auto_home(grbl_ser)
        # time.sleep(0.5)
        PRINT_MODE = True
        FILE_TO_PRINT = open(CURRENT_FILE_PATH, 'r')
        print("-- starts printing file: " + CURRENT_FILE_PATH)

    line = FILE_TO_PRINT.readline()
    if not line and get_state(grbl_ser) == "Idle":
        # clear the current file, exit print mode
        exit_print_mode()
    else:
        time.sleep(1)
        print(line.strip())
        grbl_ser.write(line.encode())
        CURRENT_LINE_RESULT = grbl_ser.readline()
        CURRENT_LINE_RESULT = CURRENT_LINE_RESULT.decode()
        CURRENT_LINE_RESULT = CURRENT_LINE_RESULT.strip()
        # print("current line return: " + str(CURRENT_LINE_RESULT))

    # print(get_state(grbl_ser) == "Idle", get_state(grbl_ser))
    # print("current line read: " + str(CURRENT_LINE_RESULT))


def set_screen(ui_controller):
    ui_controller.set_bg_color()
    ui_controller.draw_frame_rectangle()
    # ui_controller.set_header(WELCOME)
    # ui_controller.set_instruction(INSTRUCTIONS_MSG)


def run_game(ui_controller, grbl_ser):
    global PRINT_MODE
    global LED_PREV_STATE
    global FILES_DISPLAY_MSG
    global CURRENT_FILE_MSG
    global CURRENT_FILE_PATH
    global CURRENT_FILE_PATH_INDEX
    global QUIT_GAME

    # LED_PREV_STATE = False
    last_time_stamp = time.time()

    while not QUIT_GAME:

        # ui_controller.draw_animation()
        keys = pygame.key.get_pressed()

        if keys[K_c]:
            ui_controller.clean_text()

        last_time_stamp = listen_to_sys_keys(keys, grbl_ser, ui_controller)  # Listen to system keys (i.e. quit, etc..)
        if not CURRENT_FILE_PATH:           # Listen to print keys
            listen_to_print_buttons(keys)
        listen_to_movement_keys(keys)       # Listen to movement keys

        # Apply movement - in case there was a change
        if MOVEMENT_VECTOR[X_INDEX] or MOVEMENT_VECTOR[Y_INDEX] or MOVEMENT_VECTOR[Z_INDEX] or MOVEMENT_VECTOR[LED_INDEX]!= LED_PREV_STATE:
            # print(MOVEMENT_VECTOR)
            last_time_stamp = time.time()
            if PRINT_MODE:
                ui_controller.clean_text()
                ui_controller.set_header(END_PRINTING_MSG)
                ui_controller.set_instruction("הלחצנים כבר יהיו זמינים")
                pygame.display.update()
                exit_print_mode()
            elif not PRINT_MODE and get_state(grbl_ser) == "Run":
                ui_controller.set_instruction(uic.CLEAN_MSG)
                ui_controller.set_instruction("הלחצנים כבר יהיו זמינים")
                pygame.display.update()

            else:
                apply_movement()        # Apply movement
                ui_controller.set_instruction(uic.CLEAN_MSG)
                ui_controller.set_instruction(get_arrow_symbol(), font_size=36, font_file_path="C:\Windows\Fonts\WINGDNG3.TTF")
                if MOVEMENT_VECTOR[LED_INDEX] != LED_PREV_STATE:          # Apply led changes
                    # apply_led_toggle()
                    ui_controller.set_instruction(uic.CLEAN_MSG)
                    if MOVEMENT_VECTOR[LED_INDEX] and not LED_PREV_STATE:
                        ui_controller.set_instruction("הדלקת נורה!")
                    elif not MOVEMENT_VECTOR[LED_INDEX] and LED_PREV_STATE:
                        ui_controller.set_instruction("כיבית נורה!")
                    # LED_PREV_STATE = False
                set_feed_rate()         # Apply feed rate
                send_move(grbl_ser)             # Send GCODE command
                pygame.display.update()

            reset_command_values()  # reset G-code values for the next command


        # clear the command buffer when joystick is idle (only once)
        elif IS_JOYSTICK_IDLE:
            global IS_JOYSTICK_IDLE
            IS_JOYSTICK_IDLE = False
            # if not MOVEMENT_VECTOR[LED_INDEX] and LED_PREV_STATE:
            #     apply_movement()
            #     print("turning off")
            # clear_commands_queue(grbl_ser)

        elif CURRENT_FILE_PATH:  # user or system chose file to print
            if not PRINT_MODE:
                ui_controller.clean_text()
                ui_controller.set_header("מדפיס כעת " + CURRENT_FILE_MSG)
                pygame.display.update()
            else:
                ui_controller.set_instruction(uic.CLEAN_MSG)
                ui_controller.set_instruction(PRINTING_MSG)
                pygame.display.update()

            # time.sleep(0.5)
            print_current_file(grbl_ser)  # entered print mode
            last_time_stamp = time.time()

        if keys[K_i] or keys[K_o] or keys[K_p] and CURRENT_FILE_PATH:
            print("Currently printing please wait!")
            ui_controller.set_instruction(uic.CLEAN_MSG)
            ui_controller.set_instruction("נבחר כבר קובץ")
            pygame.display.update()
            time.sleep(1)

        if time.time() - last_time_stamp > PENDING_TIME and not PRINT_MODE:
            ui_controller.set_instruction(uic.CLEAN_MSG)
            pygame.display.update()
            ui_controller.set_instruction("עבר הזמן!")
            pygame.display.update()
            print("Time is up!")
            CURRENT_FILE_PATH_INDEX += 1
            CURRENT_FILE_PATH = FILES_PATHS[CURRENT_FILE_PATH_INDEX % len(FILES_PATHS)]
            CURRENT_FILE_MSG = FILES_DISPLAY_MSG[CURRENT_FILE_PATH_INDEX % len(FILES_DISPLAY_MSG)]
            ui_controller.clean_text()
            ui_controller.set_header("מדפיס כעת " + CURRENT_FILE_MSG)
            pygame.display.update()

            print_current_file(grbl_ser)  # entered print mode

        if not CURRENT_FILE_PATH and not IS_JOYSTICK_IDLE:  # clear msg after 1 second
            if (time.time() - last_time_stamp) > 1.5:
                ui_controller.set_instruction(uic.CLEAN_MSG)
                if get_state(grbl_ser) == "Idle":
                    ui_controller.clean_text()
                    ui_controller.set_header(WELCOME)
                pygame.display.update()

        pygame.event.pump()

    pygame.quit()

# -------------------------------------------------------


def main():
    # init serial connection
    grbl_ser = serial.Serial('COM5', baudrate=115200, timeout=1)
    # init pygame  main screen
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    ui_controller = uic.UiProperties(screen)
    # auto home
    set_screen(ui_controller)

    # Auto homing
    ui_controller.set_header(AUTO_HOMING_MSG)
    ui_controller.set_instruction(PLEASE_WAIT_MSG)
    pygame.display.update()
    auto_home(grbl_ser)

    # Welcome page
    ui_controller.clean_text()
    ui_controller.set_header(WELCOME)
    ui_controller.set_instruction(INSTRUCTIONS_MSG)
    pygame.display.update()

    run_game(ui_controller, grbl_ser)


main()

