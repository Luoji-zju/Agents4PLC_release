# Multi-Agent ST Code Generation Demo Logs

This directory contains two representative workflow logs demonstrating the capabilities and limitations of our multi-agent system for generating and verifying Structured Text (ST) code for industrial PLC applications.

## Case 211: `StackMin` – Direct Success

- **Problem**: Implement a stack that removes the *minimum* element (not the top) on `pop`.
- **Outcome**: The system generated correct code in a single pass.
- **Verification**: All 6 formal properties (including error/status consistency and boundary conditions) passed immediately.
- **Takeaway**: Demonstrates a clean, end-to-end success of the retrieval → planning → coding → verification pipeline.

## Case 213: `MultiPumpCtrl` – Verification Feedback Loop Failure

- **Problem**: Priority-based pump control with manual/auto modes and stop-signal override.
- **Outcome**: The initial code failed formal verification. The debugging agent attempted two patches based on counterexamples.
- **Issue**: The formal verifier encountered **state explosion** (not explicitly shown, but inferred from persistent failures despite seemingly correct patches), leading the agent to misdiagnose the root cause. Subsequent patches introduced logical inconsistencies (e.g., inverted stop condition, duplicated logic).
- **Silver Lining**: The syntax-level patching mechanism worked correctly—patches were applied as intended. The failure stems from **semantic misinterpretation** under incomplete verification feedback, not tooling.
- **Takeaway**: Highlights a current limitation: when formal verification cannot provide precise counterexamples (e.g., due to state-space explosion), the agent may "overfit" to partial diagnostics and degrade correctness.

---

These cases illustrate both the promise and the challenges of integrating formal methods into autonomous code generation workflows.