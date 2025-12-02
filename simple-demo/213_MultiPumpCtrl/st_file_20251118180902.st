
FUNCTION_BLOCK MultiPumpCtrl
VAR_INPUT
    mode : BOOL;
    start : BOOL;
    stop : BOOL;
    priorities : ARRAY[1..5] OF INT;
    selections : ARRAY[1..5] OF BOOL;
END_VAR
VAR_OUTPUT
    RunComds : ARRAY[1..5] OF BOOL;
END_VAR
VAR
    i : INT;
    j : INT;
    maxPriority : INT;
    maxIndex : INT;
    runCount : INT;
    usedInAuto : ARRAY[1..5] OF BOOL;
END_VAR

(* Stop signal has highest priority *)
IF stop THEN
    FOR i := 1 TO 5 DO
        RunComds[i] := FALSE;
    END_FOR;
ELSE
    (* Mode selection logic *)
    IF NOT mode THEN (* Manual mode *)
        IF start THEN
            FOR i := 1 TO 5 DO
                RunComds[i] := selections[i];
            END_FOR;
        END_IF;
    ELSE (* Automatic mode *)
        IF start THEN
            (* Initialize usedInAuto array *)
            FOR i := 1 TO 5 DO
                usedInAuto[i] := FALSE;
            END_FOR;
            
            runCount := 0;
            
            (* Find 3 highest priority pumps *)
            WHILE runCount < 3 DO
                maxPriority := -32768; (* Minimum INT value *)
                maxIndex := 0;
                
                (* Find highest priority pump not already used *)
                FOR i := 1 TO 5 DO
                    IF (priorities[i] > maxPriority) AND NOT usedInAuto[i] THEN
                        maxPriority := priorities[i];
                        maxIndex := i;
                    END_IF;
                END_FOR;
                
                (* Mark pump as used and set run command *)
                IF maxIndex > 0 THEN
                    usedInAuto[maxIndex] := TRUE;
                    RunComds[maxIndex] := TRUE;
                    runCount := runCount + 1;
                END_IF;
            END_WHILE;
            
            (* Set remaining pumps to FALSE *)
            FOR i := 1 TO 5 DO
                IF NOT usedInAuto[i] THEN
                    RunComds[i] := FALSE;
                END_IF;
            END_FOR;
        END_IF;
    END_IF;
END_IF;
END_FUNCTION_BLOCK
