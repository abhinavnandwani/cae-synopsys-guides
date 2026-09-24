# CAE validation record

Maintained by Abhinav Nandwani. Tested on 23 September 2026.

## Environment and observed results

Simulation and synthesis completed on CAE linux-2613. Interactive walkthroughs
and physical exercises were checked on linux-2015 using the shared home.
The original teaching workspace was `~/siliconbadgers-cae-lab-20260923`.
That historical path remains visible in the original screenshots.

- VCS Y-2026.03_Full64 compiled and ran the passing register test, wrote FSDB
  and coverage, and detected an intentionally injected stuck-at-zero error.
  The fatal returned raw exit zero on this environment, so the runner also
  checks diagnostics and pass markers.
- Verdi Y-2026.03 displayed source, hierarchy, and the four signals over
  0 to 31 ns. Signal selection, cursor interpretation, Zoom All, and Save
  Signal were checked.
- URG Y-2026.03's dashboard, hierarchy, and DUT module pages were opened.
  DUT line and branch coverage were 100%; toggle coverage was 87.5% because
  reset was not reasserted. Dashboard totals also include UVM and testbench code.
- Design Compiler and Design Vision Y-2026.03 produced and opened a mapped
  netlist, DDC, SDC, and reports. Schematic expansion and the timing-report
  GUI were exercised. Teaching cell area was 7.116032; the displayed setup
  path had 8.86 ns slack under the exercise constraints.
- ICC2 Library Manager X-2025.06-SP3 imported installed EDK technology, DB,
  and LEF, passed `check_workspace`, and created a teaching NDM on CAE.
- ICC2 X-2025.06-SP3 linked the netlist, read the constraints, initialized a
  floorplan, performed initial placement, and saved the design library/block.
  `q_reg` had origin `8.0387 8.7512` and `physical_status placed`. The GUI
  showed matching properties. The saved block reopened successfully.

## What the example establishes

This is a one-register teaching flow. It establishes access and shows how to
inspect source, simulation, coverage, mapped logic, timing, and initial
physical placement. UVM 1.2 is imported as an availability check; the testbench
is procedural, not a full class-based UVM environment.

Physical placement is not a complete P&R or signoff flow. Power planning,
final pin planning, detailed legalization, clock-tree work, routing, extraction,
and signoff remain. The PD guide explains the observed library warnings.
The installed SAED32 RVT library is a teaching default, not a project process
selection or an accelerator PPA estimate.

## Document editions

The PDF, Word, and web editions use the Markdown files in `manuscripts/`,
including the shared access instructions in `common-access.md`. The repository
README describes how to rebuild them.

Screenshots are real native-resolution captures. The original image files are
unchanged; cropping is applied in the document or webpage layout. Captures are
1237 by 793 pixels. The Apps-menu excerpt is displayed at a modest size.

All 32 rendered pages were reviewed for layout. The common login and terminal
pages match across guides; companion source links vary by guide. The PDFs
include direct links to the companion code, with full URLs rendered blue and
underlined.
PDF and Word author metadata both identify Abhinav Nandwani.
