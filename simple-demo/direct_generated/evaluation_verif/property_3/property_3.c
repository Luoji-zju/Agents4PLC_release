#include <stdbool.h>
#include <stdint.h>
#include <assert.h>
#include <math.h>

// Declare nondet assignment functions
bool nondet_bool();
uint8_t nondet_uint8_t();
uint16_t nondet_uint16_t();
uint32_t nondet_uint32_t();
uint64_t nondet_uint64_t();
int8_t nondet_int8_t();
int16_t nondet_int16_t();
int32_t nondet_int32_t();
int64_t nondet_int64_t();
double nondet_float();
double nondet_double();

// Root data structure
typedef struct {
	float Pressure_LOW;
	bool Motor_Critical;
	float Threshold;
} __FB_MotorControl;

// Global variables
__FB_MotorControl instance;
bool EoC;
bool BoC;
bool __cbmc_boc_marker;
bool __cbmc_eoc_marker;

// Automata declarations
void FB_MotorControl(__FB_MotorControl *__context);
void VerificationLoop();

// Automata
void FB_MotorControl(__FB_MotorControl *__context) {
	// Temporary variables
	
	// Start with initial location
	goto init;
	init: {
		if ((__context->Pressure_LOW < __context->Threshold)) {
			__context->Motor_Critical = true;
			goto l5;
		}
		if ((! (__context->Pressure_LOW < __context->Threshold))) {
			__context->Motor_Critical = false;
			goto l5;
		}
		//assert(false);
		return;  			}
	l5: {
		goto __end_of_automaton;
		//assert(false);
		return;  			}
	
	// End of automaton
	__end_of_automaton: ;
}
void VerificationLoop() {
	// Temporary variables
	
	// Start with initial location
	goto init1;
	init1: {
			goto loop_start;
		//assert(false);
		return;  			}
	end: {
		goto __end_of_automaton;
		//assert(false);
		return;  			}
	loop_start: {
			
    while (isnan(instance.Pressure_LOW) || isinf(instance.Pressure_LOW)) {
        instance.Pressure_LOW = nondet_float();
    }
    
			BoC = true;
			goto prepare_BoC;
		if (false) {
			goto end;
		}
		//assert(false);
		return;  			}
	prepare_BoC: {
		__cbmc_boc_marker = true; // to indicate the beginning of the loop for the counterexample parser
		__cbmc_boc_marker = false;
			BoC = false;
			goto l_main_call;
		//assert(false);
		return;  			}
	l_main_call: {
			// Assign inputs
			FB_MotorControl(&instance);
			// Assign outputs
			goto callEnd;
		//assert(false);
		return;  			}
	callEnd: {
			EoC = true;
			goto prepare_EoC;
		//assert(false);
		return;  			}
	prepare_EoC: {
		assert((!(EoC) || ((instance.Pressure_LOW >= 0) && (instance.Pressure_LOW <= 65535))));
		__cbmc_eoc_marker = true; // to indicate the end of the loop for the counterexample parser
		__cbmc_eoc_marker = false;
			EoC = false;
			goto loop_start;
		//assert(false);
		return;  			}
	
	// End of automaton
	__end_of_automaton: ;
}

// Main
void main() {
	// Initial values
	instance.Pressure_LOW = 0.0;
	instance.Motor_Critical = false;
	instance.Threshold = 36464.0;
	EoC = false;
	BoC = false;
	
	VerificationLoop();
}

