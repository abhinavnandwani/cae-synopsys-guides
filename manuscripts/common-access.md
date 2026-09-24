## Sign in to Guacamole
Guacamole displays a CAE Linux desktop in your browser. The tools run on the CAE machine. Use your own UW NetID and confirm that your account can reach CAE Linux services before the lab.

1. On your laptop, open https://guacamole.cae.wisc.edu in a browser.
2. Complete the UW web sign-in with your NetID and password, then complete MFA if requested.
3. At the Linux login screen, enter your UW NetID and password again. Use your NetID credentials at this second prompt too. The old separate CAE username and password are not the instructions for this service.
4. Wait for the Linux desktop. Open Apps in the upper-left corner and choose Terminal under Favorites. Maximize the terminal by double-clicking its title bar.
5. Keep the Guacamole tab open. A terminal inside this desktop is already on CAE; do not SSH back into CAE from it.

![Open Terminal from the CAE Apps menu.](02-apps-terminal.png|3.0)

If you already have an active session, the browser may reconnect without showing every login screen. If sign-in fails, record which prompt failed: UW web sign-in, MFA, or the Linux desktop login. These are different stages.

Official CAE login instructions and screenshots: https://kb.wisc.edu/cae/163323

<!-- page -->
## Enter the Synopsys environment
Run these commands in the CAE terminal, one line at a time. Do not type a prompt such as `$` or `synopsys>` before a command.

```bash
module load synopsys/suite
synopsys-run
command -v vcs dc_shell verdi icc2_shell pt_shell
```

The prompt becomes `synopsys>`. The module selects the site setup; the container provides the operating environment expected by the tools. Load the module before entering the container and repeat this setup for every new terminal used for Synopsys tools.

![Tool paths inside the working CAE Synopsys container.](v2-environment.png|6.5)

## Get the companion exercise onto CAE
On your laptop, open Terminal or PowerShell. Clone the guide repository, then copy it to your CAE home directory:

```bash
git clone https://github.com/abhinavnandwani/cae-synopsys-guides.git
scp -r cae-synopsys-guides YOUR_NETID@best-tux.cae.wisc.edu:~/
```

Replace `YOUR_NETID` with your NetID. Check a new SSH host key against the CAE fingerprint at https://kb.wisc.edu/moodle/162780 before accepting. If Git is unavailable, extract the repository ZIP, rename its folder to `cae-synopsys-guides`, then run the SCP line. Guacamole does not provide file transfer. The repository README also explains cloning directly on CAE.

Back in the CAE container terminal:

```bash
cd ~/cae-synopsys-guides/lab
pwd
ls
```

You should see `run_lab.py`, `rtl`, `tb`, `synth`, and `README.md`. The recorded screenshots use a dated demonstration folder. Use the folder you copied. Keep work in your home directory so it is available across CAE hosts.

<!-- page -->
## Work confidently in the terminal
The current directory affects relative paths. `pwd` prints it, `ls` lists files, `cd ..` moves to the parent, and `cd ~/cae-synopsys-guides/lab` returns to the exercise. A leading `/` means an absolute path; `~` means your home directory. Quote paths containing spaces.

| Prompt or location | Commands that belong there |
| --- | --- |
| Laptop Terminal or PowerShell | `ssh` and `scp` to reach CAE or transfer files. |
| CAE host shell | `module load synopsys/suite`, then `synopsys-run`. |
| Container `synopsys>` | Linux commands, `python3 run_lab.py`, `vcs`, `verdi`, `dc_shell`, and `icc2_shell`. |
| Tool prompt such as `dc_shell>` | Tool Tcl commands such as `read_ddc`, `report_timing`, and `help`. |

Use these from the exercise folder to inspect source and logs without changing them:

```bash
ls -lh
cat rtl/sb_flop.v
sed -n '1,80p' tb/tb.sv
less runs/YOUR_RUN/compile.log
grep -nE 'Error|Fatal|Warning' runs/YOUR_RUN/compile.log
tail -n 30 runs/YOUR_RUN/simulate.log
```

Replace `YOUR_RUN` with an actual directory printed by the runner. In `less`, use Space to advance, `/Error` then Enter to search, `n` for the next match, and `q` to return to the shell. An Up-arrow recalls a command; Tab completes a path. Read a command before rerunning it.

For an interactive foreground command that is stuck, Ctrl+C requests interruption. For a GUI launched with `&`, close the application through its File menu. `jobs` lists jobs started by that shell. Keep logs: `command > run.log 2>&1` sends both standard output and errors to a file. Immediately after a command, `echo $?` reports its exit status, but a zero status alone does not prove the design passed.

## Connect without the browser when useful
For terminal-only work, open a terminal on your laptop and run `ssh YOUR_NETID@best-tux.cae.wisc.edu`, then load the module and enter the container as above. Use Guacamole for the GUI steps in this handout. SSH and Guacamole may reach different hosts, but your CAE home directory is shared.

When finished, save work, close the EDA applications, and run `exit` to leave the container. Log out of the Linux desktop from the upper-right system menu. Closing the browser alone can leave the session running during CAE's two-hour reconnection window.
