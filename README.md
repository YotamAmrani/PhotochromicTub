# PhotochromicTub
### An interactive project made for the Science museum of Jerusalem

The Photochromic tub is an interactive project,
consist of a large 'Aquarium', filled with special photochromic solution
and a 3D printer.
A visitor may choose to control the system directly via the joystick interface, or 
print Pre-prepared 3D drawings via designated push buttons.

The project includes of 3 main parts:
- The 3D printer (GRBL and motors).
- The controller main script.
- The joystick interface.

![image (67)](https://user-images.githubusercontent.com/87602958/234101972-fd9d5222-ab68-4cd0-b064-b95256ab0135.png)


### The 3D printer
The printer consist of the following components:
- Arduino nano.
- Arduino CNC shield.
- a4988 stepper motor driver (one for each axis).
- Nema17 stepper motors (one for each axis) with matching rails.
- UV Led (connecte to the PWM spindle port).
- 3 limit switches

The Arduino is running the GRBL Library (https://github.com/cprezzi/grbl-servo)
with the following minor changes:
- Enabling M3 and S G-CODE commands in JOG mode (in order to support the spindle, i.e. the LED, while moving)
- Adjusting the PWM frequency to match the UV LED (under the config file, edit the SPINDLE_IS_SERVO and SPINDLE_PWM_MIN_VALUE macros)
After running the system GRBL settings were adjusted to atch the motors (acceleration, max feed rate,step per mm etc.. )
(Modified version is under the GRBL folder)

### The controller main script
The controller script is a python script running over a PC.
the script is responsible for the following parts:
- Receiving input events from the joystick interface.
- Interpret the events into G-CODE commands, and them via serial port to the 3D printer.
- In case that the system enters IDLE mode, a custom G-CODE file will be printed.
- Display GUI to the screen according to current system states (using pygame lib).
(Script can be found uner the 'python Script for GRBL' folder)

### The joystick interface
The joystick interface is a simple interface consist of the following components:
- Arduino pro micro (in order to emulate a keyboard).
- arcade joystick (4 push buttons inputs, one per axis).
- Push buttons (LED control, and printing pre-configured G-CODE files).
(Arduino code can be found uner the 'keyboard_simulator_digital_write' folder)






