
FUNCTION_BLOCK FB_Estop_Processor
VAR_INPUT
    Field_Estop_IN : BOOL;
    R1_Estop_IN : BOOL;
    R2_Estop_IN : BOOL;
    R3_Estop_IN : BOOL;
    B1_Estop_IN : BOOL;
    B2_Estop_IN : BOOL;
    B3_Estop_IN : BOOL;
END_VAR

VAR_OUTPUT
    Field_Estop_OUT : BOOL;
    R1_Estop_OUT : BOOL;
    R2_Estop_OUT : BOOL;
    R3_Estop_OUT : BOOL;
    B1_Estop_OUT : BOOL;
    B2_Estop_OUT : BOOL;
    B3_Estop_OUT : BOOL;
END_VAR

(* Invert each input signal to produce the corresponding output signal *)
Field_Estop_OUT := NOT Field_Estop_IN;
R1_Estop_OUT := NOT R1_Estop_IN;
R2_Estop_OUT := NOT R2_Estop_IN;
R3_Estop_OUT := NOT R3_Estop_IN;
B1_Estop_OUT := NOT B1_Estop_IN;
B2_Estop_OUT := NOT B2_Estop_IN;
B3_Estop_OUT := NOT B3_Estop_IN;

END_FUNCTION_BLOCK
