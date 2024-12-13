
FUNCTION_BLOCK NOT_GATE
    VAR_INPUT
        Input : BOOL; // Boolean input for the NOT gate
    END_VAR
    
    VAR_OUTPUT
        NotResult : BOOL; // Boolean output for the NOT gate result
    END_VAR

    // Implementing the logic of the NOT gate
    NotResult := NOT Input;
    
END_FUNCTION_BLOCK
