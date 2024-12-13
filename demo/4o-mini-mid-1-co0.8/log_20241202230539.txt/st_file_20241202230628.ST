
FUNCTION_BLOCK FB_MonitorStartStop
VAR_INPUT
    Start_Stop : BOOL;  (* Input signal indicating start/stop *)
END_VAR

VAR_OUTPUT
    ONS_Trig : BOOL;     (* Output indicating rising edge trigger *)
    Rising_ONS : BOOL;   (* Output reflecting the current state of Start_Stop *)
END_VAR

VAR
    Previous_Start_Stop : BOOL;  (* Variable to store the previous state of Start_Stop *)
END_VAR

(* Execution section of the function block *)
Rising_ONS := Start_Stop;  (* Update the current state *)
ONS_Trig := Start_Stop AND NOT Previous_Start_Stop;  (* Detect the rising edge *)
Previous_Start_Stop := Rising_ONS;  (* Store the current state for the next cycle *)

END_FUNCTION_BLOCK
