# Added by Yuzong Chen (yc2367@cornell.edu)
# This file contains subcircuits for BRAM-CIM dummy array


import math


# Added by Yuzong Chen (yc2367@cornell.edu)
# This is the precharging circuitry for BRAM-CIM dummy array
def generate_precharge_dummy_lp(spice_filename, circuit_name):

	# Open SPICE file for appending
	spice_file = open(spice_filename, 'a')
	# currently only works for 22nm
	spice_file.write("******************************************************************************************\n")
	spice_file.write("* " + circuit_name + " subcircuit dummy-array precharge and equalization \n")
	spice_file.write("******************************************************************************************\n")
	spice_file.write(".SUBCKT " + circuit_name + " n_precharge_bar n_bl n_blbar n_vdd n_gnd\n")
	spice_file.write("M1 n_bl n_precharge_bar n_vdd n_vdd pmos_lp L=gate_length W=90n ")
	spice_file.write("AS=90n*trans_diffusion_length AD=90n*trans_diffusion_length PS=90n+2*trans_diffusion_length PD=90n+2*trans_diffusion_length\n")
	spice_file.write("M0 n_blbar n_precharge_bar n_vdd n_vdd pmos_lp L=gate_length W=90n ")
	spice_file.write("AS=90n*trans_diffusion_length AD=90n*trans_diffusion_length PS=90n+2*trans_diffusion_length PD=90n+2*trans_diffusion_length\n")
	spice_file.write("M2 n_bl n_precharge_bar n_blbar n_vdd pmos_lp L=gate_length W=45n ")
	spice_file.write("AS=45n*trans_diffusion_length AD=45n*trans_diffusion_length PS=45n+2*trans_diffusion_length PD=45n+2*trans_diffusion_length\n")
	spice_file.write(".ENDS\n\n\n")
	spice_file.close()

	tran_names_list = []
	wire_names_list = []

	return tran_names_list, wire_names_list


# Added by Yuzong Chen (yc2367@cornell.edu)
# This is the full-swing read circuit for BRAM-CIM dummy array
# We are not going to size this circuit, the pmos/nmos ratio is determined by the stardard cell pmos/nmos ratio in 28nm technology 
def generate_readcircuit_dummy_lp(spice_filename, circuit_name):

	# Open SPICE file for appending
	spice_file = open(spice_filename, 'a')
	# currently only works for 22nm
	spice_file.write("******************************************************************************************\n")
	spice_file.write("* " + circuit_name + " subcircuit dummy-array read circuit \n")
	spice_file.write("******************************************************************************************\n")
	spice_file.write(".SUBCKT " + circuit_name + " Ren n_bl n_blbar out outbar n_vdd n_gnd\n")
	spice_file.write("X_inv_readcircuit_dummy_1   n_bl    n_1    n_vdd n_gnd inv_lp Wn=45n Wp=55n\n")
	spice_file.write("X_inv_readcircuit_dummy_2   n_blbar n_2    n_vdd n_gnd inv_lp Wn=45n Wp=55n\n")
	spice_file.write("Xreadcircuit_dummy_nand2_1  Ren n_1 o_1    n_vdd n_gnd nand2_dummy_lp Wn=45n Wp=55n\n")
	spice_file.write("Xreadcircuit_dummy_nand2_2  Ren n_2 o_2    n_vdd n_gnd nand2_dummy_lp Wn=45n Wp=55n\n")
	spice_file.write("Xreadcircuit_dummy_nand2_3  o_1 z_2 z_1    n_vdd n_gnd nand2_dummy_lp Wn=45n Wp=55n\n")
	spice_file.write("Xreadcircuit_dummy_nand2_4  o_2 z_1 z_2    n_vdd n_gnd nand2_dummy_lp Wn=45n Wp=55n\n")
	spice_file.write("X_inv_readcircuit_dummy_3   z_1     out    n_vdd n_gnd inv_lp Wn=90n Wp=110n\n")
	spice_file.write("X_inv_readcircuit_dummy_4   z_2     outbar n_vdd n_gnd inv_lp Wn=90n Wp=110n\n")
	spice_file.write(".ENDS\n\n\n")
	spice_file.close()

	tran_names_list = []
	wire_names_list = []

	return tran_names_list, wire_names_list


# Added by Yuzong Chen (yc2367@cornell.edu)
# This is the sense amp circuit for BRAM-CIM dummy array
# We are not going to size this circuit. 
def generate_samp_dummy_lp(spice_filename, circuit_name):

	# Open SPICE file for appending
	spice_file = open(spice_filename, 'a')
	# currently only works for 22nm

	spice_file.write("******************************************************************************************\n")
	spice_file.write("* " + circuit_name + " subcircuit dummy-array sense amp \n")
	spice_file.write("******************************************************************************************\n")
	spice_file.write(".SUBCKT " + circuit_name + " n_se n_in1 n_in2 n_out n_vdd n_gnd \n")

	spice_file.write("M1 n_in1 n_se n_1_1 n_vdd pmos_lp L=32n W=250n ")
	spice_file.write("AS=250n*trans_diffusion_length AD=250n*trans_diffusion_length PS=250n+2*trans_diffusion_length PD=250n+2*trans_diffusion_length\n")	
	spice_file.write("M0 n_1_1 n_1_2 n_vdd n_vdd pmos_lp L=65n W=100n ")
	spice_file.write("AS=100n*trans_diffusion_length AD=100n*trans_diffusion_length PS=100n+2*trans_diffusion_length PD=100n+2*trans_diffusion_length\n")	
	spice_file.write("M2 n_1_2 n_1_1 n_vdd  n_vdd pmos_lp L=65n W=100n ")
	spice_file.write("AS=100n*trans_diffusion_length AD=100n*trans_diffusion_length PS=100n+2*trans_diffusion_length PD=100n+2*trans_diffusion_length\n")	
	spice_file.write("M3 n_in2 n_se n_1_2 n_vdd pmos_lp L=32n W=250n ")
	spice_file.write("AS=250n*trans_diffusion_length AD=250n*trans_diffusion_length PS=250n+2*trans_diffusion_length PD=250n+2*trans_diffusion_length\n")	
	spice_file.write("M4 n_1_1 n_1_2 n_gnd2 n_gnd nmos_lp L=65n W=900n ")
	spice_file.write("AS=900n*trans_diffusion_length AD=900n*trans_diffusion_length PS=900n+2*trans_diffusion_length PD=900n+2*trans_diffusion_length\n")
	spice_file.write("M5 n_1_2 n_1_1 n_gnd2 n_gnd nmos_lp L=65n W=900n ")
	spice_file.write("AS=900n*trans_diffusion_length AD=900n*trans_diffusion_length PS=900n+2*trans_diffusion_length PD=900n+2*trans_diffusion_length\n")
	spice_file.write("M6 n_gnd2 n_se n_gnd n_gnd nmos_lp L=65n W=250n ")
	spice_file.write("AS=250n*trans_diffusion_length AD=250n*trans_diffusion_length PS=250n+2*trans_diffusion_length PD=250n+2*trans_diffusion_length\n")	
	#add the two inverters
	#spice_file.write("X_inv" + circuit_name + "_1 n_1_1 n_hang n_vdd n_gnd inv Wn=inv_samp_output_1_nmos Wp=inv_samp_output_1_pmos\n")
	#spice_file.write("X_inv" + circuit_name + "_2 n_1_2 n_out n_vdd n_gnd inv Wn=inv_samp_output_1_nmos Wp=inv_samp_output_1_pmos\n")
	spice_file.write("X_inv" + circuit_name + "_1 n_1_1 n_hang n_vdd n_gnd inv_lp Wn=90n Wp=110n\n")
	spice_file.write("X_inv" + circuit_name + "_2 n_1_2 n_out n_vdd n_gnd inv_lp Wn=90n Wp=110n\n")

	spice_file.write(".ENDS\n\n\n")
	spice_file.close()	
	tran_names_list = []
	wire_names_list = []

	return tran_names_list, wire_names_list


