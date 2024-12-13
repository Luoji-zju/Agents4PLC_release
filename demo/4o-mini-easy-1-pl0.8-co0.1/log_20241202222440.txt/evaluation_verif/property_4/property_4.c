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
	bool i;
	int16_t macro;
	int16_t micro;
	int16_t o;
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
		if (__context->i) {
			goto l1;
		}
		if ((! __context->i)) {
			goto l9;
		}
		//assert(false);
		return;  			}
	l1: {
		if ((__context->micro > 0)) {
			__context->micro = (__context->micro - 1);
			goto l7;
		}
		if ((! (__context->micro > 0))) {
			__context->macro = (__context->macro + 1);
			goto l5;
		}
		//assert(false);
		return;  			}
	l5: {
			__context->micro = __context->macro;
			goto l7;
		//assert(false);
		return;  			}
	l7: {
			goto l9;
		//assert(false);
		return;  			}
	l9: {
			__context->o = __context->macro;
			goto l10;
		//assert(false);
		return;  			}
	l10: {
		if ((__context->macro < 0)) {
			__context->macro = 0;
			goto l14;
		}
		if ((! (__context->macro < 0))) {
			goto l14;
		}
		//assert(false);
		return;  			}
	l14: {
		if ((__context->micro < 0)) {
			__context->micro = 0;
			goto l18;
		}
		if ((! (__context->micro < 0))) {
			goto l18;
		}
		//assert(false);
		return;  			}
	l18: {
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
			instance.i = nondet_bool();
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
		assert((!(EoC) || (instance.o > 0)));
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
	instance.i = false;
	instance.macro = 0;
	instance.micro = 0;
	instance.o = 0;
	EoC = false;
	BoC = false;
	
	VerificationLoop();
}

