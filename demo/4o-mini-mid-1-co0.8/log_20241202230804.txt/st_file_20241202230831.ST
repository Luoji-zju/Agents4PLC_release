
FUNCTION_BLOCK LED_Motor_Controller
VAR_INPUT
    PI_Button_Left : BOOL; 
    PI_Button_Right : BOOL; 
    E_Left : BOOL; 
    E_Right : BOOL; 
END_VAR_INPUT

VAR_OUTPUT
    PI_LED_Red : BOOL; 
    PI_LED_Green : BOOL; 
    A_Motor_Left : BOOL; 
    A_Motor_Right : BOOL; 
END_VAR_OUTPUT

(* Logic to control the LEDs and motor direction *)
(* Activate the red LED when E_Left is true and the green LED when E_Right is true *)
PI_LED_Red := E_Left;
PI_LED_Green := E_Right;

(* Control the motor direction based on button presses *)
A_Motor_Left := NOT PI_Button_Left;  (* Set motor left output to TRUE when left button is not pressed *)
A_Motor_Right := NOT PI_Button_Right; (* Set motor right output to TRUE when right button is not pressed *)

END_FUNCTION_BLOCK
