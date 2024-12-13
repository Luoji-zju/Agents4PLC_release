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
	int16_t N;
	int16_t O;
	int16_t F1;
	int16_t F2;
	int16_t CNT;
	int16_t Temp;
} __FB_Fibonacci_Calculator;

// Global variables
__FB_Fibonacci_Calculator instance;
bool EoC;
bool BoC;
bool __cbmc_boc_marker;
bool __cbmc_eoc_marker;

// Automata declarations
void FB_Fibonacci_Calculator(__FB_Fibonacci_Calculator *__context);
void VerificationLoop();

// Automata
void FB_Fibonacci_Calculator(__FB_Fibonacci_Calculator *__context) {
	// Temporary variables
	
	// Start with initial location
	goto init;
	init: {
		if ((__context->N <= 2)) {
			__context->O = 1;
			goto l16;
		}
		if ((! (__context->N <= 2))) {
			goto l3;
		}
		//assert(false);
		return;  			}
	l3: {
		if ((__context->CNT < __context->N)) {
			__context->Temp = (__context->F1 + __context->F2);
			goto l5;
		}
		if ((! (__context->CNT < __context->N))) {
			goto l14;
		}
		//assert(false);
		return;  			}
	l5: {
		if ((__context->Temp > 32767)) {
			__context->O = 32767;
			goto l14;
		}
		if ((! (__context->Temp > 32767))) {
			__context->F1 = __context->F2;
			goto l11;
		}
		//assert(false);
		return;  			}
	l11: {
			__context->F2 = __context->Temp;
			__context->CNT = (__context->CNT + 1);
			goto l3;
		//assert(false);
		return;  			}
	l14: {
			__context->O = __context->F2;
			goto l16;
		//assert(false);
		return;  			}
	l16: {
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
			instance.N = nondet_int16_t();
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
			FB_Fibonacci_Calculator(&instance);
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
		assert((!(EoC) || (instance.O >= 0)));
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
	instance.N = 5;
	instance.O = 0;
	instance.F1 = 1;
	instance.F2 = 1;
	instance.CNT = 2;
	instance.Temp = 0;
	EoC = false;
	BoC = false;
	
	VerificationLoop();
}

