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
	bool flag;
	int16_t count;
	int16_t i;
	int16_t j;
	int16_t maxIterations;
} __FB_LoopCounter;

// Global variables
__FB_LoopCounter instance;
bool EoC;
bool BoC;
bool __cbmc_boc_marker;
bool __cbmc_eoc_marker;

// Automata declarations
void FB_LoopCounter(__FB_LoopCounter *__context);
void VerificationLoop();

// Automata
void FB_LoopCounter(__FB_LoopCounter *__context) {
	// Temporary variables
	
	// Start with initial location
	goto init;
	init: {
			__context->count = 0;
			__context->i = 0;
			goto l17;
		//assert(false);
		return;  			}
	l3: {
		if (__context->flag) {
			goto l13;
		}
		if ((! __context->flag)) {
			__context->count = (__context->count + 1);
			goto l8;
		}
		//assert(false);
		return;  			}
	l8: {
		if ((__context->count >= __context->maxIterations)) {
			goto l13;
		}
		if ((! (__context->count >= __context->maxIterations))) {
			__context->j = (__context->j + 2);
			goto l14;
		}
		//assert(false);
		return;  			}
	l13: {
			__context->i = (__context->i + 1);
			goto l17;
		//assert(false);
		return;  			}
	l14: {
		if ((__context->j <= 100)) {
			goto l3;
		}
		if ((! (__context->j <= 100))) {
			goto l13;
		}
		//assert(false);
		return;  			}
	l16: {
		goto __end_of_automaton;
		//assert(false);
		return;  			}
	l17: {
		if ((__context->i <= 10)) {
			__context->j = 10;
			goto l14;
		}
		if ((! (__context->i <= 10))) {
			goto l16;
		}
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
			instance.flag = nondet_bool();
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
			FB_LoopCounter(&instance);
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
		assert((!(EoC) || ((instance.j >= 10) && (instance.j <= 100))));
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
	instance.flag = false;
	instance.count = 0;
	instance.i = 0;
	instance.j = 0;
	instance.maxIterations = 45;
	EoC = false;
	BoC = false;
	
	VerificationLoop();
}

