
FUNCTION_BLOCK FB_CompareAndSet
VAR_INPUT
    x : INT;
    y : INT;
END_VAR

VAR_OUTPUT
    Counter : INT;
END_VAR

VAR
    InternalCounter : INT := 0;
END_VAR

(* Function block logic starts here *)

IF x < y THEN
    x := y;
ELSE
    y := x;
END_IF;

(* Increment the execution counter *)
InternalCounter := InternalCounter + 1;
Counter := InternalCounter;

END_FUNCTION_BLOCK
