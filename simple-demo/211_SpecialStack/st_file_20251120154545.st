
FUNCTION_BLOCK StackMin
VAR_INPUT
    push : BOOL;
    pop : BOOL;
    reset : BOOL;
END_VAR
VAR_OUTPUT
    error : BOOL;
    status : WORD;
END_VAR
VAR_IN_OUT
    item : INT;
    stack : ARRAY[0..3] OF INT;
END_VAR
VAR
    top : INT := -1;
    min_index : INT;
    i : INT;
    temp_min : INT;
END_VAR

(* Reset has highest priority *)
IF reset THEN
    top := -1;
    error := FALSE;
    status := 16#0000;
(* Push operation *)
ELSIF push THEN
    IF top = 3 THEN
        error := TRUE;
        status := 16#8A04;
    ELSE
        top := top + 1;
        stack[top] := item;
        error := FALSE;
        status := 16#0000;
    END_IF;
(* Pop operation *)
ELSIF pop THEN
    IF top = -1 THEN
        error := TRUE;
        status := 16#8A05;
    ELSE
        (* Find minimum value and its index *)
        min_index := 0;
        temp_min := stack[0];
        FOR i := 1 TO top DO
            IF stack[i] < temp_min THEN
                temp_min := stack[i];
                min_index := i;
            END_IF;
        END_FOR;
        
        (* Store min value in output *)
        item := temp_min;
        
        (* Shift elements down *)
        FOR i := min_index TO top - 1 DO
            stack[i] := stack[i + 1];
        END_FOR;
        
        (* Decrement top *)
        top := top - 1;
        error := FALSE;
        status := 16#0000;
    END_IF;
(* No operation - clear error state *)
ELSE
    error := FALSE;
    status := 16#0000;
END_IF;
END_FUNCTION_BLOCK