# Added by Yuzong Chen (yc2367@cornell.edu)
# This is the write driver for BRAM-CIM dummy array
# The part which is commented out can be restored (you need to comment those below it) to enable sizing of this module
# It is however expected that write driver not be in the critical path of SRAM-based BRAm and therefore sizing it will just increase COFEE's runtime.
def generate_writedriver_dummy_lp(spice_filename, circuit_name):

	# Open SPICE file for appending
	spice_file = open(spice_filename, 'a')
	# currently only works for 22nm

	spice_file.write("******************************************************************************************\n")
	spice_file.write("* " + circuit_name + " subcircuit dummy array write driver \n")
	spice_file.write("******************************************************************************************\n")
	spice_file.write(".SUBCKT " + circuit_name + " n_we n_din n_bl n_br n_vdd n_gnd\n")

	spice_file.write("M0 p_1_1 n_web n_vdd n_vdd pmos_lp L=gate_length W=90n ")
	spice_file.write("AS=90n*trans_diffusion_length AD=90n*trans_diffusion_length PS=90n+2*trans_diffusion_length PD=90n+2*trans_diffusion_length\n")	
	spice_file.write("M1 p_1_2 n_web n_vdd n_vdd pmos_lp L=gate_length W=90n ")
	spice_file.write("AS=90n*trans_diffusion_length AD=90n*trans_diffusion_length PS=90n+2*trans_diffusion_length PD=90n+2*trans_diffusion_length\n")	
	spice_file.write("M2 n_bl n_din1 p_1_1 n_vdd pmos_lp L=gate_length W=90n ")
	spice_file.write("AS=90n*trans_diffusion_length AD=90n*trans_diffusion_length PS=90n+2*trans_diffusion_length PD=90n+2*trans_diffusion_length\n")	
	spice_file.write("M3 n_br n_dinb p_1_2 n_vdd pmos_lp L=gate_length W=90n ")
	spice_file.write("AS=90n*trans_diffusion_length AD=90n*trans_diffusion_length PS=90n+2*trans_diffusion_length PD=90n+2*trans_diffusion_length\n")	

	spice_file.write("M4 n_1_1 n_we n_gnd n_gnd nmos_lp L=gate_length W=120n ")
	spice_file.write("AS=120n*trans_diffusion_length AD=120n*trans_diffusion_length PS=120n+2*trans_diffusion_length PD=120n+2*trans_diffusion_length\n")	
	spice_file.write("M5 n_1_2 n_we n_gnd n_gnd nmos_lp L=gate_length W=120n ")
	spice_file.write("AS=120n*trans_diffusion_length AD=120n*trans_diffusion_length PS=120n+2*trans_diffusion_length PD=120n+2*trans_diffusion_length\n")	
	spice_file.write("M6 n_bl n_din1 n_1_1 n_gnd nmos_lp L=gate_length W=120n ")
	spice_file.write("AS=120n*trans_diffusion_length AD=120n*trans_diffusion_length PS=120n+2*trans_diffusion_length PD=120n+2*trans_diffusion_length\n")	
	spice_file.write("M7 n_br n_dinb n_1_2 n_gnd nmos_lp L=gate_length W=120n ")
	spice_file.write("AS=120n*trans_diffusion_length AD=120n*trans_diffusion_length PS=120n+2*trans_diffusion_length PD=120n+2*trans_diffusion_length\n")	
	#add the two inverters
	spice_file.write("X_inv_writedriver_dummy_1 n_din  n_dinb n_vdd n_gnd inv_lp Wn=45n Wp=55n\n")
	spice_file.write("X_inv_writedriver_dummy_2 n_dinb n_din1  n_vdd n_gnd inv_lp Wn=45n Wp=55n\n")
	spice_file.write("X_inv_writedriver_dummy_3 n_we n_web n_vdd n_gnd inv_lp Wn=45n Wp=55n\n")
	spice_file.write(".ENDS\n\n\n")
	spice_file.close()	

	tran_names_list = []
	wire_names_list = []

	return tran_names_list, wire_names_list


