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

## Get the lab onto CAE

Open [CAE Guacamole](https://guacamole.cae.wisc.edu), complete the UW web
sign-in and the second Linux login, then open **Apps → Terminal**.
The guides explain both login stages in detail.

In the CAE **host terminal**, before entering the Synopsys container:

```sh
cd ~
git clone https://github.com/abhinavnandwani/cae-synopsys-guides.git
cd cae-synopsys-guides/lab
module load synopsys/suite
synopsys-run
```

Inside the container, run the exercise for your guide:

```sh
cd ~/cae-synopsys-guides/lab
python3 run_lab.py simulation
python3 run_lab.py synthesis
```

Follow the PDF for interpreting the output and opening the GUI. Physical design
has additional steps in its guide and the [lab README](lab/README.md).
The tools and licenses come from CAE, so running these commands on a laptop
without the CAE environment will not run the lab.

### Laptop transfer alternative

If cloning directly on CAE is unavailable, clone on your laptop, then copy it:

```sh
git clone https://github.com/abhinavnandwani/cae-synopsys-guides.git
scp -r cae-synopsys-guides YOUR_NETID@best-tux.cae.wisc.edu:~/
```

Replace `YOUR_NETID`. Verify a new host key against the
[CAE SSH fingerprint](https://kb.wisc.edu/moodle/162780).
You can also use GitHub's **Code → Download ZIP**. Extract the ZIP and rename
the resulting folder to `cae-synopsys-guides` before using the SCP command.
Guacamole's CAE deployment does not provide file transfer.

## Get later updates

For a Git clone, return to the CAE host shell and run:

```sh
cd ~/cae-synopsys-guides
git status
git pull --ff-only
```

Run outputs are ignored by Git. If you edited the teaching source, save your
work on a branch and commit it before updating. If Git reports a conflict,
stop and resolve it; do not delete your changes. A ZIP download has no Git
history, so download a fresh copy into a separate folder for an updated version.

## Contents

- `guides/`: reading PDFs and editable Word copies.
- `lab/`: the shared RTL, testbench, runner, synthesis and physical-design scripts.
- `manuscripts/`: Markdown sources with shared access instructions.
- `assets/`: original screenshots used in the guides.
- `build_guides.py` and `build_handouts.py`: document generation.
- [VALIDATION.md](VALIDATION.md): versions, observed results, and flow limits.

The example exercises were tested on CAE on 23 September 2026. The screenshots
retain the original dated demonstration paths; use the current clone paths in
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
`--source` pointing at this clone. It copies the published PDFs and original
screenshots and records source hashes so the web and offline editions can be
checked together. Do not edit the generated website guide text separately.

The initial import includes previously prepared AI-assisted guides and code.
Their original creation predates this repository's Git history; the import
does not claim retroactive line-level attribution.

## Sharing with the club

Maintain one canonical repository under Abhinav Nandwani's account. Share its
README and the relevant guide link with each team. Club repositories can link
here instead of copying the PDFs and lab into each repository. Members can
read the PDF online, download it, or clone everything once and pull updates.

Only the authored guides, screenshots, and teaching sources belong here.
Generated tool runs, library databases, NDMs, and licensed tool files stay on CAE.
