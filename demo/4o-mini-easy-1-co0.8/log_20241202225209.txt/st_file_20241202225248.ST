
FUNCTION_BLOCK NOT_GATE
VAR_INPUT
    Input : BOOL;  (* Input boolean variable *)
END_VAR

VAR_OUTPUT
    NegatedOutput : BOOL;  (* Output for the negated value *)
END_VAR

(* Implementing the logic for negation *)
NegatedOutput := NOT Input;  (* Negation of the input variable *)

END_FUNCTION_BLOCK
