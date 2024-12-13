
FUNCTION_BLOCK LED_Control
VAR_INPUT
    PB1 : BOOL;  (* Push Button 1 *)
    PB2 : BOOL;  (* Push Button 2 *)
END_VAR

VAR_OUTPUT
    LED : BOOL;  (* LED output *)
END_VAR

(* Implementing the logic for LED control based on PB1 and PB2 *)
LED := PB1 AND NOT PB2;

END_FUNCTION_BLOCK
