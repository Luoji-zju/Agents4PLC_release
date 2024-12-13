
FUNCTION_BLOCK FB_ValueTracker
VAR_INPUT
    aaa : DINT;
    bbb : DINT;
END_VAR

VAR_OUTPUT
    OUT : DINT;
    UPDATED_CYCLE : DINT;
END_VAR

VAR
    CYCLE : DINT := 0;
END_VAR

(* Increment logic based on the comparison of aaa and bbb *)
IF aaa = bbb THEN
    aaa := aaa + 1;
ELSIF aaa > bbb THEN
    bbb := bbb + 1;
ELSE
    aaa := aaa + 1;
END_IF;

(* Calculate the difference between aaa and bbb *)
OUT := aaa - bbb;

(* Increment the cycle count *)
CYCLE := CYCLE + 1;
UPDATED_CYCLE := CYCLE;

END_FUNCTION_BLOCK
