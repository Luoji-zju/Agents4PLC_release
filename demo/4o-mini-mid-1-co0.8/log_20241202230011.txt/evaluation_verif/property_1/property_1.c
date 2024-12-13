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
	bool TICK;
	bool IN1;
	bool IN2;
	bool IN3;
	bool IN4;
	bool IN5;
	bool Data[6];
	int16_t index;
} __F_CollectInput;

// Global variables
__F_CollectInput instance;
uint16_t __assertion_error;
bool __cbmc_boc_marker;
bool __cbmc_eoc_marker;

// Automata declarations
void F_CollectInput(__F_CollectInput *__context);
void VerificationLoop();

// Automata
void F_CollectInput(__F_CollectInput *__context) {
	// Temporary variables
	
	// Start with initial location
	goto init;
	init: {
		if (__context->TICK) {
			__context->Data[__context->index] = __context->IN1;
			goto l2;
		}
		if ((! __context->TICK)) {
			goto l17;
		}
		//assert(false);
		return;  			}
	l2: {
			__context->index = (__context->index + 1);
			__context->Data[__context->index] = __context->IN2;
			goto l4;
		//assert(false);
		return;  			}
	l4: {
			__context->index = (__context->index + 1);
			__context->Data[__context->index] = __context->IN3;
			goto l6;
		//assert(false);
		return;  			}
	l6: {
			__context->index = (__context->index + 1);
			__context->Data[__context->index] = __context->IN4;
			goto l8;
		//assert(false);
		return;  			}
	l8: {
			__context->index = (__context->index + 1);
			__context->Data[__context->index] = __context->IN5;
			goto l10;
		//assert(false);
		return;  			}
	l10: {
			__context->index = (__context->index + 1);
			goto l11;
		//assert(false);
		return;  			}
	l11: {
		if ((__context->index > 5)) {
			__context->index = 1;
			goto l15;
		}
		if ((! (__context->index > 5))) {
			goto l15;
		}
		//assert(false);
		return;  			}
	l15: {
			goto l17;
		//assert(false);
		return;  			}
	l17: {
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
			goto prepare_BoC;
		if (false) {
			goto end;
		}
		//assert(false);
		return;  			}
	prepare_BoC: {
		__cbmc_boc_marker = true; // to indicate the beginning of the loop for the counterexample parser
		__cbmc_boc_marker = false;
			goto l_main_call;
		//assert(false);
		return;  			}
	l_main_call: {
			// Assign inputs
			F_CollectInput(&instance);
			// Assign outputs
			goto callEnd;
		//assert(false);
		return;  			}
	callEnd: {
			goto prepare_EoC;
		//assert(false);
		return;  			}
	prepare_EoC: {
		assert((__assertion_error == 0));
		__cbmc_eoc_marker = true; // to indicate the end of the loop for the counterexample parser
		__cbmc_eoc_marker = false;
			goto loop_start;
		//assert(false);
		return;  			}
	
	// End of automaton
	__end_of_automaton: ;
}

// Main
void main() {
	// Initial values
	instance.TICK = false;
	instance.IN1 = false;
	instance.IN2 = false;
	instance.IN3 = false;
	instance.IN4 = false;
	instance.IN5 = false;
	instance.Data[1] = false;
	instance.Data[2] = false;
	instance.Data[3] = false;
	instance.Data[4] = false;
	instance.Data[5] = false;
	instance.index = 1;
	__assertion_error = 0;
	
	VerificationLoop();
}

