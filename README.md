# Performance Takehome (Harbor Task)

This repo packages Anthropic's original performance take-home as a single [Harbor](https://github.com/laude-institute/harbor) task.

Upstream source: https://github.com/anthropics/original_performance_takehome

Default timeouts: 2 hours (agent) + 2 hours (verifier).

## Install Harbor

```bash
uv tool install harbor
# or
pip install harbor
```

## Run (local checkout)

```bash
git clone https://github.com/voctory/performance-takehome-bench.git
cd performance-takehome-bench

harbor run --path . --agent oracle --n-concurrent 1 -k 1
```

## Run (no checkout; Harbor pulls from Git)

```bash
harbor trials start \
  --task-git-url https://github.com/voctory/performance-takehome-bench.git \
  --path original-performance-takehome \
  --agent oracle
```

## Timeouts

The task defaults to 2 hours for both the agent and verifier. You can scale these with `--timeout-multiplier`:

```bash
# Example: give 4 hours total (2h * 2.0) for agent+verifier timeouts
harbor run --path . --agent oracle --n-concurrent 1 -k 1 --timeout-multiplier 2.0
```
