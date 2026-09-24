#!/usr/bin/env python3
"""Run the CAE teaching example inside the Synopsys container.

Each invocation has a fresh run directory. Only the small example is run.
No shell profiles, installed tools, licensed libraries or team repos are edited.
"""
import argparse
import datetime
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
LIBRARY = "/srv/auto/apps/saed32_edk/2023/lib/stdcell_rvt/SAED32_EDK/lib/stdcell_rvt/db_nldm/saed32rvt_tt1p05v25c.db"
parser = argparse.ArgumentParser()
parser.add_argument("lab", choices=["simulation", "synthesis"])
args = parser.parse_args()
run = ROOT / "runs" / (args.lab + "-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f"))
run.mkdir(parents=True)
records = []

def execute(name, command, cwd=run, expected_failure=False):
    started = time.monotonic()
    with (cwd / (name + ".log")).open("w") as log:
        proc = subprocess.Popen(command, cwd=cwd, stdout=log, stderr=subprocess.STDOUT,
                                start_new_session=True)
        try:
            code = proc.wait(timeout=180)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGTERM)
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait()
            raise RuntimeError(name + " exceeded 180 seconds; inspect " + str(cwd / (name + ".log")))
    output = (cwd / (name + ".log")).read_text(errors="replace")
    records.append(dict(step=name, command=command, cwd=str(cwd), exit_code=code,
                        elapsed_seconds=round(time.monotonic()-started, 2)))
    print(name + ": exit " + str(code), flush=True)
    if expected_failure:
        if "Fatal:" not in output or "data failed" not in output or "SB_SNPS_SIM_PASS" in output:
            raise RuntimeError("Expected stuck-at-zero failure was not detected")
        print("Expected fatal diagnostic detected (raw exit code is not the verdict)", flush=True)
    elif code != 0 or re.search(r"^(?:Error|Fatal)(?:\s|:|\[)", output, re.M):
        raise RuntimeError(name + " failed; inspect its log")
    return output

try:
    if args.lab == "simulation":
        verdi = shutil.which("verdi")
        if not verdi:
            raise RuntimeError("Load synopsys/suite and enter synopsys-run first")
        os.environ["VERDI_HOME"] = str(Path(verdi).parent.parent)
        execute("compile", ["vcs", "-full64", "-sverilog", "-timescale=1ns/1ps",
                "-ntb_opts", "uvm-1.2", "-debug_access+all", "-kdb",
                "-cm", "line+cond+tgl+branch+assert",
                str(ROOT / "rtl/sb_flop.v"), str(ROOT / "tb/tb.sv"), "-top", "tb", "-o", "simv"])
        output = execute("simulate", ["./simv", "-cm", "line+cond+tgl+branch+assert"])
        if "SB_SNPS_SIM_PASS" not in output or not (run / "smoke.fsdb").stat().st_size:
            raise RuntimeError("Missing simulation pass marker or waveform")
        execute("coverage", ["urg", "-full64", "-dir", "simv.vdb", "-report", "coverage_report"])
        negative = run / "negative"
        negative.mkdir()
        execute("expected_failure", [str(run / "simv"), "+INJECT_FAILURE"],
                cwd=negative, expected_failure=True)
    else:
        os.environ.setdefault("SB_TARGET_LIBRARY", LIBRARY)
        os.environ["SB_RTL"] = str(ROOT / "rtl/sb_flop.v")
        if not Path(os.environ["SB_TARGET_LIBRARY"]).is_file():
            raise RuntimeError("Teaching library not found; set SB_TARGET_LIBRARY to an approved .db")
        output = execute("synthesis", ["dc_shell", "-f", str(ROOT / "synth/run.tcl")])
        required = ["mapped.v", "mapped.ddc", "constraints.sdc", "area.rpt", "timing.rpt"]
        if "SB_SNPS_SYNTH_DONE" not in output or not all((run/p).stat().st_size for p in required):
            raise RuntimeError("Missing synthesis completion marker or output")
    result = "PASS"
except Exception as exc:
    result = "FAIL"
    print(str(exc), file=sys.stderr)
finally:
    (run / "result.json").write_text(json.dumps(dict(result=result, lab=args.lab,
        run_directory=str(run), steps=records), indent=2) + "\n")
    print("RUN_DIRECTORY=" + str(run))
    print("LAB_RESULT=" + result)
sys.exit(0 if result == "PASS" else 1)
