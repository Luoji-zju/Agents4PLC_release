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
	int16_t a;
	int16_t b;
	int16_t max_value;
} __USER_MAX;
typedef struct {
	int16_t a;
	int16_t b;
	int16_t min_value;
} __USER_MIN;
typedef struct {
	int16_t input1;
	int16_t input2;
	int16_t input3;
	int16_t input4;
	int16_t input5;
	int16_t CYCLE;
	int16_t M;
	int16_t N;
	int16_t UPDATED_CYCLE;
	int16_t TEMP_MAX_OUT;
	int16_t TEMP_MIN_2_OUT;
	int16_t TEMP_MIN_3_OUT;
	__USER_MAX user_max;
	__USER_MIN user_min;
} __FB_ValueComparison;

// Global variables
__FB_ValueComparison instance;
bool EoC;
bool BoC;
bool __cbmc_boc_marker;
bool __cbmc_eoc_marker;

// Automata declarations
void USER_MAX(__USER_MAX *__context);
void USER_MIN(__USER_MIN *__context);
void FB_ValueComparison(__FB_ValueComparison *__context);
void VerificationLoop();

// Automata
void USER_MAX(__USER_MAX *__context) {
	// Temporary variables
	
	// Start with initial location
	goto init;
	init: {
			__context->max_value = __context->a;
			goto l1;
		//assert(false);
		return;  			}
	l1: {
		if ((__context->b > __context->a)) {
			__context->max_value = __context->b;
			goto l5;
		}
		if ((! (__context->b > __context->a))) {
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
void USER_MIN(__USER_MIN *__context) {
	// Temporary variables
	
	// Start with initial location
	goto init1;
	init1: {
			__context->min_value = __context->a;
			goto l11;
		//assert(false);
		return;  			}
	l11: {
		if ((__context->b < __context->a)) {
			__context->min_value = __context->b;
			goto l51;
		}
		if ((! (__context->b < __context->a))) {
			goto l51;
		}
		//assert(false);
		return;  			}
	l51: {
		goto __end_of_automaton;
		//assert(false);
		return;  			}
	
	// End of automaton
	__end_of_automaton: ;
}
void FB_ValueComparison(__FB_ValueComparison *__context) {
	// Temporary variables
	
	// Start with initial location
	goto init2;
	init2: {
			// Assign inputs
			__context->user_max.a = __context->input2;
			__context->user_max.b = __context->input3;
			USER_MAX(&__context->user_max);
			// Assign outputs
			goto l12;
		//assert(false);
		return;  			}
	l12: {
			__context->TEMP_MAX_OUT = __context->user_max.max_value;
			goto l2;
		//assert(false);
		return;  			}
	l2: {
			// Assign inputs
			__context->user_max.a = __context->input1;
			__context->user_max.b = __context->TEMP_MAX_OUT;
			USER_MAX(&__context->user_max);
			// Assign outputs
			goto l3;
		//assert(false);
		return;  			}
	l3: {
			__context->M = __context->user_max.max_value;
			goto l4;
		//assert(false);
		return;  			}
	l4: {
			// Assign inputs
			__context->user_min.a = __context->input4;
			__context->user_min.b = __context->input5;
			USER_MIN(&__context->user_min);
			// Assign outputs
			goto l52;
		//assert(false);
		return;  			}
	l52: {
			__context->TEMP_MIN_2_OUT = __context->user_min.min_value;
			goto l6;
		//assert(false);
		return;  			}
	l6: {
			// Assign inputs
			__context->user_min.a = __context->input2;
			__context->user_min.b = __context->input3;
			USER_MIN(&__context->user_min);
			// Assign outputs
			goto l7;
		//assert(false);
		return;  			}
	l7: {
			// Assign inputs
			__context->user_min.a = __context->user_min.min_value;
			__context->user_min.b = __context->TEMP_MIN_2_OUT;
			USER_MIN(&__context->user_min);
			// Assign outputs
			goto l8;
		//assert(false);
		return;  			}
	l8: {
			__context->TEMP_MIN_3_OUT = __context->user_min.min_value;
			goto l9;
		//assert(false);
		return;  			}
	l9: {
			// Assign inputs
			__context->user_min.a = __context->input1;
			__context->user_min.b = (__context->TEMP_MIN_3_OUT + __context->input3);
			USER_MIN(&__context->user_min);
			// Assign outputs
			goto l10;
		//assert(false);
		return;  			}
	l10: {
			__context->N = __context->user_min.min_value;
			__context->UPDATED_CYCLE = (__context->CYCLE + 1);
			goto l121;
		//assert(false);
		return;  			}
	l121: {
		goto __end_of_automaton;
		//assert(false);
		return;  			}
	
	// End of automaton
	__end_of_automaton: ;
}
void VerificationLoop() {
	// Temporary variables
	
	// Start with initial location
	goto init3;
	init3: {
			goto loop_start;
		//assert(false);
		return;  			}
	end: {
		goto __end_of_automaton;
		//assert(false);
		return;  			}
	loop_start: {
			instance.CYCLE = nondet_int16_t();
			instance.input1 = nondet_int16_t();
			instance.input2 = nondet_int16_t();
			instance.input3 = nondet_int16_t();
			instance.input4 = nondet_int16_t();
			instance.input5 = nondet_int16_t();
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
			FB_ValueComparison(&instance);
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
		assert((!((EoC && (instance.input1 <= (((instance.input3 * instance.input4) + instance.input5) + instance.input2)))) || (instance.N == instance.input1)));
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
	instance.input1 = 0;
	instance.input2 = 0;
	instance.input3 = 0;
	instance.input4 = 0;
	instance.input5 = 0;
	instance.CYCLE = 0;
	instance.M = 0;
	instance.N = 0;
	instance.UPDATED_CYCLE = 0;
	instance.TEMP_MAX_OUT = 0;
	instance.TEMP_MIN_2_OUT = 0;
	instance.TEMP_MIN_3_OUT = 0;
	instance.user_max.a = 0;
	instance.user_max.b = 0;
	instance.user_max.max_value = 0;
	instance.user_min.a = 0;
	instance.user_min.b = 0;
	instance.user_min.min_value = 0;
	EoC = false;
	BoC = false;
	
	VerificationLoop();
}

