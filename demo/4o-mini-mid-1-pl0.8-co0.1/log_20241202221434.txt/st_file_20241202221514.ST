
FUNCTION_BLOCK FB_StartStopMonitor
VAR_INPUT
    Start_Stop : BOOL;  // Input signal to monitor
    ON_OFF : BOOL;      // Current state of the output
END_VAR

VAR_OUTPUT
    ONS_Trig : BOOL;    // Rising edge trigger output
    Rising_ONS : BOOL;  // Store the current value of Start_Stop
END_VAR

VAR
    Prev_State : BOOL;  // Previous state of the Start_Stop input
END_VAR

(* Main logic for rising edge detection *)
Rising_ONS := Start_Stop;   // Store current value of Start_Stop
ONS_Trig := NOT Prev_State AND Rising_ONS;  // Detect rising edge
Prev_State := Start_Stop;  // Store the previous state

(* Update ON_OFF state based on the rising edge trigger *)
IF ONS_Trig THEN
    ON_OFF := NOT ON_OFF;  // Toggle ON_OFF state
END_IF

END_FUNCTION_BLOCK
