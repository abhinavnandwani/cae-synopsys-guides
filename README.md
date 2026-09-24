# CAE Synopsys guides

By **Abhinav Nandwani**

Three visual guides for using the Synopsys tools on UW–Madison CAE Linux.
Each includes Guacamole login, terminal use, a runnable register example,
and detailed GUI walkthroughs with real screenshots.

| Guide | Read | Editable copy | Covers |
| --- | --- | --- | --- |
| Verification | [PDF](guides/cae-verification-handout.pdf) | [Word](guides/cae-verification-handout.docx) | VCS, passing and failing tests, Verdi, URG coverage |
| RTL | [PDF](guides/cae-rtl-handout.pdf) | [Word](guides/cae-rtl-handout.docx) | RTL interpretation, simulation, debugging, synthesis checks, Design Vision |
| Synthesis and physical design | [PDF](guides/cae-pd-handout.pdf) | [Word](guides/cae-pd-handout.docx) | Design Compiler, constraints, reference libraries, ICC2 floorplan and placement inspection |

Read the full guides online at
[Learning Resources: Synopsys on CAE](https://abhinavnandwani.com/learning/cae-synopsys/).
The website adds section links and copyable commands. Its pages and these PDFs
are generated from the same manuscripts in this repository.

## Example code

| File | Purpose |
| --- | --- |
| [sb_flop.v](lab/rtl/sb_flop.v) | One-bit register RTL |
| [tb.sv](lab/tb/tb.sv) | Passing test and injected failure |
| [run_lab.py](lab/run_lab.py) | Simulation, coverage, and synthesis runner |
| [run.tcl](lab/synth/run.tcl) | Synthesis and timing constraints |
| [build_reference.tcl](lab/physical/build_reference.tcl) | ICC2 reference library setup |
| [floorplan.tcl](lab/physical/floorplan.tcl) | Physical import and initial placement |

See the [lab instructions](lab/README.md) for the run commands. Each guide covers
the CAE environment and the relevant terminal and GUI workflow.

## Contents

- `guides/`: reading PDFs and editable Word copies.
- `lab/`: the shared RTL, testbench, runner, synthesis and physical-design scripts.
- `manuscripts/`: Markdown sources with shared access instructions.
- `assets/`: original screenshots used in the guides.
- `build_guides.py` and `build_handouts.py`: document generation.
- [VALIDATION.md](VALIDATION.md): versions, observed results, and flow limits.

The example exercises were tested on CAE on 23 September 2026. The screenshots
retain the original dated demonstration paths; use the paths in
the command blocks. The RTL identifiers and result markers are unchanged so
they continue to match the validated logs and screenshots.

## Rebuild the documents

Reading the PDFs or running the lab does not require the document dependencies.
To edit the guides, install Python 3.10 or newer and LibreOffice, then run:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-docs.txt
python3 build_guides.py
soffice --headless --convert-to pdf --outdir guides guides/*.docx
```

`soffice` must be on your PATH. On macOS, the executable is commonly inside
`/Applications/LibreOffice.app/Contents/MacOS/`. Generated Markdown stays in
`.build/`; final DOCX and PDF files go in `guides/`. Review every rendered page
after editing, including link appearance and destinations.

The website renderer lives in
[`abhinavnandwani.github.io/scripts/build_learning.py`](https://github.com/abhinavnandwani/abhinavnandwani.github.io/blob/master/scripts/build_learning.py).
After updating the manuscripts and rebuilding the PDFs, run that renderer with
`--source` pointing at this repository. It copies the published PDFs and original
screenshots and records source hashes so the web and offline editions can be
checked together. Do not edit the generated website guide text separately.
