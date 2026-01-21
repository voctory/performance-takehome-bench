Optimize the kernel in `/app/perf_takehome.py` (`KernelBuilder.build_kernel`) to minimize simulated cycle count while preserving correctness.

The verifier runs a frozen simulator and checks:
- Correct output values for `forest_height=10`, `rounds=16`, `batch_size=256`
- Cycle-count thresholds (reward increases as you beat more thresholds)

Notes:
- Only edits under `/app` matter (the simulator + reference are provided by the verifier after the agent finishes).
- The cycle count is measured by the simulator (`Machine.cycle`), not Python runtime.

