# The runner supplies absolute paths and the selected teaching library.
set_app_var target_library [list $env(SB_TARGET_LIBRARY)]
set_app_var link_library [concat * $target_library]
read_verilog $env(SB_RTL)
current_design sb_flop
if {![link]} {error "Design failed to link"}
create_clock -name clk -period 10 [get_ports clk]
set_input_delay 1 -clock clk [get_ports {rst d}]
set_output_delay 1 -clock clk [get_ports q]
compile
if {![check_design]} {error "check_design failed"}
redirect -file area.rpt {report_area}
redirect -file timing.rpt {report_timing}
redirect -file constraints.rpt {report_constraint -all_violators}
write -format verilog -hierarchy -output mapped.v
write -format ddc -hierarchy -output mapped.ddc
write_sdc constraints.sdc
puts SB_SNPS_SYNTH_DONE
quit
