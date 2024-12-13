
FUNCTION_BLOCK F_CollectInput
VAR_INPUT
    IN1 : BOOL;
    IN2 : BOOL;
    IN3 : BOOL;
    IN4 : BOOL;
    IN5 : BOOL;
    TICK : BOOL;
END_VAR

VAR_OUTPUT
    Data : ARRAY[0..19] OF BOOL;
    Finished : BOOL;
END_VAR

VAR
    j : INT := 0;  (* Index for storing data in the array *)
END_VAR

(* Collect input signals into the Data array when TICK is TRUE *)
IF TICK THEN
    IF j < 20 THEN
        Data[j] := IN1 OR IN2 OR IN3 OR IN4 OR IN5;  (* Collecting the input signals *)
        j := j + 1;  (* Increment index for next data collection *)
    ELSE
        Finished := TRUE;  (* Indicate that data collection is finished *)
    END_IF;
ELSE
    Finished := FALSE;  (* Reset finished flag if TICK is not active *)
END_IF;

END_FUNCTION_BLOCK

PROGRAM MAIN
VAR_INPUT
    IN1 : BOOL;
    IN2 : BOOL;
    IN3 : BOOL;
    IN4 : BOOL;
    IN5 : BOOL;
    TICK : BOOL;
    RESET : BOOL;
END_VAR

VAR_OUTPUT
    Out : BOOL;
    OutReady : BOOL;
    FeedNext : BOOL;
END_VAR

VAR
    fb_CollectInput : F_CollectInput;  (* Instance of the function block *)
    A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15 : BOOL;  (* Boolean conditions *)
END_VAR

(* Call the function block to collect inputs *)
fb_CollectInput(IN1 := IN1, IN2 := IN2, IN3 := IN3, IN4 := IN4, IN5 := IN5, TICK := TICK);

(* Process the collected data after collection is finished *)
IF fb_CollectInput.Finished THEN
    (* Example logical conditions based on the Data array *)
    A1 := fb_CollectInput.Data[0];
    A2 := fb_CollectInput.Data[1];
    A3 := fb_CollectInput.Data[2];
    A4 := fb_CollectInput.Data[3];
    A5 := fb_CollectInput.Data[4];
    A6 := fb_CollectInput.Data[5];
    A7 := fb_CollectInput.Data[6];
    A8 := fb_CollectInput.Data[7];
    A9 := fb_CollectInput.Data[8];
    A10 := fb_CollectInput.Data[9];
    A11 := fb_CollectInput.Data[10];
    A12 := fb_CollectInput.Data[11];
    A13 := fb_CollectInput.Data[12];
    A14 := fb_CollectInput.Data[13];
    A15 := fb_CollectInput.Data[14];

    (* Example logical operation to determine the output *)
    Out := (A1 AND NOT A2) OR (A3 AND A4) OR (A5 AND NOT A6);
    
    OutReady := TRUE;  (* Indicate that output is ready *)
    FeedNext := TRUE;  (* Indicate that the next cycle can proceed *)
ELSE
    OutReady := FALSE;  (* Reset output ready flag if not finished *)
    FeedNext := FALSE;  (* Reset feed next flag if not finished *)
END_IF;

(* Reset logic for the next data collection cycle *)
IF RESET THEN
    fb_CollectInput := F_CollectInput();  (* Reinitialize the function block *)
END_IF;

END_PROGRAM
