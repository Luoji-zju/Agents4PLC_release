
FUNCTION_BLOCK TOGGLE_OUTPUT
VAR_INPUT
    Button : BOOL; (* Input button signal *)
END_VAR_INPUT

VAR_OUTPUT
    ToggledOutput : BOOL := FALSE; (* Output state initialized to FALSE *)
END_VAR_OUTPUT

VAR
    PrevButtonState : BOOL := FALSE; (* Previous button state initialized to FALSE *)
END_VAR

(* Check for button press transition *)
IF (Button = TRUE) AND (PrevButtonState = FALSE) THEN
    ToggledOutput := NOT ToggledOutput; (* Toggle the output state *)
END_IF

(* Update the previous button state *)
PrevButtonState := Button;

END_FUNCTION_BLOCK
