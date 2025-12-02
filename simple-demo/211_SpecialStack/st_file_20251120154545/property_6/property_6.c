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
	bool push;
	bool pop;
	bool reset;
	bool error;
	uint16_t status;
	int16_t item;
	int16_t stack[4];
	int16_t top;
	int16_t min_index;
	int16_t i;
	int16_t temp_min;
} __StackMin;

// Global variables
__StackMin instance;
bool EoC;
bool BoC;
bool __cbmc_boc_marker;
bool __cbmc_eoc_marker;

// Automata declarations
void StackMin(__StackMin *__context);
void VerificationLoop();

// Automata
void StackMin(__StackMin *__context) {
	// Temporary variables
	
	// Start with initial location
	goto init;
	init: {
		if (__context->reset) {
			__context->top = (- 1);
			__context->error = false;
			__context->status = 0;
			goto l44;
		}
		if (((! __context->reset) && __context->push)) {
			goto l5;
		}
		if ((((! __context->reset) && (! __context->push)) && __context->pop)) {
			goto l15;
		}
		if (((! __context->reset) && ((! ((! __context->reset) && __context->push)) && (! (((! __context->reset) && (! __context->push)) && __context->pop))))) {
			__context->error = false;
			__context->status = 0;
			goto l44;
		}
		//assert(false);
		return;  			}
	l5: {
		if ((__context->top == 3)) {
			__context->error = true;
			__context->status = 35332;
			goto l14;
		}
		if ((! (__context->top == 3))) {
			__context->top = (__context->top + 1);
			__context->stack[__context->top] = __context->item;
			__context->error = false;
			__context->status = 0;
			goto l14;
		}
		//assert(false);
		return;  			}
	l14: {
			goto l44;
		//assert(false);
		return;  			}
	l15: {
		if ((__context->top == (- 1))) {
			__context->error = true;
			__context->status = 35333;
			goto l40;
		}
		if ((! (__context->top == (- 1)))) {
			__context->min_index = 0;
			__context->temp_min = __context->stack[0];
			__context->i = 1;
			goto l29;
		}
		//assert(false);
		return;  			}
	l22: {
		if ((__context->stack[__context->i] < __context->temp_min)) {
			__context->temp_min = __context->stack[__context->i];
			__context->min_index = __context->i;
			goto l27;
		}
		if ((! (__context->stack[__context->i] < __context->temp_min))) {
			goto l27;
		}
		//assert(false);
		return;  			}
	l27: {
			__context->i = (__context->i + 1);
			goto l29;
		//assert(false);
		return;  			}
	l29: {
		if ((__context->i <= __context->top)) {
			goto l22;
		}
		if ((! (__context->i <= __context->top))) {
			__context->item = __context->temp_min;
			__context->i = __context->min_index;
			goto l35;
		}
		//assert(false);
		return;  			}
	l33: {
			__context->i = (__context->i + 1);
			goto l35;
		//assert(false);
		return;  			}
	l35: {
		if ((__context->i <= (__context->top - 1))) {
			__context->stack[__context->i] = __context->stack[(__context->i + 1)];
			goto l33;
		}
		if ((! (__context->i <= (__context->top - 1)))) {
			__context->top = (__context->top - 1);
			__context->error = false;
			__context->status = 0;
			goto l40;
		}
		//assert(false);
		return;  			}
	l40: {
			goto l44;
		//assert(false);
		return;  			}
	l44: {
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
			instance.item = nondet_int16_t();
			instance.pop = nondet_bool();
			instance.push = nondet_bool();
			instance.reset = nondet_bool();
			instance.stack[0] = nondet_int16_t();
			instance.stack[1] = nondet_int16_t();
			instance.stack[2] = nondet_int16_t();
			instance.stack[3] = nondet_int16_t();
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
			StackMin(&instance);
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
		assert((!((EoC && (instance.reset == true))) || ((instance.error == false) && (instance.status == 0))));
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
	instance.push = false;
	instance.pop = false;
	instance.reset = false;
	instance.error = false;
	instance.status = 0;
	instance.item = 0;
	instance.stack[0] = 0;
	instance.stack[1] = 0;
	instance.stack[2] = 0;
	instance.stack[3] = 0;
	instance.top = -1;
	instance.min_index = 0;
	instance.i = 0;
	instance.temp_min = 0;
	EoC = false;
	BoC = false;
	
	VerificationLoop();
}

