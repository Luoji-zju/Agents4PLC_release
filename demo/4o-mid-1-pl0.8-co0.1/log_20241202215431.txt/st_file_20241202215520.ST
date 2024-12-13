
FUNCTION_BLOCK LED_Motor_Controller
VAR_INPUT
    PI_Button_Left : BOOL;
    PI_Button_Right : BOOL;
    E_Left : BOOL;
    E_Right : BOOL;
END_VAR

VAR_OUTPUT
    PI_LED_Red : BOOL;
    PI_LED_Green : BOOL;
    A_Motor_Left : BOOL;
    A_Motor_Right : BOOL;
END_VAR

(* Control logic for LEDs *)
PI_LED_Red := E_Left AND PI_Button_Left;
PI_LED_Green := E_Right AND PI_Button_Right;

(* Control logic for motor direction *)
A_Motor_Left := NOT PI_Button_Left;
A_Motor_Right := NOT PI_Button_Right;

END_FUNCTION_BLOCK
