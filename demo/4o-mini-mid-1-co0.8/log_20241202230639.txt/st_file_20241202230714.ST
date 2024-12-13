

FUNCTION_BLOCK LatencyMonitor
VAR_INPUT
    latency_xx_ms : REAL;      // Input latency in milliseconds
    NODE_xx_STATUS : INT;      // Node status (1 for active, 0 for inactive)
END_VAR_INPUT

VAR_IN_OUT
    errors_xx : INT;           // Count of errors for the specific node
    errors_all : INT;          // Total count of errors
    min_latency_ms : REAL;     // Minimum latency observed
    max_latency_ms : REAL;     // Maximum latency observed
END_VAR_IN_OUT

(* Initialize error counts and latency extremes if not already set *)
IF (errors_xx < 0) THEN
    errors_xx := 0;
END_IF;

IF (errors_all < 0) THEN
    errors_all := 0;
END_IF;

IF (min_latency_ms < 0) THEN
    min_latency_ms := REAL#Infinity;   // Set to a high value
END_IF;

IF (max_latency_ms < 0) THEN
    max_latency_ms := -REAL#Infinity;  // Set to a low value
END_IF;

(* Check for error conditions *)
IF (latency_xx_ms = 0 OR NODE_xx_STATUS <> 1) THEN
    errors_xx := errors_xx + 1;      // Increment specific error count
    errors_all := errors_all + 1;    // Increment total error count
END_IF;

(* Update minimum latency if applicable *)
IF (latency_xx_ms < min_latency_ms) THEN
    min_latency_ms := latency_xx_ms;
END_IF;

(* Update maximum latency if applicable *)
IF (latency_xx_ms > max_latency_ms) THEN
    max_latency_ms := latency_xx_ms;
END_IF;

END_FUNCTION_BLOCK

