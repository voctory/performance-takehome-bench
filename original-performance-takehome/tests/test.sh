#!/usr/bin/env bash
set -euo pipefail

# Always generate a reward file; Harbor reads /logs/verifier/reward.txt.
python3 /tests/verify.py || true

if [ ! -f /logs/verifier/reward.txt ]; then
  echo 0 > /logs/verifier/reward.txt
fi

