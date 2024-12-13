
FUNCTION_BLOCK FB_StartStopMonitor
VAR_INPUT
    Start_Stop : BOOL;  // Input signal to monitor
    ON_OFF : BOOL;      // Current state of the output
END_VAR

VAR_OUTPUT
    ONS_Trig : BOOL;    // Rising edge trigger output
END_VAR

VAR
    Prev_State : BOOL;  // Previous state of the Start_Stop input
END_VAR

(* Main logic for rising edge detection *)
Prev_State := Start_Stop;  // Store the previous state
Rising_ONS := Start_Stop;   // Current state of Start_Stop
ONS_Trig := NOT Prev_State AND Rising_ONS;  // Detect rising edge

(* Update ON_OFF state based on the rising edge trigger *)
IF ONS_Trig THEN
    ON_OFF := NOT ON_OFF;  // Toggle ON_OFF state
END_IF

END_FUNCTION_BLOCK

(* Testing the function block in a main program *)
PROGRAM prg
VAR
    fb : FB_StartStopMonitor;  // Instance of the function block
    Start_Stop_Input : BOOL;   // Input for Start_Stop
    ON_OFF_State : BOOL;        // Output state
END_VAR

(* Example usage *)
Start_Stop_Input := TRUE;  // Simulate input
fb(Start_Stop := Start_Stop_Input, ON_OFF := ON_OFF_State);
(* After execution, fb.ONS_Trig and fb.ON_OFF will reflect the updated states *)

END_PROGRAM
