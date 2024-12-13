

FUNCTION_BLOCK dw
VAR_INPUT
    i : INT;
END_VAR
VAR_OUTPUT
    o : INT;
END_VAR
VAR
    ss : INT := 0; // Internal variable initialized to 0
END_VAR

// Increment ss on every execution
ss := ss + 1;

// Conditional check for input 'i'
IF i = 1 THEN
    o := 1;
ELSE
    o := ss;
END_IF
END_FUNCTION_BLOCK

PROGRAM MAIN
VAR
    fb_dw : dw; // Instance of Function Block dw
    input_i : INT := 3; // Input value
    output_o : INT; // Variable to store output
END_VAR

// Execute the function block with input value
fb_dw(i := input_i, o => output_o);
END_PROGRAM

