`timescale 1ns/1ps
`include "uvm_macros.svh"
module tb;
  import uvm_pkg::*;
  logic clk = 0, rst = 1, d = 0, q;
  sb_flop dut(.*);
  always #5 clk = ~clk;
  initial begin
    $fsdbDumpfile("smoke.fsdb");
    $fsdbDumpvars(0, tb);
    `uvm_info("ACCESS", "UVM package and macros are available", UVM_LOW)
    #11;
    if (q !== 0) $fatal(1, "reset failed");
    rst = 0; d = 1;
    if ($test$plusargs("INJECT_FAILURE")) force dut.q = 1'b0;
    #10;
    if (q !== 1) $fatal(1, "data failed");
    d = 0;
    #10;
    if (q !== 0) $fatal(1, "data failed");
    $display("SB_SNPS_SIM_PASS");
    $finish;
  end
endmodule
