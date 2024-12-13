

FUNCTION_BLOCK FB_LED_Motor_Control
VAR_INPUT
    PI_Button_Left  : BOOL;  (* Input for the left button press *)
    PI_Button_Right : BOOL;  (* Input for the right button press *)
    E_Left          : BOOL;  (* Signal for activating the red LED *)
    E_Right         : BOOL;  (* Signal for activating the green LED *)
END_VAR

VAR_OUTPUT
    PI_LED_Red      : BOOL;  (* Output to control the red LED *)
    PI_LED_Green    : BOOL;  (* Output to control the green LED *)
    A_Motor_Left    : BOOL;  (* Output to run the motor left *)
    A_Motor_Right   : BOOL;  (* Output to run the motor right *)
END_VAR

(* Logic to control the LEDs *)
PI_LED_Red := E_Left;
PI_LED_Green := E_Right;

(* Logic to control the motor direction *)
IF NOT PI_Button_Left THEN
    A_Motor_Left := TRUE;
    A_Motor_Right := FALSE;
ELSE
    A_Motor_Left := FALSE;
END_IF;

IF NOT PI_Button_Right THEN
    A_Motor_Right := TRUE;
    A_Motor_Left := FALSE;
ELSE
    A_Motor_Right := FALSE;
END_IF;

END_FUNCTION_BLOCK

