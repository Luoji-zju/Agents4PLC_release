
FUNCTION_BLOCK FB_MonitorSignals
VAR_INPUT
    Start_Stop : BOOL;  // Input signal to monitor for rising edge
END_VAR

VAR_OUTPUT
    ONS_Trig : BOOL;    // Output signal set to TRUE on rising edge
    ON_OFF : BOOL;      // Output signal toggled based on XOR logic
    Rising_ONS : BOOL;  // Stores current state of Start_Stop for next cycle
END_VAR

VAR
    Prev_Start_Stop : BOOL := FALSE;  // Internal variable to track previous state of Start_Stop
END_VAR

// Detect rising edge of Start_Stop
ONS_Trig := (NOT Prev_Start_Stop) AND Start_Stop;

// Toggle ON_OFF based on XOR of ONS_Trig and current ON_OFF state
ON_OFF := ONS_Trig XOR ON_OFF;

// Update Rising_ONS and Prev_Start_Stop for next cycle
Rising_ONS := Start_Stop;
Prev_Start_Stop := Start_Stop;

END_FUNCTION_BLOCK
