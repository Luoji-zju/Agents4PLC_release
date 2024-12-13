
FUNCTION_BLOCK FB_MotorControl
VAR_INPUT
    Pressure_LOW : REAL;
END_VAR

VAR_OUTPUT
    Motor_Critical : BOOL;
END_VAR

VAR
    Threshold : REAL := 36464.0;
END_VAR

(* Implementing the logic to evaluate motor activation based on pressure *)
IF Pressure_LOW < Threshold THEN
    Motor_Critical := TRUE;
ELSE
    Motor_Critical := FALSE;
END_IF;

END_FUNCTION_BLOCK
