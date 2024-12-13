

(* Define the function block F_CollectInput as per the requirements *)
FUNCTION_BLOCK F_CollectInput
VAR_INPUT
    TICK : BOOL;
    RESET : BOOL;
    IN1 : BOOL;
    IN2 : BOOL;
    IN3 : BOOL;
    IN4 : BOOL;
    IN5 : BOOL;
END_VAR

VAR_OUTPUT
    OutputSignal : BOOL;
END_VAR

VAR
    InternalState : BOOL;
END_VAR

(* Logic for the function block *)
IF RESET THEN
    InternalState := FALSE;
ELSIF TICK THEN
    InternalState := IN1 OR IN2 OR IN3 OR IN4 OR IN5;
END_IF;

OutputSignal := InternalState;
END_FUNCTION_BLOCK

(* Main program *)
PROGRAM MainProgram
VAR
    ClockSignal : BOOL;
    ResetSignal : BOOL;
    InputSignal1 : BOOL;
    InputSignal2 : BOOL;
    InputSignal3 : BOOL;
    InputSignal4 : BOOL;
    InputSignal5 : BOOL;
    fbCollectInput : F_CollectInput; (* Instance of the function block *)
    ResultSignal : BOOL;
END_VAR

(* Invocation of the function block with correct parameters *)
fbCollectInput(TICK := ClockSignal, RESET := ResetSignal, IN1 := InputSignal1, IN2 := InputSignal2, IN3 := InputSignal3, IN4 := InputSignal4, IN5 := InputSignal5);

ResultSignal := fbCollectInput.OutputSignal;
END_PROGRAM

