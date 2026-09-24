# Verification on CAE
By Abhinav Nandwani

Use this guide to compile a SystemVerilog test, inspect its source and waveforms, generate coverage, and prove that the test catches a known bug. The terminal and GUI sections use the same small register example. The final section connects this workflow to the team's test plan and verification scaffolding.

{{ACCESS}}

<!-- page -->
## Run the verification exercise from the terminal
Inside the Synopsys container, start from the companion folder:

```bash
cd ~/cae-synopsys-guides/lab
python3 run_lab.py simulation
```

The runner creates a new directory under `runs/` for every invocation. It compiles the design, executes a passing simulation, builds a coverage report, and executes a separate intentionally failing simulation. The final `LAB_RESULT=PASS` means these checks behaved as expected, including detection of the deliberate failure.

![The saved passing log contains the UVM access message and SB_SNPS_SIM_PASS.](v2-simulation-pass.png|6.5)

| File in the printed run directory | How to use it |
| --- | --- |
| `compile.log` | Start here for syntax, missing include, package, and elaboration errors. |
| `simulate.log` | Inspect test diagnostics, simulation time, and the pass marker. |
| `simv` | The compiled simulation executable for this build. |
| `smoke.fsdb` | Waveform data for the passing run. |
| `simv.vdb` | Collected coverage data. |
| `coverage_report/` | URG's HTML coverage report. |
| `negative/expected_failure.log` | Evidence that the injected fault was detected. |
| `result.json` | Exact commands, working directories, elapsed time, raw exit codes, and verdict. |

Change into the exact run directory the runner printed. Do not guess that an older directory is the latest run. Inspect `result.json` and the logs even when the final result says PASS. A working test harness and a correct design are separate questions.

<!-- page -->
## Understand and reproduce the terminal commands
The example has `rtl/sb_flop.v` and `tb/tb.sv`. The testbench instantiates the register, drives a 10 ns clock, checks reset, checks captured data, and writes an FSDB. UVM 1.2 is imported to check that the installed integration works; this example is a procedural testbench, not a complete class-based UVM environment.

To run the commands directly, create a separate manual run directory first:

```bash
SB_LAB="$HOME/cae-synopsys-guides/lab"
SB_RUN=$(mktemp -d "$SB_LAB/runs/manual-sim-XXXXXX")
cd "$SB_RUN"
export VERDI_HOME="$(dirname "$(dirname "$(command -v verdi)")")"
vcs -full64 -sverilog -timescale=1ns/1ps \
  -ntb_opts uvm-1.2 -debug_access+all -kdb \
  -cm line+cond+tgl+branch+assert \
  "$SB_LAB/rtl/sb_flop.v" "$SB_LAB/tb/tb.sv" \
  -top tb -o simv > compile.log 2>&1
echo $?
./simv -cm line+cond+tgl+branch+assert > simulate.log 2>&1
grep -nE 'Error|Fatal|SB_SNPS_SIM_PASS' simulate.log
urg -full64 -dir simv.vdb -report coverage_report \
  > coverage.log 2>&1
```

Stop after compilation if it fails. The shell does not automatically stop this sequence for you. The supplied Python runner is preferable for repeatable runs because it checks diagnostics and required outputs and gives each command a 180-second limit.

`-full64` selects the working 64-bit VCS mode on this installation. `-sverilog` enables SystemVerilog parsing. `-top tb` selects the testbench top. `-debug_access+all -kdb` retains information needed for source-level debugging. The `-cm` options enable the listed coverage types; they do not create missing assertions or functional coverage goals.

## Inspect the test before trusting it
Read the checks in `tb/tb.sv`. At 11 ns the test checks the reset value and drives one onto `d`. It checks `q` at 21 ns, then drives zero. It checks again at 31 ns. These checks occur after the relevant rising edge so the nonblocking assignment has completed. A real interface test should define its sampling convention just as explicitly.

<!-- page -->
## Open Verdi and navigate the design
From the passing simulation directory, launch the GUI inside Guacamole:

