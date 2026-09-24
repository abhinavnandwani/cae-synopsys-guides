# Run from the directory containing sb_rvt.ndm.
# SB_SYNTH_RUN must point to the successful synthesis run.
create_lib -ref_libs {sb_rvt.ndm} sb_flop.dlib
read_verilog -top sb_flop $env(SB_SYNTH_RUN)/mapped.v
link_block
read_sdc $env(SB_SYNTH_RUN)/constraints.sdc
initialize_floorplan -control_type die \
    -boundary {{0 0} {20 20}} -core_offset 2
create_placement -floorplan
puts "REGISTER_ORIGIN=[get_attribute [get_cells q_reg] origin]"
puts "REGISTER_STATUS=[get_attribute [get_cells q_reg] physical_status]"
save_block
save_lib
puts SB_SNPS_FLOORPLAN_DONE
exit
