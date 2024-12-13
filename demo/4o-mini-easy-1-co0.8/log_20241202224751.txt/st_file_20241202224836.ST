
FUNCTION_BLOCK FB_SequentialAssignment
VAR_INPUT
    i : INT;   // Input variable
END_VAR

VAR
    a : INT;   // Intermediate variable
    b : INT;   // Intermediate variable
    c : INT;   // Intermediate variable
    d0 : INT;  // Intermediate variable
END_VAR

VAR_OUTPUT
    o : INT;   // Output variable
END_VAR

// Sequentially assign values
a := i;      // Assign input to a
b := a;      // Assign a to b
c := b;      // Assign b to c
d0 := c;     // Assign c to d0
o := d0;     // Assign d0 to output o
END_FUNCTION_BLOCK

PROGRAM MAIN
VAR
    fb : FB_SequentialAssignment; // Instance of the function block
END_VAR

// Call the function block with input value 3
fb(i := 3);

// The output variable o can be observed via fb.o after execution
END_PROGRAM
