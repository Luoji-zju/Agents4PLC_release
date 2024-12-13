
FUNCTION_BLOCK FB_ValueTracker
VAR_INPUT
    aaa : INT; 
    bbb : INT; 
    CYCLE : INT; 
END_VAR

VAR_OUTPUT
    OUT : INT; 
    UPDATED_CYCLE : INT; 
END_VAR

(* Increment the cycle counter *)
CYCLE := CYCLE + 1;

(* Compare aaa and bbb, and increment accordingly *)
IF aaa = bbb THEN
    aaa := aaa + 1;
ELSIF aaa > bbb THEN
    bbb := bbb + 1;
ELSE
    aaa := aaa + 1;
END_IF;

(* Calculate the difference between aaa and bbb *)
OUT := aaa - bbb;

(* Update the output cycle counter *)
UPDATED_CYCLE := CYCLE;

END_FUNCTION_BLOCK
