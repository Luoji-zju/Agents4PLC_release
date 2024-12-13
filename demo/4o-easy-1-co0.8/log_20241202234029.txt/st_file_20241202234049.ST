
FUNCTION_BLOCK FB_LoopCounter
VAR_INPUT
    i : BOOL; (* Trigger input *)
END_VAR

VAR
    macro : INT := 1; (* Starts from 1 to ensure positivity *)
    micro : INT := 1; (* Initial value same as macro for proper reset logic *)
END_VAR

VAR_OUTPUT
    o : INT; (* Output variable showing incremented values of macro *)
END_VAR

(* Counter logic implementation *)
IF i THEN
    micro := micro - 1;
    IF micro <= 0 THEN
        macro := macro + 1;
        micro := macro; (* Reset micro to the new macro value *)
    END_IF;
END_IF;

o := macro; (* Assign the current value of macro to output *)

END_FUNCTION_BLOCK
