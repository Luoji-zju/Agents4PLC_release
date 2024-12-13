

FUNCTION_BLOCK FB_TankControl
VAR_INPUT
    low_level_switch : BOOL;  // Input from low-level switch
    high_level_switch : BOOL; // Input from high-level switch
END_VAR

VAR_OUTPUT
    pump : BOOL; // Output to control the pump
END_VAR

VAR
    error_flag : BOOL := FALSE; // Error flag for handling malfunctions
END_VAR

// Main logic for controlling the tank filling system
IF low_level_switch THEN
    pump := TRUE; // Start the pump when low-level switch is activated
ELSIF high_level_switch THEN
    pump := FALSE; // Stop the pump when high-level switch is activated
ELSE
    pump := FALSE; // Ensure pump is off if neither switch is activated
END_IF

// Error handling (example: both switches activated simultaneously)
IF low_level_switch AND high_level_switch THEN
    error_flag := TRUE; // Set error flag if both switches are activated
END_IF

END_FUNCTION_BLOCK

PROGRAM prgTankControl
VAR
    fbTankControl : FB_TankControl; // Instance of the function block
    low_switch : BOOL; // Simulated input for low-level switch
    high_switch : BOOL; // Simulated input for high-level switch
    pump_status : BOOL; // Variable to hold pump status
END_VAR

// Simulate inputs (in real application, these would be mapped to actual I/O)
low_switch := FALSE; // Example: low-level switch is not activated
high_switch := FALSE; // Example: high-level switch is not activated

// Call the function block with inputs and get the pump status
fbTankControl(low_level_switch := low_switch, high_level_switch := high_switch, pump => pump_status);

END_PROGRAM