```bash
verdi -ssf smoke.fsdb
```

Keep that terminal available for launch diagnostics. Maximize Verdi by double-clicking its title bar. The hierarchy pane identifies instances; the source pane shows their code; the lower nWave pane displays recorded signal values.

![The passing test open in Verdi with its source and waveform panes.](v2-verdi-overview.png|6.5)

1. In the hierarchy pane, select `tb`. Expand it and select `dut` to inspect the instantiated `sb_flop` module. Confirm that you opened the intended source and top.
2. Return to `tb` to read the stimulus and checks alongside the RTL. Locate the clock generator, reset release, assignments to `d`, and `$fatal` checks.
3. In the lower nWave pane, choose Signal, then Get Signals. Select the `/tb` scope in the dialog.
4. Select `clk`, `rst`, `d`, and `q`. In the tested interface, selecting a signal and clicking Apply adds it to the waveform list. Repeat for the four signals, then click OK.
5. In nWave, choose View, then Zoom, then Zoom All. This displays the entire saved simulation rather than just its initial few nanoseconds.

If the source view is empty, first confirm that you launched from the run directory that contains the matching build data. Do not mix one build's debug database with another build's waveform. If the waveform list is empty, adding signals is still required even though the FSDB loaded successfully.

<!-- page -->
## Debug the waveform rather than just displaying it
Start with all four signals visible and the full 0 to 31 ns interval. The recorded view uses picoseconds on the ruler: 10000 ps is 10 ns. Signal values in the value column correspond to the current cursor position, not necessarily the end of the run.

![Clock, reset, data, and output shown over the complete saved test.](v2-verdi-waveform.png|6.5)

1. Click in the waveform near the first rising edge of `clk`. Follow the same vertical time position through `rst`, `d`, and `q`.
2. Move the time cursor before and after the edge. Before the first rising edge, `q` is unknown. At 5 ns, the asserted synchronous reset sets it to zero.
3. Inspect the reset release and data change at 11 ns. The output should not update immediately because the register samples on the next rising edge.
4. Inspect 15 ns. `q` captures one. Inspect 21 ns when `d` returns to zero, then 25 ns when `q` captures zero.
5. Use the nWave View, Zoom menu to inspect a smaller interval, then Zoom All to recover the overview. Keep the clock visible when investigating a data transition.

| Time | Expected observation |
| --- | --- |
| Before 5 ns | `q` is unknown; no active clock edge has applied reset yet. |
| 5 ns | `q` becomes zero while `rst` is high. |
| 11 ns | `rst` becomes zero and `d` becomes one. |
| 15 ns | `q` becomes one. |
| 21 ns | `d` becomes zero. |
| 25 ns | `q` becomes zero. |
| 31 ns | Final check completes and simulation ends. |

Write down the first time observed behavior differs from expected behavior. Then return to the source driving or sampling that signal. A waveform file existing proves only that recording worked; the test's checks and these transitions establish the example's behavior.

Save the signal arrangement with nWave File, Save Signal. Give the file a descriptive `.rc` name in the run directory. Use File, Restore Signal to load that arrangement in a later session with the matching FSDB. This saves a view configuration, not new simulation results. For readable screenshots, enlarge Monospaced Font under Tools, Preferences, General, Appearance.

<!-- page -->
## Investigate the deliberately failing run
The runner invokes the simulation again with `+INJECT_FAILURE` in a separate `negative/` directory. At 11 ns, the test forces the register output to zero. The expected one is therefore missing at the 21 ns check.

```bash
cat negative/expected_failure.log
verdi -ssf negative/smoke.fsdb
```

![The captured failing run stops at 21000 ps with the data failed diagnostic.](v2-failure.png|6.5)

In the failing waveform, add the same four signals. Confirm that `d` becomes one but `q` stays zero, then locate the failed check at 21 ns in the source. Compare against the passing run at 15 ns and 21 ns. A separate viewer is useful for comparing the two results; close each viewer when finished.

