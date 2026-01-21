# Performance Takehome (Harbor Task)

This repo packages Anthropic's original performance take-home as a single [Harbor](https://github.com/laude-institute/harbor) task.

Upstream source: https://github.com/anthropics/original_performance_takehome

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
