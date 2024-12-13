
FUNCTION_BLOCK FB_CalculateOutput
VAR_INPUT
    i : INT;  (* Input variable of type INT *)
END_VAR

VAR_OUTPUT
    o : INT;  (* Output variable of type INT *)
END_VAR

(* Main logic to determine output based on input conditions *)
IF i = 0 THEN
    o := 0;  (* If input is 0, output is 0 *)
ELSIF i >= 1 AND i <= 5 THEN
    o := i * i;  (* If input is between 1 and 5, output is the square of input *)
ELSIF i >= 6 AND i <= 10 THEN
    o := i + 2 * i;  (* If input is between 6 and 10, output is input plus two times input *)
ELSE
    o := -1;  (* For any other value, output is -1 *)
END_IF;

END_FUNCTION_BLOCK
