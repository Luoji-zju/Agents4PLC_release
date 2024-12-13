

FUNCTION_BLOCK FB_MonitorStartStop
VAR_INPUT
    Start_Stop : BOOL;
END_VAR

VAR_OUTPUT
    ONS_Trig : BOOL;
    ON_OFF : BOOL;
    Rising_ONS : BOOL;
END_VAR

VAR
    Prev_Start_Stop : BOOL := FALSE;  (* Internal variable to hold the previous state of Start_Stop *)
END_VAR

(* Detecting the rising edge of Start_Stop signal *)
ONS_Trig := (Start_Stop AND NOT Prev_Start_Stop);

(* Update ON_OFF based on XOR operation with ONS_Trig *)
ON_OFF := ONS_Trig XOR ON_OFF;

(* Store the current state of Start_Stop for the next cycle *)
Rising_ONS := Start_Stop;
Prev_Start_Stop := Start_Stop;

END_FUNCTION_BLOCK