On the tested installation, VCS returned raw exit code zero even for this fatal diagnostic. The runner therefore requires the positive pass marker, rejects unexpected error or fatal diagnostics, and separately verifies that the deliberate failure reports `data failed` without the pass marker. Do not use exit zero as the only test verdict.

## Preserve both sides of the comparison
Keep the passing and failing logs and waveforms in their separate directories. Record the expected failure text and time. When adapting this pattern, inject a fault that violates a specific requirement and confirm that the intended checker catches it. A crash during compilation is not evidence that a behavioral checker works.

<!-- page -->
## Inspect coverage in the GUI
In the CAE desktop file manager, open the passing run's `coverage_report` folder and open `dashboard.html` with Firefox. Alternatively, in a CAE host terminal, run `firefox /absolute/path/to/coverage_report/dashboard.html`. This browser runs on CAE; the file is not on your laptop.

![URG's DUT page shows source coverage and the missing reset toggle.](v2-coverage.png|6.5)

1. On the dashboard, check the run date, tool version, command line, and test count. This example report contains one passing test; the deliberately failing run is separate.
2. Click hierarchy at the top. Expand `tb` if necessary, then click its `dut` child. The module page should identify `sb_flop` and the instance `tb.dut`.
3. Inspect Line and Branch. The tested DUT shows 100% for both. Match the covered source statements to the reset and data paths in the RTL.
4. Inspect Toggle and its Port Details table. The DUT reports 87.5% toggle coverage. `rst` has a falling transition but no rising transition because the test starts in reset and never reasserts it.
5. Compare the DUT with the dashboard totals. The totals also include testbench and imported UVM code. Always record the measured scope and metric with a percentage.

As a follow-on exercise, reassert reset after capturing data, check the resulting output at the appropriate clock edge, and regenerate the report in a fresh run. Confirm both the new behavior and the previously missing transition. Increasing coverage without a meaningful check is not sufficient.

Condition and assertion coverage do not have meaningful DUT targets in this tiny example. High code coverage does not establish arithmetic correctness, protocol behavior, corner cases, or interactions between units. The project test plan must connect requirements to stimulus, checks, and suitable coverage goals.

<!-- page -->
## Turn the exercise into verification infrastructure
For each project layer, specify the behavior to verify, reference model or expected result, stimulus, checks, coverage, and reproducible command. Decide where C++, SystemVerilog, UVM, or another method fits the layer. The availability of a UVM package does not by itself choose the methodology.

| What a runnable test should retain | Why it is needed |
| --- | --- |
| Source revision and source manifest | Identifies the exact implementation and test compiled. |
| Tool version and full commands | Makes setup and build differences diagnosable. |
| Seed and configuration when applicable | Reproduces randomized or configurable behavior. |
| Timeout and explicit verdict | Distinguishes a hang, a crash, and a failed check. |
| Logs, waveform, and coverage | Preserves evidence for debugging and review. |
| Known failing case | Shows that the checker rejects incorrect behavior. |

## Troubleshoot in a consistent order
If compilation fails, read the first relevant error before investigating later errors that may be consequences. Check the top module, source list, package and include order, and SystemVerilog flags. If simulation starts but no pass marker appears, inspect where it stops and whether the expected checker ran. If the GUI is blank, check the selected FSDB, scope, signal list, and matching build directory.

If a tool prints only a CAE launcher warning, return to the host shell and load the module before entering the container. For a license failure, retain the exact diagnostic and tool version. For an unresponsive GUI, first allow startup or loading to complete; do not repeatedly start duplicate copies that each consume resources.

## Completion check
Complete the passing and deliberately failing runs, explain the waveform at each expected edge, identify at least one coverage limitation, and show another teammate how to reproduce the run from its command and source revision. The team's project deliverables remain the architecture-based test plan, per-layer methodology proposal, and hardened runnable verification scaffolding.

Tested on CAE with VCS Y-2026.03_Full64, Verdi Y-2026.03, and URG Y-2026.03. Setup reference: https://kb.wisc.edu/cae-software-guide

Verdi overview: https://www.synopsys.com/verification/debug/verdi.html
