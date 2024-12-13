
FUNCTION_BLOCK FB_MotorControl
VAR_INPUT
    Pressure_LOW : REAL;  (* Input variable for low pressure value *)
END_VAR

VAR_OUTPUT
    Motor_Critical : BOOL;  (* Output variable indicating motor activation status *)
END_VAR

VAR
    Threshold : REAL := 36464;  (* Local variable for critical pressure limit *)
END_VAR

(* Conditional evaluation to determine if the motor should be activated *)
IF Pressure_LOW < Threshold THEN
    Motor_Critical := TRUE;  (* Activate motor if pressure is below threshold *)
ELSE
    Motor_Critical := FALSE;  (* Do not activate motor if pressure is above threshold *)
END_IF;

END_FUNCTION_BLOCK
