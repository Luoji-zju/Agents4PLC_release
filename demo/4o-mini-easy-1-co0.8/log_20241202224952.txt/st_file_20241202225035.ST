
FUNCTION_BLOCK FIND_MAX_VALUE
VAR_INPUT
    Value1 : INT; // First integer input
    Value2 : INT; // Second integer input
END_VAR

VAR_OUTPUT
    MaxValue : INT; // Output for the maximum value
END_VAR

(* Compare Value1 and Value2 and assign the maximum to MaxValue *)
IF Value1 > Value2 THEN
    MaxValue := Value1;
ELSE
    MaxValue := Value2;
END_IF;

END_FUNCTION_BLOCK

FUNCTION_BLOCK FIND_MIN_VALUE
VAR_INPUT
    Value1 : INT; // First integer input
    Value2 : INT; // Second integer input
END_VAR

VAR_OUTPUT
    MinValue : INT; // Output for the minimum value
END_VAR

(* Compare Value1 and Value2 and assign the minimum to MinValue *)
IF Value1 < Value2 THEN
    MinValue := Value1;
ELSE
    MinValue := Value2;
END_IF;

END_FUNCTION_BLOCK

FUNCTION_BLOCK FIND_MAX_OF_THREE
VAR_INPUT
    Value1 : INT; // First integer input
    Value2 : INT; // Second integer input
    Value3 : INT; // Third integer input
END_VAR

VAR_OUTPUT
    MaxValue : INT; // Output for the maximum value
END_VAR

(* Assume Value1 is the largest initially *)
MaxValue := Value1;

(* Check if Value2 is greater than MaxValue *)
IF Value2 > MaxValue THEN
    MaxValue := Value2;
END_IF;

(* Check if Value3 is greater than MaxValue *)
IF Value3 > MaxValue THEN
    MaxValue := Value3;
END_IF;

END_FUNCTION_BLOCK

PROGRAM MainProgram
VAR
    maxValueResult : INT; // Variable to hold result of max value
    minValueResult : INT; // Variable to hold result of min value
    maxOfThreeResult : INT; // Variable to hold result of max of three
    fbMax : FIND_MAX_VALUE; // Instance of FIND_MAX_VALUE function block
    fbMin : FIND_MIN_VALUE; // Instance of FIND_MIN_VALUE function block
    fbMaxOfThree : FIND_MAX_OF_THREE; // Instance of FIND_MAX_OF_THREE function block
END_VAR

(* Example usage of the function blocks *)
fbMax(Value1 := 10, Value2 := 5);
maxValueResult := fbMax.MaxValue;

fbMin(Value1 := 10, Value2 := 5);
minValueResult := fbMin.MinValue;

fbMaxOfThree(Value1 := 10, Value2 := 15, Value3 := 12);
maxOfThreeResult := fbMaxOfThree.MaxValue;

END_PROGRAM
