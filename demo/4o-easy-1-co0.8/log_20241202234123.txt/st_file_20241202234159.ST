
FUNCTION_BLOCK FB_Estop_Processor
VAR_INPUT
    Field_Estop_IN : BOOL;  (* Input for field emergency stop *)
    R1_Estop_IN : BOOL;     (* Input for R1 emergency stop *)
    R2_Estop_IN : BOOL;     (* Input for R2 emergency stop *)
END_VAR

VAR_OUTPUT
    Field_Estop_OUT : BOOL; (* Output for field emergency stop *)
    R1_Estop_OUT : BOOL;    (* Output for R1 emergency stop *)
    R2_Estop_OUT : BOOL;    (* Output for R2 emergency stop *)
END_VAR

(* Invert each input signal to produce the corresponding output signal *)
Field_Estop_OUT := NOT Field_Estop_IN;
R1_Estop_OUT := NOT R1_Estop_IN;
R2_Estop_OUT := NOT R2_Estop_IN;

END_FUNCTION_BLOCK
