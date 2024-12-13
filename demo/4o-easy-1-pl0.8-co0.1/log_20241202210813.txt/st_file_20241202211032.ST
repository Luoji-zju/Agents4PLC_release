
FUNCTION_BLOCK FB_LoopCounter
VAR_INPUT
    i : BOOL; (* Input trigger to increment the counter *)
END_VAR

VAR_OUTPUT
    o : INT; (* Output representing the current macro value *)
END_VAR

VAR
    macro : INT := 1; (* Macro variable initialized to 1 *)
    micro : INT := 1; (* Micro variable initialized to 1 *)
END_VAR

(* Logic to handle the loop counter *)
IF i THEN
    IF micro = 0 THEN
        macro := macro + 1; (* Increment macro when micro reaches zero *)
        micro := macro;     (* Reset micro to the new value of macro *)
    END_IF;
    o := macro;             (* Assign the current macro value to output *)
    micro := micro - 1;     (* Decrement micro by 1 *)
END_IF;

END_FUNCTION_BLOCK
