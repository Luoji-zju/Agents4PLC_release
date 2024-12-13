
FUNCTION_BLOCK FB_SequentialAssignment
    VAR_INPUT
        i : INT; (* Input variable *)
    END_VAR

    VAR
        a : INT; (* Intermediate variable *)
        b : INT; (* Intermediate variable *)
        c : INT; (* Intermediate variable *)
        d0 : INT; (* Intermediate variable *)
    END_VAR

    VAR_OUTPUT
        o : INT; (* Output variable *)
    END_VAR

    (* Sequential Assignment Logic *)
    a := i;
    b := a;
    c := b;
    d0 := c;
    o := d0;
END_FUNCTION_BLOCK

PROGRAM MAIN
VAR
    fbInstance : FB_SequentialAssignment; (* Instance of the function block *)
    inputValue : INT := 3; (* Input value *)
    outputValue : INT; (* Variable to hold the output value *)
END_VAR

(* Call the function block with the input value *)
fbInstance(i := inputValue);

(* Retrieve the output from the function block *)
outputValue := fbInstance.o;
END_PROGRAM
