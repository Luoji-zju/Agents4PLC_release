
FUNCTION_BLOCK FB_Sum
VAR_INPUT
    num1 : INT;
    num2 : INT;
END_VAR

VAR_OUTPUT
    sum : INT;
END_VAR

(* Subroutine to compute the sum of num1 and num2 *)
sum := num1 + num2;

END_FUNCTION_BLOCK

PROGRAM MAIN
VAR
    fb_sum_instance : FB_Sum;
    result : INT;
END_VAR

(* Call the function block with input values 5 and 7 *)
fb_sum_instance(num1 := 5, num2 := 7);

(* Store the result in the variable 'result' *)
result := fb_sum_instance.sum;

END_PROGRAM
