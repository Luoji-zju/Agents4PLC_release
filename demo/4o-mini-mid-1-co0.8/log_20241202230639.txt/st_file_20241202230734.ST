
FUNCTION_BLOCK LatencyMonitor
VAR
    latency_xx_ms : DINT;      // Input latency in milliseconds
    NODE_xx_STATUS : UDINT;    // Node status (1 for active, 0 for inactive)
    errors_xx : DINT;           // Count of errors for the specific node
    errors_all : DINT;          // Total count of errors
    min_latency_ms : DINT;      // Minimum latency observed
    max_latency_ms : DINT;      // Maximum latency observed
END_VAR

(* Initialize error counts and latency extremes if not already set *)
IF (errors_xx < 0) THEN
    errors_xx := 0;
END_IF;

IF (errors_all < 0) THEN
    errors_all := 0;
END_IF;

IF (min_latency_ms < 0) THEN
    min_latency_ms := DINT#2147483647;   // Set to a high value
END_IF;

IF (max_latency_ms < 0) THEN
    max_latency_ms := DINT#-2147483648;  // Set to a low value
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
