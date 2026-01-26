#!/usr/bin/env python3
"""Minimal wrapper to run lib/test-e2e/stress_test_v2.py.

Goals:
- Single CLI (no subcommands) with defaults + overrides
- Optional parallelism via -j/--parallel (accepts 1)
- Robust paths (do not depend on user CWD)
- Minimal, stable output
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def _repo_root(script_dir: Path) -> Path:
    # .../lib/test-e2e -> .../
    return script_dir.parents[1]


def _build_cmd(stress_test_script: Path, num_tests: int, extra_args: list[str]) -> list[str]:
    return [
        sys.executable,
        str(stress_test_script),
        "-n",
        str(num_tests),
        *extra_args,
    ]


def _run_processes(
    *,
    stress_test_script: Path,
    cwd: Path,
    num_tests: int,
    parallel: int,
    extra_args: list[str],
) -> tuple[int, int, int]:
    workers = max(1, parallel)
    workers = min(workers, num_tests)

    tests_per_worker = num_tests // workers
    if tests_per_worker < 1:
        tests_per_worker = 1
        workers = num_tests

    effective_tests = tests_per_worker * workers

    procs: list[tuple[int, subprocess.Popen[bytes]]]
    procs = []

    # In parallel mode, suppress child output to keep logs readable.
    devnull = subprocess.DEVNULL if workers > 1 else None

    for i in range(workers):
        cmd = _build_cmd(stress_test_script, tests_per_worker, extra_args)
        procs.append(
            (
                i + 1,
                subprocess.Popen(cmd, cwd=str(cwd), stdout=devnull, stderr=devnull),
            )
        )

    failed = False
    for proc_id, p in procs:
        rc = p.wait()
        if rc != 0:
            failed = True
            print(f"process {proc_id} failed (exit {rc})")

    return (1 if failed else 0), workers, effective_tests


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="test_runner.py",
        description="Wrapper minimale per eseguire lib/test-e2e/stress_test_v2.py",
    )

    parser.add_argument(
        "-n",
        "--num-tests",
        type=int,
        default=10,
        help="Numero di test da eseguire (default: 10)",
    )
    parser.add_argument(
        "-j",
        "--parallel",
        type=int,
        default=1,
        help="Numero di processi paralleli (default: 1)",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=120,
        help="FPS del gioco (default: 120)",
    )
    parser.add_argument(
        "--max-turns",
        type=int,
        default=500,
        help="Numero massimo di turni per partita (default: 500)",
    )
    parser.add_argument(
        "--event",
        type=str,
        default=None,
        help="Pattern evento da testare (es. 'color_*.png')",
    )

    args = parser.parse_args()

    if args.num_tests < 1:
        parser.error("--num-tests deve essere >= 1")
    if args.parallel < 1:
        parser.error("--parallel deve essere >= 1")
    if args.fps < 1:
        parser.error("--fps deve essere >= 1")
    if args.max_turns < 1:
        parser.error("--max-turns deve essere >= 1")

    script_dir = Path(__file__).resolve().parent
    repo_root = _repo_root(script_dir)
    stress_test_script = (script_dir / "stress_test_v2.py").resolve()

    if not stress_test_script.exists():
        print(f"missing script: {stress_test_script}")
        raise SystemExit(1)

    extra_args: list[str] = [
        "--fps",
        str(args.fps),
        "--max-turns",
        str(args.max_turns),
    ]
    if args.event:
        extra_args.extend(["--event", args.event])

    cmd_summary = f"n={args.num_tests} j={args.parallel} fps={args.fps} max_turns={args.max_turns}"
    if args.event:
        cmd_summary += f" event={args.event}"
    print(cmd_summary)

    rc, workers, effective_tests = _run_processes(
        stress_test_script=stress_test_script,
        cwd=repo_root,
        num_tests=args.num_tests,
        parallel=args.parallel,
        extra_args=extra_args,
    )

    if rc == 0:
        suffix = "" if effective_tests == args.num_tests else f" (ran {effective_tests}/{args.num_tests})"
        print(f"ok{suffix}")
    raise SystemExit(rc)


if __name__ == "__main__":
    main()
