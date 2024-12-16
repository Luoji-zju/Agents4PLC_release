
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

    (* Logic to determine if the motor should be triggered based on the low pressure value *)
    IF Pressure_LOW < Threshold THEN
        Motor_Critical := TRUE;  (* Trigger the motor *)
    ELSE
        Motor_Critical := FALSE; (* Do not trigger the motor *)
    END_IF;
END_FUNCTION_BLOCK
