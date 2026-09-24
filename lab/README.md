# CAE Synopsys teaching examples

By Abhinav Nandwani

These exercises use a single register to check access and explain the tools.

In a CAE terminal, from the exercise directory:

```sh
cd ~/cae-synopsys-guides/lab
module load synopsys/suite
synopsys-run
python3 run_lab.py simulation
python3 run_lab.py synthesis
```

Each run prints its directory and `LAB_RESULT=PASS` or `LAB_RESULT=FAIL`.
Use the printed simulation directory to open the waveform in Verdi:

```sh
cd runs/<your-simulation-run-directory>
verdi -ssf smoke.fsdb
```

The simulation includes a separate intentionally failing run. It forces the
register output to zero; the test must reject it with a fatal `data failed`
diagnostic and no pass marker. VCS returned zero even for this fatal in the
tested CAE environment, so the runner checks the log as well as the process
exit code. Its files are isolated in `negative/`.

The synthesis example uses the installed SAED32 RVT TT 1.05 V / 25 C library.
You can set `SB_TARGET_LIBRARY` inside the container to use another installed
timing library `.db`.
Do not commit or distribute licensed libraries or tool binaries.

Exit the container with `exit`. Save work and log out of the Linux desktop
using the desktop menu when finished.

## Physical inspection exercise

After a successful synthesis run, keep its directory path. Inside the container:

```sh
SB_LAB="$HOME/cae-synopsys-guides/lab"
export SB_SYNTH_RUN="$SB_LAB/runs/YOUR_SYNTHESIS_RUN"
SB_PHYS=$(mktemp -d "$SB_LAB/runs/physical-XXXXXX")
cd "$SB_PHYS"
icc2_lm_shell -f "$SB_LAB/physical/build_reference.tcl" > library.log 2>&1
```

Replace `YOUR_SYNTHESIS_RUN`, then inspect `library.log`. Require a successful
workspace check and `sb_rvt.ndm`. Preserve and review the library warnings.
Continue only when import succeeded:

```sh
icc2_shell -f "$SB_LAB/physical/floorplan.tcl" > floorplan.log 2>&1
```

Inspect the whole log for errors, the saved design library, and register origin
and physical status. This is an initial floorplan placement of one register,
not a legalized, clocked, routed or signoff-clean physical implementation.
The NDM generated from installed EDK data stays on CAE and is not included here.

To inspect the saved result, start `icc2_shell` in that physical run directory
and enter `open_lib sb_flop.dlib`, `open_block sb_flop`, and `start_gui`.
See the PD handout for layout, property, and diagnostic inspection steps.
