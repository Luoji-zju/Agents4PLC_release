
FUNCTION_BLOCK FB_Estop_Processor
VAR_INPUT
    Field_Estop_IN : BOOL;  // Emergency stop input from field
    R1_Estop_IN    : BOOL;  // Emergency stop input from relay 1
    R2_Estop_IN    : BOOL;  // Emergency stop input from relay 2
END_VAR

VAR_OUTPUT
    Field_Estop_OUT : BOOL;  // Inverted output for field emergency stop
    R1_Estop_OUT    : BOOL;  // Inverted output for relay 1 emergency stop
    R2_Estop_OUT    : BOOL;  // Inverted output for relay 2 emergency stop
END_VAR

(* Implementing the logical NOT operation for each input signal *)
Field_Estop_OUT := NOT Field_Estop_IN;
R1_Estop_OUT := NOT R1_Estop_IN;
R2_Estop_OUT := NOT R2_Estop_IN;

END_FUNCTION_BLOCK
