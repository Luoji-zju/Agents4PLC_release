
FUNCTION_BLOCK FB_MonitorLatency
VAR_INPUT
    latency : REAL;
    NODE_STATUS : INT;
END_VAR

VAR_IN_OUT
    latency_errors : INT;
    total_errors : INT;
    min_latency : REAL;
    max_latency : REAL;
END_VAR

VAR
    is_error : BOOL;
END_VAR

(* Check for latency errors and update error counts *)
IF (latency = 0) OR (NODE_STATUS <> 1) THEN
    is_error := TRUE;
    latency_errors := latency_errors + 1;
    total_errors := total_errors + 1;
ELSE
    is_error := FALSE;
END_IF

(* Update minimum latency if the new latency is less than the current minimum or if the current minimum is negative *)
IF (latency < min_latency) OR (min_latency < 0) THEN
    min_latency := latency;
END_IF

(* Update maximum latency if the new latency is greater than the current maximum or if the current maximum is negative *)
IF (latency > max_latency) OR (max_latency < 0) THEN
    max_latency := latency;
END_IF

END_FUNCTION_BLOCK
