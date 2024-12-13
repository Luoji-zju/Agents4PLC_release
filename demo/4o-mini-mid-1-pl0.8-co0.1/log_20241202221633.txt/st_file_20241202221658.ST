
FUNCTION_BLOCK LED_Motor_Controller
VAR_INPUT
    PI_Button_Left : BOOL;  // Input for left button
    PI_Button_Right : BOOL; // Input for right button
    E_Left : BOOL;          // Enable signal for left LED
    E_Right : BOOL;         // Enable signal for right LED
END_VAR

VAR_OUTPUT
    PI_LED_Red : BOOL;      // Output for red LED
    PI_LED_Green : BOOL;    // Output for green LED
    A_Motor_Left : BOOL;     // Output for left motor direction
    A_Motor_Right : BOOL;    // Output for right motor direction
END_VAR

(* Control LED states based on enable signals *)
PI_LED_Red := E_Left;                     // Turn on red LED if E_Left is TRUE
PI_LED_Green := E_Right;                   // Turn on green LED if E_Right is TRUE

(* Control motor direction based on button states *)
A_Motor_Left := NOT PI_Button_Left;        // Motor turns left when the left button is not pressed
A_Motor_Right := NOT PI_Button_Right;      // Motor turns right when the right button is not pressed

END_FUNCTION_BLOCK
