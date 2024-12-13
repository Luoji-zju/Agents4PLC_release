
FUNCTION_BLOCK FB_MotorControl
VAR_INPUT
    Pressure_LOW : REAL; (* Input pressure value *)
END_VAR

VAR_OUTPUT
    Motor_Critical : BOOL; (* Output indicating motor activation state *)
END_VAR

VAR
    Threshold : REAL := 36464.0; (* Predefined threshold value *)
END_VAR

(* Compare Pressure_LOW with Threshold and set Motor_Critical accordingly *)
IF Pressure_LOW < Threshold THEN
    Motor_Critical := TRUE; (* Activate motor if pressure is low *)
ELSE
    Motor_Critical := FALSE; (* Deactivate motor if pressure is sufficient *)
END_IF;

END_FUNCTION_BLOCK