# Added by Yuzong Chen (yc2367@cornell.edu)
# This is the full adder circuit for BRAM-CIM dummy array (not using low-power for good performance)
# We are going to size only the carry propagation tgate of this circuit.
# For other components, the pmos/nmos ratio is determined by the stardard cell pmos/nmos ratio in 28nm technology 
# We are going to make one input of the adder always 0, as this makes it easier to measure the delay
def generate_fulladder_dummy(spice_filename, circuit_name, numberofsrams):

	# Open SPICE file for appending
	spice_file = open(spice_filename, 'a')
	# currently only works for 22nm
	spice_file.write("******************************************************************************************\n")
	spice_file.write("* " + circuit_name + " subcircuit dummy-array full adder \n")
	spice_file.write("******************************************************************************************\n")
	spice_file.write(".SUBCKT " + circuit_name + " op cin cout sum n_vdd n_gnd\n")
	
	# This inverter is just used for simulation since we have complementary outputs in the dummy array read circuit 
	spice_file.write("X_inv_fulladder_dummy_0 op  opbar  n_vdd n_gnd inv Wn=45n Wp=55n\n") 
	
	spice_file.write("X_inv_fulladder_dummy_1 cin cinbar n_vdd n_gnd inv Wn=45n Wp=55n\n")

	# circuit for sum
	spice_file.write("X_tgate_fulladder_dummy_1 op  n_1 n_vdd n_gnd n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_fulladder_dummy_2 gnd n_1 n_gnd n_vdd n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("X_inv_fulladder_dummy_2   n_1 n_1_1 n_vdd n_gnd           inv   Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_fulladder_dummy_3 n_1_1 sumbar cinbar cin    n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_fulladder_dummy_4 n_1   sumbar cin    cinbar n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	
	# circuit for carry out
	spice_file.write("Xfulladder_dummy_nand2_1  opbar n_vdd o_1 n_vdd n_gnd nand2_dummy  Wn=tgate_fulladder_dummy_1_nmos Wp=tgate_fulladder_dummy_1_pmos\n")
	spice_file.write("Xfulladder_dummy_nor2_1   opbar n_vdd o_2 n_vdd n_gnd nor2_dummy   Wn=tgate_fulladder_dummy_1_nmos Wp=tgate_fulladder_dummy_1_pmos\n")
	spice_file.write("X_tgate_fulladder_dummy_5 o_1   cout1 cin    cinbar n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_fulladder_dummy_6 o_2   cout1 cinbar cin    n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("Xwire1 cout1 cout wire Rw=wire_memorycell_horizontal_res/"+str(numberofsrams)+" Cw=wire_memorycell_horizontal_cap/"+str(numberofsrams)+"\n")

	# drive sum
	spice_file.write("X_inv_fulladder_dummy_3 sumbar  sum  n_vdd n_gnd inv Wn=65n Wp=80n\n")

	spice_file.write(".ENDS\n\n\n")
	spice_file.close()

	tran_names_list = []
	tran_names_list.append("tgate_fulladder_dummy_1_nmos")
	tran_names_list.append("tgate_fulladder_dummy_1_pmos")

	wire_names_list = []

	return tran_names_list, wire_names_list


# Added by Yuzong Chen (yc2367@cornell.edu)
# This is the 4-bit manchester carry chain for full adder in BRAM-CIM dummy array (not using low-power for good performance)
# We are going to size only the carry propagation and buffer of this circuit.
# For other components, the pmos/nmos ratio is determined by the stardard cell pmos/nmos ratio in 28nm technology 
# Hence the adder is just propagating the Cin (1111 + 0001 + 0 = 1 0000)
def generate_manchester4_dummy(spice_filename, circuit_name, numberofsrams):

	# Open SPICE file for appending
	spice_file = open(spice_filename, 'a')
	# currently only works for 22nm
	spice_file.write("******************************************************************************************\n")
	spice_file.write("* " + circuit_name + " subcircuit dummy-array 4-bit manchester carry chain full adder \n")
	spice_file.write("******************************************************************************************\n")
	spice_file.write(".SUBCKT " + circuit_name + " clk cinb cout ina3 ina2 ina1 ina0 inb3 inb2 inb1 inb0 sum4 n_vdd n_gnd\n")
	
	# input carry, add buffer to cin
	spice_file.write("X_inv_manchester4_dummy_21 cinb   c_x1  n_vdd n_gnd inv Wn=65n Wp=80n\n") # Cin buffer 1
	# Cin buffer 2
	spice_file.write("M01 n_vdd clk cin_buff n_vdd pmos L=gate_length W=45n ")
	spice_file.write("AS=45n*trans_diffusion_length AD=45n*trans_diffusion_length PS=45n+2*trans_diffusion_length PD=45n+2*trans_diffusion_length\n")
	spice_file.write("M02 cib0 c_x1 c_x2 n_gnd nmos L=gate_length W=ptran_manchester4_dummy_1_nmos ")
	spice_file.write("AS=ptran_manchester4_dummy_1_nmos*trans_diffusion_length AD=ptran_manchester4_dummy_1_nmos*trans_diffusion_length"+
										" PS=ptran_manchester4_dummy_1_nmos+2*trans_diffusion_length PD=ptran_manchester4_dummy_1_nmos+2*trans_diffusion_length\n")
	spice_file.write("M03 c_x2 clk n_gnd n_gnd nmos L=gate_length W=ptran_manchester4_dummy_1_nmos ")
	spice_file.write("AS=ptran_manchester4_dummy_1_nmos*trans_diffusion_length AD=ptran_manchester4_dummy_1_nmos*trans_diffusion_length"+
										" PS=ptran_manchester4_dummy_1_nmos+2*trans_diffusion_length PD=ptran_manchester4_dummy_1_nmos+2*trans_diffusion_length\n")

	# 1111 + 0001
	# Generate
	spice_file.write("Xmanchester4_dummy_nor2_1 a0b b0b gen_1 n_vdd n_gnd nor2_dummy Wn=45n Wp=55n\n")
	spice_file.write("Xmanchester4_dummy_nor2_2 a1b b1b gen_2 n_vdd n_gnd nor2_dummy Wn=45n Wp=55n\n")
	spice_file.write("Xmanchester4_dummy_nor2_3 a2b b2b gen_3 n_vdd n_gnd nor2_dummy Wn=45n Wp=55n\n")
	spice_file.write("Xmanchester4_dummy_nor2_4 a3b b3b gen_4 n_vdd n_gnd nor2_dummy Wn=45n Wp=55n\n")

	# Propagate
	spice_file.write("X_tgate_manchester4_dummy_1 a0 prop_1 b0b b0 n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_manchester4_dummy_2 a0b prop_1 b0 b0b n_vdd n_gnd tgate Wn=45n Wp=55n\n")

	spice_file.write("X_tgate_manchester4_dummy_3 a1 prop_2 b1b b1 n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_manchester4_dummy_4 a1b prop_2 b1 b1b n_vdd n_gnd tgate Wn=45n Wp=55n\n")

	spice_file.write("X_tgate_manchester4_dummy_5 a2 prop_3 b2b b2 n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_manchester4_dummy_6 a2b prop_3 b2 b2b n_vdd n_gnd tgate Wn=45n Wp=55n\n")

	spice_file.write("X_tgate_manchester4_dummy_7 a3 prop_4 b3b b3 n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_manchester4_dummy_8 a3b prop_4 b3 b3b n_vdd n_gnd tgate Wn=45n Wp=55n\n")

	# Complementary carry
	spice_file.write("X_inv_manchester4_dummy_1 cib1_1 c1  n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_manchester4_dummy_2 c1     c1b n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_manchester4_dummy_3 cib2_2 c2  n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_manchester4_dummy_4 c2     c2b n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_manchester4_dummy_5 cib3_3 c3  n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_manchester4_dummy_6 c3     c3b n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_manchester4_dummy_7 cib4_4 c4  n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_manchester4_dummy_8 c4     c4b n_vdd n_gnd inv Wn=45n Wp=55n\n")

	# Sum
	spice_file.write("X_inv_manchester4_dummy_11    prop_1 n_1    n_vdd n_gnd inv   Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_manchester4_dummy_12  n_1    sumb1  c1b   c1    n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_manchester4_dummy_13  prop_1 sumb1  c1    c1b   n_vdd n_gnd tgate Wn=45n Wp=55n\n")

	spice_file.write("X_inv_manchester4_dummy_14    prop_2 n_2    n_vdd n_gnd inv   Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_manchester4_dummy_15  n_2    sumb2  c2b   c2    n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_manchester4_dummy_16  prop_2 sumb2  c2    c2b   n_vdd n_gnd tgate Wn=45n Wp=55n\n")

	spice_file.write("X_inv_manchester4_dummy_17    prop_3 n_3    n_vdd n_gnd inv   Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_manchester4_dummy_18  n_3    sumb3  c3b   c3    n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_manchester4_dummy_19  prop_3 sumb3  c3    c3b   n_vdd n_gnd tgate Wn=45n Wp=55n\n")

	spice_file.write("X_inv_manchester4_dummy_20    prop_4 n_4    n_vdd n_gnd inv   Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_manchester4_dummy_21  n_4    sumb4  c4b   c4    n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_manchester4_dummy_22  prop_4 sumb4  c4    c4b   n_vdd n_gnd tgate Wn=45n Wp=55n\n")

	spice_file.write("X_inv_manchester4_dummy_31 sumb1  sum1  n_vdd n_gnd inv Wn=65n Wp=80n\n")
	spice_file.write("X_inv_manchester4_dummy_32 sumb2  sum2  n_vdd n_gnd inv Wn=65n Wp=80n\n")
	spice_file.write("X_inv_manchester4_dummy_33 sumb3  sum3  n_vdd n_gnd inv Wn=65n Wp=80n\n")
	spice_file.write("X_inv_manchester4_dummy_34 sumb4  sum4  n_vdd n_gnd inv Wn=65n Wp=80n\n")

	# Carry chain
	spice_file.write("M11  cib0    prop_1 cib1_1  n_gnd nmos L=gate_length W=ptran_manchester4_dummy_5_nmos ")
	spice_file.write("AS=ptran_manchester4_dummy_5_nmos*trans_diffusion_length AD=ptran_manchester4_dummy_5_nmos*trans_diffusion_length"+
										" PS=ptran_manchester4_dummy_5_nmos+2*trans_diffusion_length PD=ptran_manchester4_dummy_5_nmos+2*trans_diffusion_length\n")
	spice_file.write("M12  n_vdd   clk    cib1_1  n_vdd pmos L=gate_length W=45n ")
	spice_file.write("AS=45n*trans_diffusion_length AD=45n*trans_diffusion_length PS=45n+2*trans_diffusion_length PD=45n+2*trans_diffusion_length\n")
	spice_file.write("M13  cib1_1  gen_1  n_x1    n_gnd nmos L=gate_length W=ptran_manchester4_dummy_6_nmos ")
	spice_file.write("AS=ptran_manchester4_dummy_6_nmos*trans_diffusion_length AD=ptran_manchester4_dummy_6_nmos*trans_diffusion_length"+
										" PS=ptran_manchester4_dummy_6_nmos+2*trans_diffusion_length PD=ptran_manchester4_dummy_6_nmos+2*trans_diffusion_length\n")
	spice_file.write("M14  n_x1    clk    n_gnd   n_gnd nmos L=gate_length W=ptran_manchester4_dummy_6_nmos ")
	spice_file.write("AS=ptran_manchester4_dummy_6_nmos*trans_diffusion_length AD=ptran_manchester4_dummy_6_nmos*trans_diffusion_length"+
										" PS=ptran_manchester4_dummy_6_nmos+2*trans_diffusion_length PD=ptran_manchester4_dummy_6_nmos+2*trans_diffusion_length\n")

	spice_file.write("Xwire1 cib1_1 cib1 wire Rw=wire_memorycell_horizontal_res/"+str(numberofsrams)+" Cw=wire_memorycell_horizontal_cap/"+str(numberofsrams)+"\n")

	spice_file.write("M21  cib1    prop_2 cib2_2  n_gnd nmos L=gate_length W=ptran_manchester4_dummy_5_nmos ")
	spice_file.write("AS=ptran_manchester4_dummy_5_nmos*trans_diffusion_length AD=ptran_manchester4_dummy_5_nmos*trans_diffusion_length"+
										" PS=ptran_manchester4_dummy_5_nmos+2*trans_diffusion_length PD=ptran_manchester4_dummy_5_nmos+2*trans_diffusion_length\n")
	spice_file.write("M22  n_vdd   clk    cib2_2  n_vdd pmos L=gate_length W=45n ")
	spice_file.write("AS=45n*trans_diffusion_length AD=45n*trans_diffusion_length PS=45n+2*trans_diffusion_length PD=45n+2*trans_diffusion_length\n")
	spice_file.write("M23  cib2_2  gen_2  n_x2    n_gnd nmos L=gate_length W=ptran_manchester4_dummy_6_nmos ")
	spice_file.write("AS=ptran_manchester4_dummy_6_nmos*trans_diffusion_length AD=ptran_manchester4_dummy_6_nmos*trans_diffusion_length"+
										" PS=ptran_manchester4_dummy_6_nmos+2*trans_diffusion_length PD=ptran_manchester4_dummy_6_nmos+2*trans_diffusion_length\n")
	spice_file.write("M24  n_x2    clk    n_gnd   n_gnd nmos L=gate_length W=ptran_manchester4_dummy_6_nmos ")
	spice_file.write("AS=ptran_manchester4_dummy_6_nmos*trans_diffusion_length AD=ptran_manchester4_dummy_6_nmos*trans_diffusion_length"+
										" PS=ptran_manchester4_dummy_6_nmos+2*trans_diffusion_length PD=ptran_manchester4_dummy_6_nmos+2*trans_diffusion_length\n")

	spice_file.write("Xwire2 cib2_2 cib2 wire Rw=wire_memorycell_horizontal_res/"+str(numberofsrams)+" Cw=wire_memorycell_horizontal_cap/"+str(numberofsrams)+"\n")

	spice_file.write("M31  cib2    prop_3 cib3_3  n_gnd nmos L=gate_length W=ptran_manchester4_dummy_5_nmos ")
	spice_file.write("AS=ptran_manchester4_dummy_5_nmos*trans_diffusion_length AD=ptran_manchester4_dummy_5_nmos*trans_diffusion_length"+
										" PS=ptran_manchester4_dummy_5_nmos+2*trans_diffusion_length PD=ptran_manchester4_dummy_5_nmos+2*trans_diffusion_length\n")
	spice_file.write("M32  n_vdd   clk    cib3_3  n_vdd pmos L=gate_length W=45n ")
	spice_file.write("AS=45n*trans_diffusion_length AD=45n*trans_diffusion_length PS=45n+2*trans_diffusion_length PD=45n+2*trans_diffusion_length\n")
	spice_file.write("M33  cib3_3  gen_3  n_x3     n_gnd nmos L=gate_length W=ptran_manchester4_dummy_6_nmos ")
	spice_file.write("AS=ptran_manchester4_dummy_6_nmos*trans_diffusion_length AD=ptran_manchester4_dummy_6_nmos*trans_diffusion_length"+
										" PS=ptran_manchester4_dummy_6_nmos+2*trans_diffusion_length PD=ptran_manchester4_dummy_6_nmos+2*trans_diffusion_length\n")
	spice_file.write("M34  n_x3    clk    n_gnd   n_gnd nmos L=gate_length W=ptran_manchester4_dummy_6_nmos ")
	spice_file.write("AS=ptran_manchester4_dummy_6_nmos*trans_diffusion_length AD=ptran_manchester4_dummy_6_nmos*trans_diffusion_length"+
										" PS=ptran_manchester4_dummy_6_nmos+2*trans_diffusion_length PD=ptran_manchester4_dummy_6_nmos+2*trans_diffusion_length\n")

	spice_file.write("Xwire3 cib3_3 cib3 wire Rw=wire_memorycell_horizontal_res/"+str(numberofsrams)+" Cw=wire_memorycell_horizontal_cap/"+str(numberofsrams)+"\n")

	spice_file.write("M41  cib3    prop_4 cout_0  n_gnd nmos L=gate_length W=ptran_manchester4_dummy_5_nmos ")
	spice_file.write("AS=ptran_manchester4_dummy_5_nmos*trans_diffusion_length AD=ptran_manchester4_dummy_5_nmos*trans_diffusion_length"+
										" PS=ptran_manchester4_dummy_5_nmos+2*trans_diffusion_length PD=ptran_manchester4_dummy_5_nmos+2*trans_diffusion_length\n")
	spice_file.write("M42  n_vdd   clk    cout_0  n_vdd pmos L=gate_length W=45n ")
	spice_file.write("AS=45n*trans_diffusion_length AD=45n*trans_diffusion_length PS=45n+2*trans_diffusion_length PD=45n+2*trans_diffusion_length\n")
	spice_file.write("M43  cout_0  gen_4  n_x4    n_gnd nmos L=gate_length W=ptran_manchester4_dummy_6_nmos ")
	spice_file.write("AS=ptran_manchester4_dummy_6_nmos*trans_diffusion_length AD=ptran_manchester4_dummy_6_nmos*trans_diffusion_length"+
										" PS=ptran_manchester4_dummy_6_nmos+2*trans_diffusion_length PD=ptran_manchester4_dummy_6_nmos+2*trans_diffusion_length\n")
	spice_file.write("M44  n_x4    clk    n_gnd   n_gnd nmos L=gate_length W=ptran_manchester4_dummy_6_nmos ")
	spice_file.write("AS=ptran_manchester4_dummy_6_nmos*trans_diffusion_length AD=ptran_manchester4_dummy_6_nmos*trans_diffusion_length"+
										" PS=ptran_manchester4_dummy_6_nmos+2*trans_diffusion_length PD=ptran_manchester4_dummy_6_nmos+2*trans_diffusion_length\n")

	spice_file.write("Xwire4 cib4_4 cout wire Rw=wire_memorycell_horizontal_res/"+str(numberofsrams)+" Cw=wire_memorycell_horizontal_cap/"+str(numberofsrams)+"\n")

	# Bypass signal
	spice_file.write("Xwire11 prop_1 prop_1_1 wire Rw=wire_memorycell_horizontal_res/"+str(numberofsrams/4)+" Cw=wire_memorycell_horizontal_cap/"+str(numberofsrams/4)+"\n")
	spice_file.write("Xwire12 prop_2 prop_2_2 wire Rw=wire_memorycell_horizontal_res/"+str(numberofsrams/4)+" Cw=wire_memorycell_horizontal_cap/"+str(numberofsrams/4)+"\n")
	spice_file.write("Xwire13 prop_3 prop_3_3 wire Rw=wire_memorycell_horizontal_res/"+str(numberofsrams/4)+" Cw=wire_memorycell_horizontal_cap/"+str(numberofsrams/4)+"\n")
	spice_file.write("Xwire14 prop_4 prop_4_4 wire Rw=wire_memorycell_horizontal_res/"+str(numberofsrams/4)+" Cw=wire_memorycell_horizontal_cap/"+str(numberofsrams/4)+"\n")

	spice_file.write("Xmanchester4_dummy_nand2_11 prop_1_1 prop_2_2 n_z1   n_vdd n_gnd nand2_dummy Wn=45n Wp=55n\n")
	spice_file.write("Xmanchester4_dummy_nand2_12 prop_3_3 prop_4_4 n_z2   n_vdd n_gnd nand2_dummy Wn=45n Wp=55n\n")
	spice_file.write("Xmanchester4_dummy_nor2_13  n_z1  n_z2    byp n_vdd n_gnd nor2_dummy  Wn=45n Wp=55n\n")
	spice_file.write("X_inv_manchester4_dummy_41 byp   bypassb      n_vdd n_gnd inv Wn=65n Wp=80n\n")
	spice_file.write("X_inv_manchester4_dummy_42 bypassb   bypass      n_vdd n_gnd inv Wn=65n Wp=80n\n")

	spice_file.write("Xwire5 cib0 cout_1 wire Rw=wire_memorycell_horizontal_res/"+str(numberofsrams/4)+" Cw=wire_memorycell_horizontal_cap/"+str(numberofsrams/4)+"\n")
	spice_file.write("M51 cout_1 bypass cout  n_gnd nmos L=gate_length W=ptran_manchester4_dummy_5_nmos ")
	spice_file.write("AS=ptran_manchester4_dummy_5_nmos*trans_diffusion_length AD=ptran_manchester4_dummy_5_nmos*trans_diffusion_length"+
										" PS=ptran_manchester4_dummy_5_nmos+2*trans_diffusion_length PD=ptran_manchester4_dummy_5_nmos+2*trans_diffusion_length\n")
	spice_file.write("M52 cout_0 bypassb cout  n_gnd nmos L=gate_length W=ptran_manchester4_dummy_5_nmos ")
	spice_file.write("AS=ptran_manchester4_dummy_5_nmos*trans_diffusion_length AD=ptran_manchester4_dummy_5_nmos*trans_diffusion_length"+
										" PS=ptran_manchester4_dummy_5_nmos+2*trans_diffusion_length PD=ptran_manchester4_dummy_5_nmos+2*trans_diffusion_length\n")

	# set up inputs
	spice_file.write("X_inv_manchester4_dummy_51 ina3  a3b   n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_manchester4_dummy_52 a3b   a3    n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_manchester4_dummy_53 ina2  a2b   n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_manchester4_dummy_54 a2b   a2    n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_manchester4_dummy_55 ina1  a1b   n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_manchester4_dummy_56 a1b   a1    n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_manchester4_dummy_57 ina0  a0b   n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_manchester4_dummy_58 a0b   a0    n_vdd n_gnd inv Wn=45n Wp=55n\n")

	spice_file.write("X_inv_manchester4_dummy_61 inb3  b3b   n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_manchester4_dummy_62 b3b   b3    n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_manchester4_dummy_63 inb2  b2b   n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_manchester4_dummy_64 b2b   b2    n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_manchester4_dummy_65 inb1  b1b   n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_manchester4_dummy_66 b1b   b1    n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_manchester4_dummy_67 inb0  b0b   n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_manchester4_dummy_68 b0b   b0    n_vdd n_gnd inv Wn=45n Wp=55n\n")
	
	spice_file.write(".ENDS\n\n\n")
	spice_file.close()

	tran_names_list = []
	#tran_names_list.append("ptran_manchester4_dummy_0_pmos") # clk pmos, 45n, 5
	tran_names_list.append("ptran_manchester4_dummy_1_nmos") # Cin buffer 2, sizable, 2
	#tran_names_list.append("inv_manchester4_dummy_2_nmos") # inv, nand2 nor2, 45n, 26
	#tran_names_list.append("inv_manchester4_dummy_2_pmos") # inv, nand2 nor2, 55n, 26
	#tran_names_list.append("tgate_manchester4_dummy_3_nmos") # standard tgate, 45n, 16
	#tran_names_list.append("tgate_manchester4_dummy_3_pmos") # standard tgate, 55n, 16
	#tran_names_list.append("inv_manchester4_dummy_4_nmos") # cin, sum, bypass driver, 65n, 7
	#tran_names_list.append("inv_manchester4_dummy_4_pmos") # cin, sum, bypass driver, 80n, 7
	tran_names_list.append("ptran_manchester4_dummy_5_nmos") # carry chain and bypass signal pass gate, sizable, 6
	tran_names_list.append("ptran_manchester4_dummy_6_nmos") # carry chain pulldown nmos, sizable, 8

	wire_names_list = []

	return tran_names_list, wire_names_list


# Added by Yuzong Chen (yc2367@cornell.edu)
# This is the 4-bit carry-lookahead adder in BRAM-CIM dummy array (not using low-power for good performance)
# Hence the adder is just propagating the Cin (1111 + 0001 + 0 = 1 0000)
def generate_lookahead4_dummy(spice_filename, circuit_name, numberofsrams):

	# Open SPICE file for appending
	spice_file = open(spice_filename, 'a')
	# currently only works for 22nm
	spice_file.write("******************************************************************************************\n")
	spice_file.write("* " + circuit_name + " subcircuit dummy-array 4-bit manchester carry chain full adder \n")
	spice_file.write("******************************************************************************************\n")
	spice_file.write(".SUBCKT " + circuit_name + " cin cout ina3 ina2 ina1 ina0 inb3 inb2 inb1 inb0 sum4 n_vdd n_gnd\n")

	# 1111 + 0001
	# Generate
	spice_file.write("Xlookahead4_dummy_nor2_1 a0b b0b gen_1 n_vdd n_gnd nor2_dummy Wn=45n Wp=55n\n")
	spice_file.write("Xlookahead4_dummy_nor2_2 a1b b1b gen_2 n_vdd n_gnd nor2_dummy Wn=45n Wp=55n\n")
	spice_file.write("Xlookahead4_dummy_nor2_3 a2b b2b gen_3 n_vdd n_gnd nor2_dummy Wn=45n Wp=55n\n")
	spice_file.write("Xlookahead4_dummy_nor2_4 a3b b3b gen_4 n_vdd n_gnd nor2_dummy Wn=45n Wp=55n\n")

	# Propagate
	spice_file.write("X_tgate_lookahead4_dummy_1 a0 prop_1 b0b b0 n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_lookahead4_dummy_2 a0b prop_1 b0 b0b n_vdd n_gnd tgate Wn=45n Wp=55n\n")

	spice_file.write("X_tgate_lookahead4_dummy_3 a1 prop_2 b1b b1 n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_lookahead4_dummy_4 a1b prop_2 b1 b1b n_vdd n_gnd tgate Wn=45n Wp=55n\n")

	spice_file.write("X_tgate_lookahead4_dummy_5 a2 prop_3 b2b b2 n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_lookahead4_dummy_6 a2b prop_3 b2 b2b n_vdd n_gnd tgate Wn=45n Wp=55n\n")

	spice_file.write("X_tgate_lookahead4_dummy_7 a3 prop_4 b3b b3 n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_lookahead4_dummy_8 a3b prop_4 b3 b3b n_vdd n_gnd tgate Wn=45n Wp=55n\n")

	# Cout
	spice_file.write("X_inv_lookahead4_dummy_91   cin c0b    n_vdd n_gnd inv   Wn=45n Wp=55n\n")
	spice_file.write("Xlookahead4_dummy_nand2_1   a0b b0b z1 n_vdd n_gnd nand2_dummy  Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_fulladder_dummy_91  z1      c1_1 cin c0b n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_fulladder_dummy_92  gen_1   c1_1 c0b cin n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("Xwire11 c1_1 c1 wire Rw=wire_memorycell_horizontal_res/"+str(numberofsrams)+" Cw=wire_memorycell_horizontal_cap/"+str(numberofsrams)+"\n")

	spice_file.write("X_inv_lookahead4_dummy_92   c1  c1b    n_vdd n_gnd inv   Wn=45n Wp=55n\n")
	spice_file.write("Xlookahead4_dummy_nand2_2   a1b b1b z2 n_vdd n_gnd nand2_dummy  Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_fulladder_dummy_93  z2      c2_2 c1  c1b n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_fulladder_dummy_94  gen_2   c2_2 c1b c1 n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("Xwire12 c2_2 c2 wire Rw=wire_memorycell_horizontal_res/"+str(numberofsrams)+" Cw=wire_memorycell_horizontal_cap/"+str(numberofsrams)+"\n")

	spice_file.write("X_inv_lookahead4_dummy_93   c2  c2b    n_vdd n_gnd inv   Wn=45n Wp=55n\n")
	spice_file.write("Xlookahead4_dummy_nand2_3   a2b b2b z3 n_vdd n_gnd nand2_dummy  Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_fulladder_dummy_95  z3      c3_3 c2  c2b n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_fulladder_dummy_96  gen_3   c3_3 c2b c2 n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("Xwire13 c3_3 c3 wire Rw=wire_memorycell_horizontal_res/"+str(numberofsrams)+" Cw=wire_memorycell_horizontal_cap/"+str(numberofsrams)+"\n")

	spice_file.write("X_inv_lookahead4_dummy_94   c3  c3b    n_vdd n_gnd inv   Wn=45n Wp=55n\n")

	# Sum
	spice_file.write("X_inv_lookahead4_dummy_11    prop_1 n_1    n_vdd n_gnd inv   Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_lookahead4_dummy_12  n_1    sumb1  c0b   cin    n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_lookahead4_dummy_13  prop_1 sumb1  cin    c0b   n_vdd n_gnd tgate Wn=45n Wp=55n\n")

	spice_file.write("X_inv_lookahead4_dummy_14    prop_2 n_2    n_vdd n_gnd inv   Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_lookahead4_dummy_15  n_2    sumb2  c1b   c1    n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_lookahead4_dummy_16  prop_2 sumb2  c1    c1b   n_vdd n_gnd tgate Wn=45n Wp=55n\n")

	spice_file.write("X_inv_lookahead4_dummy_17    prop_3 n_3    n_vdd n_gnd inv   Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_lookahead4_dummy_18  n_3    sumb3  c2b   c2    n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_lookahead4_dummy_19  prop_3 sumb3  c2    c2b   n_vdd n_gnd tgate Wn=45n Wp=55n\n")

	spice_file.write("X_inv_lookahead4_dummy_20    prop_4 n_4    n_vdd n_gnd inv   Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_lookahead4_dummy_21  n_4    sumb4  c3b   c3    n_vdd n_gnd tgate Wn=45n Wp=55n\n")
	spice_file.write("X_tgate_lookahead4_dummy_22  prop_4 sumb4  c3    c3b   n_vdd n_gnd tgate Wn=45n Wp=55n\n")

	spice_file.write("X_inv_lookahead4_dummy_31 sumb1  sum1  n_vdd n_gnd inv Wn=65n Wp=80n\n")
	spice_file.write("X_inv_lookahead4_dummy_32 sumb2  sum2  n_vdd n_gnd inv Wn=65n Wp=80n\n")
	spice_file.write("X_inv_lookahead4_dummy_33 sumb3  sum3  n_vdd n_gnd inv Wn=65n Wp=80n\n")
	spice_file.write("X_inv_lookahead4_dummy_34 sumb4  sum4  n_vdd n_gnd inv Wn=65n Wp=80n\n")

	# Carry lookahead generator
	spice_file.write("Xwire21 prop_1 prop_1_1 wire Rw=wire_memorycell_horizontal_res/"+str(numberofsrams/2)+" Cw=wire_memorycell_horizontal_cap/"+str(numberofsrams/2)+"\n")
	spice_file.write("Xwire22 prop_2 prop_2_2 wire Rw=wire_memorycell_horizontal_res/"+str(numberofsrams/2)+" Cw=wire_memorycell_horizontal_cap/"+str(numberofsrams/2)+"\n")
	spice_file.write("Xwire23 prop_3 prop_3_3 wire Rw=wire_memorycell_horizontal_res/"+str(numberofsrams/2)+" Cw=wire_memorycell_horizontal_cap/"+str(numberofsrams/2)+"\n")
	spice_file.write("Xwire24 prop_4 prop_4_4 wire Rw=wire_memorycell_horizontal_res/"+str(numberofsrams/2)+" Cw=wire_memorycell_horizontal_cap/"+str(numberofsrams/2)+"\n")
	spice_file.write("Xwire25 gen_1  gen_1_1  wire Rw=wire_memorycell_horizontal_res/"+str(numberofsrams/2)+" Cw=wire_memorycell_horizontal_cap/"+str(numberofsrams/2)+"\n")
	spice_file.write("Xwire26 gen_2  gen_2_2  wire Rw=wire_memorycell_horizontal_res/"+str(numberofsrams/2)+" Cw=wire_memorycell_horizontal_cap/"+str(numberofsrams/2)+"\n")
	spice_file.write("Xwire27 gen_3  gen_3_3  wire Rw=wire_memorycell_horizontal_res/"+str(numberofsrams/2)+" Cw=wire_memorycell_horizontal_cap/"+str(numberofsrams/2)+"\n")
	spice_file.write("Xwire28 gen_4  gen_4_4  wire Rw=wire_memorycell_horizontal_res/"+str(numberofsrams/2)+" Cw=wire_memorycell_horizontal_cap/"+str(numberofsrams/2)+"\n")

	spice_file.write("M11  n_vdd  gen_4_4 x3 n_vdd pmos L=gate_length W=inv_lookahead4_dummy_1_pmos ")
	spice_file.write("AS=inv_lookahead4_dummy_1_pmos*trans_diffusion_length AD=inv_lookahead4_dummy_1_pmos*trans_diffusion_length"+
										" PS=inv_lookahead4_dummy_1_pmos+2*trans_diffusion_length PD=inv_lookahead4_dummy_1_pmos+2*trans_diffusion_length\n")
	spice_file.write("M12  x3     gen_3_3 x2 n_vdd pmos L=gate_length W=inv_lookahead4_dummy_1_pmos ")
	spice_file.write("AS=inv_lookahead4_dummy_1_pmos*trans_diffusion_length AD=inv_lookahead4_dummy_1_pmos*trans_diffusion_length"+
										" PS=inv_lookahead4_dummy_1_pmos+2*trans_diffusion_length PD=inv_lookahead4_dummy_1_pmos+2*trans_diffusion_length\n")
	spice_file.write("M13  x2     gen_2_2 x1 n_vdd pmos L=gate_length W=inv_lookahead4_dummy_1_pmos ")
	spice_file.write("AS=inv_lookahead4_dummy_1_pmos*trans_diffusion_length AD=inv_lookahead4_dummy_1_pmos*trans_diffusion_length"+
										" PS=inv_lookahead4_dummy_1_pmos+2*trans_diffusion_length PD=inv_lookahead4_dummy_1_pmos+2*trans_diffusion_length\n")
	spice_file.write("M14  x1     gen_1_1 x0 n_vdd pmos L=gate_length W=inv_lookahead4_dummy_1_pmos ")
	spice_file.write("AS=inv_lookahead4_dummy_1_pmos*trans_diffusion_length AD=inv_lookahead4_dummy_1_pmos*trans_diffusion_length"+
										" PS=inv_lookahead4_dummy_1_pmos+2*trans_diffusion_length PD=inv_lookahead4_dummy_1_pmos+2*trans_diffusion_length\n")
	spice_file.write("M15  x0     cin  coutbar n_vdd pmos L=gate_length W=inv_lookahead4_dummy_1_pmos ")
	spice_file.write("AS=inv_lookahead4_dummy_1_pmos*trans_diffusion_length AD=inv_lookahead4_dummy_1_pmos*trans_diffusion_length"+
										" PS=inv_lookahead4_dummy_1_pmos+2*trans_diffusion_length PD=inv_lookahead4_dummy_1_pmos+2*trans_diffusion_length\n")

	spice_file.write("M21  n_vdd  prop_4_4  coutbar n_vdd pmos L=gate_length W=inv_lookahead4_dummy_2_pmos ")
	spice_file.write("AS=inv_lookahead4_dummy_2_pmos*trans_diffusion_length AD=inv_lookahead4_dummy_2_pmos*trans_diffusion_length"+
										" PS=inv_lookahead4_dummy_2_pmos+2*trans_diffusion_length PD=inv_lookahead4_dummy_2_pmos+2*trans_diffusion_length\n")
	spice_file.write("M22  x3     prop_3_3  coutbar n_vdd pmos L=gate_length W=inv_lookahead4_dummy_2_pmos ")
	spice_file.write("AS=inv_lookahead4_dummy_2_pmos*trans_diffusion_length AD=inv_lookahead4_dummy_2_pmos*trans_diffusion_length"+
										" PS=inv_lookahead4_dummy_2_pmos+2*trans_diffusion_length PD=inv_lookahead4_dummy_2_pmos+2*trans_diffusion_length\n")
	spice_file.write("M23  x2     prop_2_2  coutbar n_vdd pmos L=gate_length W=inv_lookahead4_dummy_2_pmos ")
	spice_file.write("AS=inv_lookahead4_dummy_2_pmos*trans_diffusion_length AD=inv_lookahead4_dummy_2_pmos*trans_diffusion_length"+
										" PS=inv_lookahead4_dummy_2_pmos+2*trans_diffusion_length PD=inv_lookahead4_dummy_2_pmos+2*trans_diffusion_length\n")
	spice_file.write("M24  x1     prop_1_1  coutbar n_vdd pmos L=gate_length W=inv_lookahead4_dummy_2_pmos ")
	spice_file.write("AS=inv_lookahead4_dummy_2_pmos*trans_diffusion_length AD=inv_lookahead4_dummy_2_pmos*trans_diffusion_length"+
										" PS=inv_lookahead4_dummy_2_pmos+2*trans_diffusion_length PD=inv_lookahead4_dummy_2_pmos+2*trans_diffusion_length\n")

	spice_file.write("M31  n_gnd  prop_4_4 y3 n_gnd nmos L=gate_length W=inv_lookahead4_dummy_1_nmos ")
	spice_file.write("AS=inv_lookahead4_dummy_1_nmos*trans_diffusion_length AD=inv_lookahead4_dummy_1_nmos*trans_diffusion_length"+
										" PS=inv_lookahead4_dummy_1_nmos+2*trans_diffusion_length PD=inv_lookahead4_dummy_1_nmos+2*trans_diffusion_length\n")
	spice_file.write("M32  y3     prop_3_3 y2 n_gnd nmos L=gate_length W=inv_lookahead4_dummy_1_nmos ")
	spice_file.write("AS=inv_lookahead4_dummy_1_nmos*trans_diffusion_length AD=inv_lookahead4_dummy_1_nmos*trans_diffusion_length"+
										" PS=inv_lookahead4_dummy_1_nmos+2*trans_diffusion_length PD=inv_lookahead4_dummy_1_nmos+2*trans_diffusion_length\n")
	spice_file.write("M33  y2     prop_2_2 y1 n_gnd nmos L=gate_length W=inv_lookahead4_dummy_1_nmos ")
	spice_file.write("AS=inv_lookahead4_dummy_1_nmos*trans_diffusion_length AD=inv_lookahead4_dummy_1_nmos*trans_diffusion_length"+
										" PS=inv_lookahead4_dummy_1_nmos+2*trans_diffusion_length PD=inv_lookahead4_dummy_1_nmos+2*trans_diffusion_length\n")
	spice_file.write("M34  y1     prop_1_1 y0 n_gnd nmos L=gate_length W=inv_lookahead4_dummy_1_nmos ")
	spice_file.write("AS=inv_lookahead4_dummy_1_nmos*trans_diffusion_length AD=inv_lookahead4_dummy_1_nmos*trans_diffusion_length"+
										" PS=inv_lookahead4_dummy_1_nmos+2*trans_diffusion_length PD=inv_lookahead4_dummy_1_nmos+2*trans_diffusion_length\n")
	spice_file.write("M35  y0     cin  coutbar n_gnd nmos L=gate_length W=inv_lookahead4_dummy_1_nmos ")
	spice_file.write("AS=inv_lookahead4_dummy_1_nmos*trans_diffusion_length AD=inv_lookahead4_dummy_1_nmos*trans_diffusion_length"+
										" PS=inv_lookahead4_dummy_1_nmos+2*trans_diffusion_length PD=inv_lookahead4_dummy_1_nmos+2*trans_diffusion_length\n")

	spice_file.write("M41  n_gnd  gen_4_4 coutbar n_gnd nmos L=gate_length W=inv_lookahead4_dummy_2_nmos ")
	spice_file.write("AS=inv_lookahead4_dummy_2_nmos*trans_diffusion_length AD=inv_lookahead4_dummy_2_nmos*trans_diffusion_length"+
										" PS=inv_lookahead4_dummy_2_nmos+2*trans_diffusion_length PD=inv_lookahead4_dummy_2_nmos+2*trans_diffusion_length\n")
	spice_file.write("M42  y3     gen_3_3 coutbar n_gnd nmos L=gate_length W=inv_lookahead4_dummy_2_nmos ")
	spice_file.write("AS=inv_lookahead4_dummy_2_nmos*trans_diffusion_length AD=inv_lookahead4_dummy_2_nmos*trans_diffusion_length"+
										" PS=inv_lookahead4_dummy_2_nmos+2*trans_diffusion_length PD=inv_lookahead4_dummy_2_nmos+2*trans_diffusion_length\n")
	spice_file.write("M43  y2     gen_2_2 coutbar n_gnd nmos L=gate_length W=inv_lookahead4_dummy_2_nmos ")
	spice_file.write("AS=inv_lookahead4_dummy_2_nmos*trans_diffusion_length AD=inv_lookahead4_dummy_2_nmos*trans_diffusion_length"+
										" PS=inv_lookahead4_dummy_2_nmos+2*trans_diffusion_length PD=inv_lookahead4_dummy_2_nmos+2*trans_diffusion_length\n")
	spice_file.write("M44  y1     gen_1_1 coutbar n_gnd nmos L=gate_length W=inv_lookahead4_dummy_2_nmos ")
	spice_file.write("AS=inv_lookahead4_dummy_2_nmos*trans_diffusion_length AD=inv_lookahead4_dummy_2_nmos*trans_diffusion_length"+
										" PS=inv_lookahead4_dummy_2_nmos+2*trans_diffusion_length PD=inv_lookahead4_dummy_2_nmos+2*trans_diffusion_length\n")

	spice_file.write("X_inv_lookahead4_dummy_40    coutbar cout_1    n_vdd n_gnd inv   Wn=inv_lookahead4_dummy_3_nmos Wp=inv_lookahead4_dummy_3_pmos\n")
	spice_file.write("Xwire31 cout_1  cout  wire Rw=wire_memorycell_horizontal_res/"+str(numberofsrams/2)+" Cw=wire_memorycell_horizontal_cap/"+str(numberofsrams/2)+"\n")

	# set up inputs
	spice_file.write("X_inv_lookahead4_dummy_51 ina3  a3b   n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_lookahead4_dummy_52 a3b   a3    n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_lookahead4_dummy_53 ina2  a2b   n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_lookahead4_dummy_54 a2b   a2    n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_lookahead4_dummy_55 ina1  a1b   n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_lookahead4_dummy_56 a1b   a1    n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_lookahead4_dummy_57 ina0  a0b   n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_lookahead4_dummy_58 a0b   a0    n_vdd n_gnd inv Wn=45n Wp=55n\n")

	spice_file.write("X_inv_lookahead4_dummy_61 inb3  b3b   n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_lookahead4_dummy_62 b3b   b3    n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_lookahead4_dummy_63 inb2  b2b   n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_lookahead4_dummy_64 b2b   b2    n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_lookahead4_dummy_65 inb1  b1b   n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_lookahead4_dummy_66 b1b   b1    n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_lookahead4_dummy_67 inb0  b0b   n_vdd n_gnd inv Wn=45n Wp=55n\n")
	spice_file.write("X_inv_lookahead4_dummy_68 b0b   b0    n_vdd n_gnd inv Wn=45n Wp=55n\n")
	
	spice_file.write(".ENDS\n\n\n")
	spice_file.close()

	tran_names_list = []
	tran_names_list.append("inv_lookahead4_dummy_1_nmos") # Lookahead generator 1, sizable, 5
	tran_names_list.append("inv_lookahead4_dummy_1_pmos") # Lookahead generator 1, sizable, 5
	tran_names_list.append("inv_lookahead4_dummy_2_nmos") # Lookahead generator 2, sizable, 4
	tran_names_list.append("inv_lookahead4_dummy_2_pmos") # Lookahead generator 2, sizable, 4
	tran_names_list.append("inv_lookahead4_dummy_3_nmos") # Lookahead generator 2, sizable, 1
	tran_names_list.append("inv_lookahead4_dummy_3_pmos") # Lookahead generator 2, sizable, 1
	#tran_names_list.append("inv_lookahead4_dummy_4_nmos") # inv, nand2 nor2, 45n, 22
	#tran_names_list.append("inv_lookahead4_dummy_4_pmos") # inv, nand2 nor2, 55n, 22
	#tran_names_list.append("tgate_lookahead4_dummy_5_nmos") # standard tgate, 45n, 22
	#tran_names_list.append("tgate_lookahead4_dummy_5_pmos") # standard tgate, 55n, 22
	#tran_names_list.append("inv_lookahead4_dummy_6_nmos") # cin, sum, bypass driver, 65n, 4
	#tran_names_list.append("inv_lookahead4_dummy_6_pmos") # cin, sum, bypass driver, 80n, 4

	wire_names_list = []

	return tran_names_list, wire_names_list


# Added by Yuzong Chen (yc2367@cornell.edu)
# This is the 2:1 mux circuit for BRAM-CIM dummy array. It consists of 2 transmission gates.
# We are going to disable 1 transmission gates for easier measurement of the delay.
# The pmos/nmos ratio is determined by the stardard cell pmos/nmos ratio in 28nm technology 
def generate_mux2_dummy_lp(spice_filename, circuit_name):

	# Open SPICE file for appending
	spice_file = open(spice_filename, 'a')
	# currently only works for 22nm
	spice_file.write("******************************************************************************************\n")
	spice_file.write("* " + circuit_name + " subcircuit dummy-array 2:1 mux \n")
	spice_file.write("******************************************************************************************\n")
	spice_file.write(".SUBCKT " + circuit_name + " n_in n_out n_gate_nmos n_gate_pmos n_vdd n_gnd\n")
	# I am going to disable two transmission gates in this
	spice_file.write("X_tgate_mux2_dummy_1   n_in   n_out  n_gate_nmos n_gate_pmos  n_vdd n_gnd tgate_lp Wn=45n Wp=90n\n")
	spice_file.write("X_tgate_mux2_dummy_2   n_vdd  n_out  n_gnd       n_vdd        n_vdd n_gnd tgate_lp Wn=45n Wp=90n\n")

	spice_file.write(".ENDS\n\n\n")
	spice_file.close()

	tran_names_list = []
	wire_names_list = []

	return tran_names_list, wire_names_list


# Added by Yuzong Chen (yc2367@cornell.edu)
# This is the 3:1 mux circuit for BRAM-CIM dummy array. It consists of 3 transmission gates.
# We are going to disable 2 transmission gates for easier measurement of the delay.
# The pmos/nmos ratio is determined by the stardard cell pmos/nmos ratio in 28nm technology 
def generate_mux3_dummy_lp(spice_filename, circuit_name):

	# Open SPICE file for appending
	spice_file = open(spice_filename, 'a')
	# currently only works for 22nm
	spice_file.write("******************************************************************************************\n")
	spice_file.write("* " + circuit_name + " subcircuit dummy-array 3:1 mux \n")
	spice_file.write("******************************************************************************************\n")
	spice_file.write(".SUBCKT " + circuit_name + " n_in n_out n_gate_nmos n_gate_pmos n_vdd n_gnd\n")
	# I am going to disable two transmission gates in this
	spice_file.write("X_tgate_mux3_dummy_1   n_in   n_out  n_gate_nmos n_gate_pmos  n_vdd n_gnd tgate_lp Wn=45n Wp=90n\n")
	spice_file.write("X_tgate_mux3_dummy_2   n_vdd  n_out  n_gnd       n_vdd        n_vdd n_gnd tgate_lp Wn=45n Wp=90n\n")
	spice_file.write("X_tgate_mux3_dummy_3   n_vdd  n_out  n_gnd       n_vdd        n_vdd n_gnd tgate_lp Wn=45n Wp=90n\n")

	spice_file.write(".ENDS\n\n\n")
	spice_file.close()

	tran_names_list = []
	wire_names_list = []

	return tran_names_list, wire_names_list