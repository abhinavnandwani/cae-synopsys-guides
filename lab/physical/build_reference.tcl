# Run with icc2_lm_shell from a new, private teaching run directory.
# Generated reference data stays on CAE. Do not distribute it.
set edk /srv/auto/apps/saed32_edk/2023
set cells $edk/lib/stdcell_rvt/SAED32_EDK/lib/stdcell_rvt
create_workspace -technology $edk/tech/milkyway/saed32nm_1p9m_mw.tf \
    -flow normal sb_rvt
read_db $cells/db_nldm/saed32rvt_tt1p05v25c.db
read_lef $cells/lef/saed32nm_rvt_1p9m.lef
check_workspace
# Inspect check_workspace's log before using the generated library.
commit_workspace -output sb_rvt.ndm
exit
