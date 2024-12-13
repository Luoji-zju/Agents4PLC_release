
PROGRAM MAIN
VAR
    pressure_sensor : REAL;  (* Pressure sensor value *)
    temperature_sensor : REAL;  (* Temperature sensor value *)
    relay : BOOL;  (* Relay status *)
    counter : INT := 0;  (* Counter for iterations *)
    error_code : INT;  (* Error code for temperature sensor *)
    error_flag : BOOL;  (* Flag to indicate if an error has occurred *)
    GT1_OUT : BOOL;  (* Control variable for relay *)
END_VAR

(* Set Loop Conditions *)
FOR counter := 1 TO 100 DO
    (* Pressure Sensor Checking *)
    IF pressure_sensor > 50 THEN
        temperature_sensor := temperature_sensor + 1;  (* Increment temperature *)
    ELSIF pressure_sensor < 20 THEN
        temperature_sensor := temperature_sensor - 1;  (* Decrement temperature *)
    END_IF;

    (* Relay Control *)
    IF GT1_OUT THEN
        relay := TRUE;  (* Set relay to TRUE *)
    ELSE
        relay := FALSE;  (* Set relay to FALSE *)
    END_IF;

    (* Error Handling *)
    IF temperature_sensor > 100 THEN
        error_code := 1;  (* Set error code for high temperature *)
        error_flag := TRUE;  (* Mark error flag as TRUE *)
    ELSIF temperature_sensor < 0 THEN
        error_code := 2;  (* Set error code for low temperature *)
        error_flag := TRUE;  (* Mark error flag as TRUE *)
    ELSE
        error_flag := FALSE;  (* No error *)
    END_IF;

    (* Counter Management *)
    IF counter >= 100 THEN
        counter := 100;  (* Ensure counter does not exceed maximum value *)
    END_IF;
END_FOR;

(* Return Status *)
VAR_OUTPUT
    execution_status : BOOL;  (* Status indicating successful execution *)
END_VAR_OUTPUT

execution_status := NOT error_flag;  (* TRUE if no errors occurred *)
END_PROGRAM
