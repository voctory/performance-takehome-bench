from __future__ import annotations

import os
import sys
from dataclasses import dataclass

# Ensure we import the candidate's code from /app.
sys.path.insert(0, "/app")

from frozen_problem import (  # noqa: E402
    Machine,
    build_mem_image,
    reference_kernel2,
    Tree,
    Input,
    N_CORES,
)
from perf_takehome import KernelBuilder  # noqa: E402


THRESHOLDS = [
    147734,  # baseline
    18532,  # updated starting point
    2164,  # opus4 many hours
    1790,  # opus4.5 casual
    1579,  # opus4.5 2hr
    1548,  # sonnet4.5 many hours
    1487,  # opus4.5 11.5hr
    1363,  # opus4.5 improved harness
]


@dataclass(frozen=True)
class VerifyResult:
    ok: bool
    cycles: int | None = None
    reward: float = -1.0
    error: str | None = None


def _write_reward(reward: float) -> None:
    os.makedirs("/logs/verifier", exist_ok=True)
    with open("/logs/verifier/reward.txt", "w", encoding="utf-8") as f:
        f.write(str(float(reward)))


def run_once() -> VerifyResult:
    forest_height = 10
    rounds = 16
    batch_size = 256

    forest = Tree.generate(forest_height)
    inp = Input.generate(forest, batch_size, rounds)
    mem = build_mem_image(forest, inp)

    kb = KernelBuilder()
    kb.build_kernel(forest.height, len(forest.values), len(inp.indices), rounds)

    machine = Machine(mem, kb.instrs, kb.debug_info(), n_cores=N_CORES)
    machine.enable_pause = False
    machine.enable_debug = False
    machine.run()

    final_ref_mem = None
    for final_ref_mem in reference_kernel2(mem, {}):
        pass
    if final_ref_mem is None:
        return VerifyResult(ok=False, error="reference_kernel2 yielded nothing")

    inp_values_p = final_ref_mem[6]
    expected = final_ref_mem[inp_values_p : inp_values_p + batch_size]
    got = machine.mem[inp_values_p : inp_values_p + batch_size]
    if got != expected:
        return VerifyResult(ok=False, cycles=machine.cycle, reward=-1.0, error="incorrect output values")

    stages = sum(1 for t in THRESHOLDS if machine.cycle < t)
    return VerifyResult(ok=True, cycles=machine.cycle, reward=float(stages))


def main() -> int:
    # Always overwrite any pre-existing reward set by the agent.
    _write_reward(0.0)

    try:
        res = run_once()
    except Exception as e:  # noqa: BLE001
        _write_reward(-1.0)
        print(f"[verify] exception: {e}")
        return 0

    _write_reward(res.reward)
    if res.cycles is not None:
        os.makedirs("/logs/verifier", exist_ok=True)
        with open("/logs/verifier/cycles.txt", "w", encoding="utf-8") as f:
            f.write(str(res.cycles))

    if res.ok:
        print(f"[verify] ok cycles={res.cycles} reward={res.reward}")
    else:
        print(f"[verify] fail cycles={res.cycles} reward={res.reward} error={res.error}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

