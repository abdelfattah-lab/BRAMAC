
# BRAMAC-Artifacts

This github repository contains necessary artifacts for our paper: 
>Y. Chen, and M. Abdelfattah,
>"**BRAMAC: Compute-in-BRAM Architectures for Multiply-Accumulate on FPGAs**",
>to appear in _Proceedings of the 31st IEEE International Symposium On Field-Programmable Custom Computing Machines (FCCM)_, May 2023.

## Overview
This repository includes three folders corresponding to three artifacts, respectively that capture the area, frequency, and performance of BRAMAC, a compute-in-BRAM architecture that can support efficient multiply-accumulate on FPGAs. 

The first artifact, **COFFE-CIM**, is a modified version of COFFE (https://github.com/vaughnbetz/COFFE), with additional features to describe and model the additional peripheral circuits in BRAMAC. We use COFFE-CIM to evaluate the area and frequency of BRAMAC's dummy array (described in Section V-B and Section V-C of the paper). 

The second artifact, **dlabramac**, is a cycle-accurate simulator to compare the performance of Intel's Deep Learning Accelerator (Aydonat et al., FPGA'17; Abdelfattah et al., FPL'18) with and without employing BRAMAC. Two popular concolutional neural networks, AlexNet and ResNet-34 are evaluated (described in Section VI-D of the paper). 

The second artifact, **dlabramac**, is a cycle-accurate simulator to compare the performance of Intel's Deep Learning Accelerator (Aydonat et al., FPGA'17; Abdelfattah et al., FPL'18) with and without employing BRAMAC. Two popular concolutional neural networks, AlexNet and ResNet-34 are evaluated (described in Section VI-D of the paper). 

The third artifact, **synopsys**, contains the systemVerilog scripts to model and synthesize the embedded finite-state machines (eFSMs) that control BRAMAC's in-memory MAC2 operation. In addition to Synopsys Design COmpiler, TSMC 28nm techonology PDK is required for synthesize the eFSMs. We are not able to disclose any information about the technology PDK due to non-disclosure agreement with the third party. But we encourage users to synthesize the systemVerilog using their commercial or free PDKs or an FPGA CAD flow such as Intel Quartus to extimate the area cost of the eFSMs, which can be negligible compared to the dummy array area overhead (described in Section V-A and Section V-C of the paper).

## Tested Environment & Dependencies
OS requirement:
- CentOS Linux 7 (or above)

For running the first and second artifacts, **COFFE-CIM** and **dlabramac**, the following softwares are required. 
- Python 2.7
- Python 3.6 (numpy, pandas required)
- Bash 4.2
- Synopsys Hspice 2013.03 (or above)

If you decide to run the third artifact, **synopsys**, the following tools are required.
- Synopsys Design Compiler (we used verision 2022.03-sp5, but a lower verision is also expected to work).
- TSMC 28nm PDK and a corresponding tcl file to setup the Synopsys Design Compiler environment. We set the target frequency to be 2.5 GHz, i.e., a clock period of 0.4 ns.
- (Optional) Can use Intel Quartus to estimate the area cost by importing the systemVerilog scripts to a Quartus project.

## Summary of Artifact Executions
Run the following command in Terminal to clone this github repository:
 ```
 git clone https://github.com/abdelfattah-lab/BRAMAC.git
 ```

There are 3 tasks required to collect the area, frequency, and performance of BRAMAC
1. Run **COFFE-CIM** to obtain the area and delay of different components of BRAMAC. 
2. Run scripts in **dlabramac** to obtain the speedup of employing BRAMAC to Intel DLA for AlexNet and ResNet-34.
3. Run synopsys design compiler to obtain the area of the embedded finite-state machines in BRAMAC.

## 1. Running COFFE-CIM
COFFE-CIM can report the area and delay of all components in BRAMAC by running the following commands inside the BRAMAC repository:
 ```
 cd COFFE-CIM
 python2 coffe.py -i 6 input_files/CIM/RAM16_CIM.txt
 python2 coffe.py -i 6 input_files/CIM/RAM32_CIM.txt 
 ```
The two python2 commands evaluate BRAMAC based on 16Kb and 32Kb baseline BRAMs. Each of the two COFFE-CIM experiments takes roughly 12 hours to complete depending on the computer's performance. After completing, users can view the reported delay and area by running the following commands inside the BRAMAC repository:
 ```
 cd COFFE-CIM/input_files/CIM/RAM16_CIM
 open report.txt 
 cd COFFE-CIM/input_files/CIM/RAM32_CIM
 open report.txt 
 ```
The first **report.txt** file is for a 16Kb baseline BRAM, while the second **report.txt** file is for a 32Kb baseline BRAM. The dummy array area information is inside the **report.txt** file, under **DUMMY ARRAY AREA CONTRIBUTIONS**. Note that the reported dummy array area contains two dummy arrays. The user should divide the area number by 2 to obtain the area of one dummy array as in the paper. 
To estimate the dummy array area of a 20Kb baseline BRAM, the user can do a linear interpolating between 16kb and 32kb cases: **area_20Kb = area_16Kb + (area_32Kb - area_16Kb)/4**. 

## 2. Running DLA-BRAMAC
The scripts under **dlabramac** can report the speedup and area overhead of DLA-BRAMAC comapred to the baseline DLA by running the following commands inside the BRAMAC repository:
 ```
 cd dlabramac
 python3 dlabramac_2sa.py --nn_type alexnet
 python3 dlabramac_2sa.py --nn_type resnet
 python3 dlabramac_1da.py --nn_type alexnet
 python3 dlabramac_1da.py --nn_type resnet
 ```
Each two python3 commands evaluate a BRAMAC variant (2sa or 1da) for a specific network (alexnet or resnet), and will generate a **.txt** file to summarize the speedup and area overhead pf DLA-BRAMAC under different MAC precisions. 

## 3. Synthesizing the Embedded Finite-State Machine
To run this experiment in the BRAMAC repository, Synopsys Design COmpiler and a commercial Technology PDK is required. We are not able to disclose any information about the technology PDK due to non-disclosure agreement with the third party. But we encourage users to synthesize the systemVerilog using their commercial or free PDKs. We give an example on how to synthesize the embedded finite-state machine for BRAMAC-2SA. The process for synthesize the embedded finite-state machine for BRAMAC-1DA is similar. 

In addition to setting up the target library, the link library, the user can add the following two commands in their Synopsys Design Compiler tcl setup file.  
 ```
 <commands to set up target_library and link_library, leaving for the users>

 analyze -format sverilog synopsys/fsm_2sa/fsm_2sa.v
 elaborate fsm_2sa
 check_design
 create_clock clk -name ideal_clock1 -period 0.4
 compile

 write -format verilog -hierarchy -output post-synth.v
 write -format ddc     -hierarchy -output post-synth.ddc
 report_resources -nosplit -hierarchy
 report_timing -nosplit -transition_time -nets -attributes
 report_area -nosplit -hierarchy
 report_power -nosplit -hierarchy
 ```
After running Synopsys Design COmpiler with the above tcl setup file, the area of the embedded finite-state machine will be reported. 