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
	int32_t latency_xx_ms;
	uint32_t NODE_xx_STATUS;
	int32_t errors_xx;
	int32_t errors_all;
	int32_t min_latency_ms;
	int32_t max_latency_ms;
} __LatencyMonitor;

// Global variables
__LatencyMonitor instance;
bool EoC;
bool BoC;
bool __cbmc_boc_marker;
bool __cbmc_eoc_marker;

// Automata declarations
void LatencyMonitor(__LatencyMonitor *__context);
void VerificationLoop();

// Automata
void LatencyMonitor(__LatencyMonitor *__context) {
	// Temporary variables
	
	// Start with initial location
	goto init;
	init: {
		if ((__context->errors_xx < 0)) {
			__context->errors_xx = 0;
			goto l4;
		}
		if ((! (__context->errors_xx < 0))) {
			goto l4;
		}
		//assert(false);
		return;  			}
	l4: {
		if ((__context->errors_all < 0)) {
			__context->errors_all = 0;
			goto l8;
		}
		if ((! (__context->errors_all < 0))) {
			goto l8;
		}
		//assert(false);
		return;  			}
	l8: {
		if ((__context->min_latency_ms < 0)) {
			__context->min_latency_ms = 2147483647;
			goto l12;
		}
		if ((! (__context->min_latency_ms < 0))) {
			goto l12;
		}
		//assert(false);
		return;  			}
	l12: {
		if ((__context->max_latency_ms < 0)) {
			__context->max_latency_ms = -2147483648;
			goto l16;
		}
		if ((! (__context->max_latency_ms < 0))) {
			goto l16;
		}
		//assert(false);
		return;  			}
	l16: {
		if (((__context->latency_xx_ms == 0) || (__context->NODE_xx_STATUS != 1))) {
			__context->errors_xx = (__context->errors_xx + 1);
			__context->errors_all = (__context->errors_all + 1);
			goto l21;
		}
		if ((! ((__context->latency_xx_ms == 0) || (__context->NODE_xx_STATUS != 1)))) {
			goto l21;
		}
		//assert(false);
		return;  			}
	l21: {
		if ((__context->latency_xx_ms < __context->min_latency_ms)) {
			__context->min_latency_ms = __context->latency_xx_ms;
			goto l25;
		}
		if ((! (__context->latency_xx_ms < __context->min_latency_ms))) {
			goto l25;
		}
		//assert(false);
		return;  			}
	l25: {
		if ((__context->latency_xx_ms > __context->max_latency_ms)) {
			__context->max_latency_ms = __context->latency_xx_ms;
			goto l29;
		}
		if ((! (__context->latency_xx_ms > __context->max_latency_ms))) {
			goto l29;
		}
		//assert(false);
		return;  			}
	l29: {
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
			LatencyMonitor(&instance);
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
		assert((!((BoC && (((instance.latency_xx_ms == 0) || (instance.NODE_xx_STATUS != 1)) && (instance.errors_xx == 0)))) || (A[(! EoC) U (EoC && (instance.errors_xx == 1))])));
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
	instance.latency_xx_ms = 0;
	instance.NODE_xx_STATUS = 0;
	instance.errors_xx = 0;
	instance.errors_all = 0;
	instance.min_latency_ms = 0;
	instance.max_latency_ms = 0;
	EoC = false;
	BoC = false;
	
	VerificationLoop();
}

