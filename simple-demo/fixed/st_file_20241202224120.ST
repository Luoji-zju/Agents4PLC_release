
FUNCTION_BLOCK FB_CalculateOutput
VAR_INPUT
    i : INT;  // Input integer
END_VAR_INPUT

VAR_OUTPUT
    o : INT;  // Output value based on input conditions
END_VAR_OUTPUT

(* Implementing the conditional logic *)
IF i = 0 THEN
    o := 0;  // If input is 0, output is 0
ELSIF (i >= 1) AND (i <= 5) THEN
    o := i * i;  // If input is between 1 and 5, output is the square of input
ELSIF (i >= 6) AND (i <= 10) THEN
    o := i + (2 * i);  // If input is between 6 and 10, output is input plus double the input
ELSE
    o := -1;  // For all other values, output is -1
END_IF;

END_FUNCTION_BLOCK
