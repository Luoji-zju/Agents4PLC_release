
FUNCTION_BLOCK LatencyMonitor
VAR_INPUT
    latency_xx_ms : DINT;      // Latency in milliseconds
    NODE_xx_STATUS : UDINT;     // Node status
END_VAR_INPUT

VAR_IN_OUT
    errors_xx : DINT;           // Specific node error count
    errors_all : DINT;          // Total error count
    min_latency_ms : DINT;      // Minimum latency observed
    max_latency_ms : DINT;      // Maximum latency observed
END_VAR_IN_OUT

(* Check for errors based on latency and node status *)
IF (latency_xx_ms = 0) OR (NODE_xx_STATUS <> 1) THEN
    errors_xx := errors_xx + 1;  // Increment specific error count
    errors_all := errors_all + 1; // Increment total error count
END_IF

(* Update minimum latency if conditions are met *)
IF (latency_xx_ms < min_latency_ms) OR (min_latency_ms < 0) THEN
    min_latency_ms := latency_xx_ms; // Update minimum latency
END_IF

(* Update maximum latency if conditions are met *)
IF (latency_xx_ms > max_latency_ms) OR (max_latency_ms < 0) THEN
    max_latency_ms := latency_xx_ms; // Update maximum latency
END_IF

END_FUNCTION_BLOCK
