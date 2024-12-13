
PROGRAM PressureTemperatureControl
VAR_INPUT
    pressure_sensor: INT;   // Input from the pressure sensor
    temp_sensor: INT;       // Input from the temperature sensor
    GT1_OUT: BOOL;          // Control signal for relay
END_VAR

VAR
    counter: INT := 0;      // Counter for iterations
    error: BOOL := FALSE;   // Error flag
    error_code: INT := 0;   // Error code
    MAX_ITERATIONS: INT := 100; // Maximum number of iterations
END_VAR

(* Main control loop *)
WHILE counter < MAX_ITERATIONS DO
    // Adjust temperature based on pressure sensor reading
    IF pressure_sensor > 50 THEN
        temp_sensor := temp_sensor + 1; // Increment temperature
    ELSIF pressure_sensor < 20 THEN
        temp_sensor := temp_sensor - 1; // Decrement temperature
    END_IF

    // Update relay status based on GT1_OUT signal
    IF GT1_OUT THEN
        relay := TRUE; // Activate relay
    ELSE
        relay := FALSE; // Deactivate relay
    END_IF

    // Increment the counter
    counter := counter + 1;

    // Error checking for temperature limits
    IF temp_sensor < 0 OR temp_sensor > 100 THEN
        error := TRUE; // Set error flag
        error_code := -1; // Error code for temperature out of limits
    END_IF

    // Reset error flag if counter reaches 50
    IF counter = 50 THEN
        error := FALSE;
        error_code := 0; // Reset error code
    END_IF
END_WHILE

(* Program completion, returning error status *)
VAR_OUTPUT
    final_error: BOOL := error; // Outputs the final error status
END_VAR
END_PROGRAM

