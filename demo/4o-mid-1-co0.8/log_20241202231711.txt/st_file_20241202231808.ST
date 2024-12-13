

FUNCTION_BLOCK FB_OperationControl
    VAR_INPUT
        PressureSensor : REAL;
        TemperatureSensor : REAL;
        RelayStatus : BOOL;
        Counter : INT;
        GT1_OUT : BOOL;
    END_VAR

    VAR_OUTPUT
        OperationComplete : BOOL;
        UpdatedPressureSensor : REAL;
        UpdatedTemperatureSensor : REAL;
        UpdatedRelayStatus : BOOL;
        UpdatedCounter : INT;
        ErrorFlag : BOOL;
        ErrorCode : INT;
    END_VAR

    VAR
        OverflowDetected : BOOL;
    END_VAR
    
    (* Initialize variables *)
    UpdatedPressureSensor := PressureSensor;
    UpdatedTemperatureSensor := TemperatureSensor;
    UpdatedRelayStatus := RelayStatus;
    UpdatedCounter := Counter;
    ErrorFlag := FALSE;
    ErrorCode := 0;
    OperationComplete := FALSE;
    OverflowDetected := FALSE;

    (* Loop until operation is complete *)
    WHILE NOT OperationComplete DO

        (* Check for overflow in the pressure sensor *)
        IF UpdatedPressureSensor > 100.0 THEN
            OverflowDetected := TRUE;
            ErrorFlag := TRUE;
            ErrorCode := 1; (* Overflow error code *)
        ELSE
            OverflowDetected := FALSE;
        END_IF

        (* Adjust the temperature sensor based on pressure sensor value *)
        IF NOT OverflowDetected THEN
            IF UpdatedPressureSensor < 50.0 THEN
                UpdatedTemperatureSensor := UpdatedTemperatureSensor + 5.0;
            ELSE
                UpdatedTemperatureSensor := UpdatedTemperatureSensor - 3.0;
            END_IF
        END_IF

        (* Update the relay status according to GT1_OUT value *)
        UpdatedRelayStatus := GT1_OUT;

        (* Increment the counter *)
        UpdatedCounter := UpdatedCounter + 1;

        (* Check if operation is complete *)
        IF UpdatedCounter >= 10 THEN
            OperationComplete := TRUE;
        END_IF

    END_WHILE

END_FUNCTION_BLOCK

PROGRAM prg_Main
    VAR
        fbControl : FB_OperationControl;
        initialPressure : REAL := 45.0;
        initialTemperature : REAL := 70.0;
        initialRelayStatus : BOOL := FALSE;
        initialCounter : INT := 0;
        initialGT1_OUT : BOOL := TRUE;
        isComplete : BOOL;
    END_VAR

    (* Execute the function block *)
    fbControl(
        PressureSensor := initialPressure,
        TemperatureSensor := initialTemperature,
        RelayStatus := initialRelayStatus,
        Counter := initialCounter,
        GT1_OUT := initialGT1_OUT,
        OperationComplete => isComplete
    );

END_PROGRAM

