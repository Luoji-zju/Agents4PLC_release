
FUNCTION_BLOCK F_CollectInput
VAR
    TICK : BOOL;         (* Signal to trigger input collection *)
    IN1 : BOOL;         (* Input 1 *)
    IN2 : BOOL;         (* Input 2 *)
    IN3 : BOOL;         (* Input 3 *)
    IN4 : BOOL;         (* Input 4 *)
    IN5 : BOOL;         (* Input 5 *)
    Data : ARRAY[1..5] OF BOOL;  (* Array to hold collected input signals *)
    index : INT := 1;  (* Index for the array *)
END_VAR

(* Collect inputs into the Data array when TICK is TRUE *)
IF TICK THEN
    Data[index] := IN1; 
    index := index + 1;
    Data[index] := IN2; 
    index := index + 1;
    Data[index] := IN3; 
    index := index + 1;
    Data[index] := IN4; 
    index := index + 1;
    Data[index] := IN5; 
    index := index + 1;
    
    IF index > 5 THEN
        index := 1;  (* Reset index for next collection cycle *)
    END_IF;
END_IF;
END_FUNCTION_BLOCK
