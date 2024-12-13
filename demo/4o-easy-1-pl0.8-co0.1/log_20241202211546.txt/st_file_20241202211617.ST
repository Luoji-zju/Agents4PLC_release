
FUNCTION_BLOCK TOGGLE_OUTPUT
VAR_INPUT
    Button : BOOL; (* Input variable to receive the button's state *)
END_VAR

VAR_OUTPUT
    ToggledOutput : BOOL := FALSE; (* Output variable to store the toggled state, initialized to FALSE *)
END_VAR

VAR
    PrevButtonState : BOOL := FALSE; (* Internal variable to keep track of the previous button state, initialized to FALSE *)
END_VAR

(* Logic to toggle the output based on button press *)
IF (Button = TRUE) AND (PrevButtonState = FALSE) THEN
    ToggledOutput := NOT ToggledOutput; (* Toggle the output state *)
END_IF;

(* Update the previous button state with the current button state *)
PrevButtonState := Button;

END_FUNCTION_BLOCK
