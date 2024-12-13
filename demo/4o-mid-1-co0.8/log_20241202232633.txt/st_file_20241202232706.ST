
FUNCTION_BLOCK LatencyMonitor
VAR_INPUT
    latency_xx_ms : INT;  (* Latency time in milliseconds for the specific node *)
    NODE_xx_STATUS : INT; (* Current status of the node *)
END_VAR

VAR_IN_OUT
    errors_xx : INT;      (* Error count for the specific node *)
    errors_all : INT;     (* Total error count across all nodes *)
    min_latency_ms : INT; (* Minimum observed latency in milliseconds *)
    max_latency_ms : INT; (* Maximum observed latency in milliseconds *)
END_VAR

(* Main logic of the function block *)
IF (latency_xx_ms = 0) OR (NODE_xx_STATUS <> 1) THEN
    errors_xx := errors_xx + 1;
    errors_all := errors_all + 1;
END_IF;

IF (latency_xx_ms < min_latency_ms) OR (min_latency_ms < 0) THEN
    min_latency_ms := latency_xx_ms;
END_IF;

IF (latency_xx_ms > max_latency_ms) OR (max_latency_ms < 0) THEN
    max_latency_ms := latency_xx_ms;
END_IF;

END_FUNCTION_BLOCK
