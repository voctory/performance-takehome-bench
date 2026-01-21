FROM python:3.11-slim-bookworm

WORKDIR /app

RUN apt-get update -y && apt-get install -y --no-install-recommends bash git ca-certificates && rm -rf /var/lib/apt/lists/*

# Baseline starter code (agents modify files in /app).
COPY perf_takehome.py /app/perf_takehome.py
COPY problem.py /app/problem.py
COPY watch_trace.py /app/watch_trace.py
COPY watch_trace.html /app/watch_trace.html
COPY Readme.md /app/Readme.md

