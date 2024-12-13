
FUNCTION_BLOCK NOT_GATE
VAR_INPUT
    Input : BOOL;  (* Input boolean variable *)
END_VAR_INPUT

VAR_OUTPUT
    NegatedOutput : BOOL;  (* Output for the negated value *)
END_VAR_OUTPUT

(* Implementing the logic for negation *)
NegatedOutput := NOT Input;  (* Negation of the input variable *)

END_FUNCTION_BLOCK
