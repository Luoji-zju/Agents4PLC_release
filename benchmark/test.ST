FUNCTION_BLOCK FB_MotorControl
  VAR_INPUT
    Pressure_LOW : UINT; 
  END_VAR

  VAR_OUTPUT
    Motor_Critical : BOOL; 
  END_VAR

  VAR
    Threshold : UINT := 36464; 
  END_VAR
  
  IF (Pressure_LOW >= 36464) THEN
    Motor_Critical := False ;
  ELSE
    Motor_Critical := True ;
  END_IF;

END_FUNCTION_BLOCK