
FUNCTION_BLOCK FB_MaxMin
VAR_INPUT
    A : REAL;
    B : REAL;
END_VAR

VAR_OUTPUT
    MAX_OUT : REAL;
    MIN_OUT : REAL;
END_VAR

(* Corrected structure for max value assignment *)
IF A > B THEN
    MAX_OUT := A;
ELSE
    MAX_OUT := B;
END_IF;

(* Corrected structure for min value assignment *)
IF A < B THEN
    MIN_OUT := A;
ELSE
    MIN_OUT := B;
END_IF;

END_FUNCTION_BLOCK
