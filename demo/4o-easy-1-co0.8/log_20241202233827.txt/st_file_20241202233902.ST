

FUNCTION_BLOCK FB_CalculateOutput
    VAR_INPUT
        i : INT;  // Input integer
    END_VAR

    VAR_OUTPUT
        o : INT;  // Output integer
    END_VAR

    // Implement conditional logic to calculate 'o' based on 'i'
    IF i = 0 THEN
        o := 0;
    ELSIF i >= 1 AND i <= 5 THEN
        o := i * i;  // Square of 'i'
    ELSIF i >= 6 AND i <= 10 THEN
        o := i + (2 * i);  // 'i' plus two times 'i'
    ELSE
        o := -1;  // Default case for any other value of 'i'
    END_IF;

END_FUNCTION_BLOCK

