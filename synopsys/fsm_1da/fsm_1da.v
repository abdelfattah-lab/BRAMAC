`include "defines.v" // Define key parameters

// BrAMAC instruction format
//  <DUMMY> <Input_2> <Input_1> <BRAM_COL_ADDR> <BRAM_ROW_ADDR_2> <BRAM_ROW_ADDR_1> <DONE> <COPY> <START> <RESET> <INTYPE> <PREC>
//  1 bit    8 bits    8 bits       2 bits           7 bits            7 bits       1 bit  1 bit   1 bit   1 bit   1 bit   2 bits                     
//  39       38:31     30:23        22:21            20:14              13:7          6      5       4       3       2      1:0
module fsm_1da (
  input  logic               clk,
  input  logic               comp_en,          // 1'b1 if M20K is in compute mode, 1'b0 otherwise   
  input  logic               reset_bram,       // Global BRAM reset
  input  logic [`DWIDTH-1:0] inst,             // BrAMAC instruction

  output logic               carry_in,         // Adder carry in, '0' for addition, '1' for subtraction

  output logic               ren_1_dummy,      // Dummy array read port 1 enable
  output logic               ren_2_dummy,      // Dummy array read port 2 enable
  output logic               wen_1_dummy,      // Dummy array write port 1 enable
  output logic               wen_2_dummy,      // Dummy array write port 2 enable
  output logic [2:0]         raddr_1_dummy,    // Dummy array read address 1
  output logic [2:0]         raddr_2_dummy,    // Dummy array read address 2
  output logic [2:0]         waddr_1_dummy,    // Dummy array write address 1
  output logic [2:0]         waddr_2_dummy,    // Dummy array write address 2
  output logic [1:0]         wsel_1_dummy,     // Dummy array write mux sel q
  output logic [1:0]         wsel_2_dummy,     // Dummy array write mux sel 2  

  output logic               readout_dummy     // Specify if read out dummy array accumulator
);

  logic       reset_dummy;
  logic       start;
  logic       done;
  logic       copy_en;
  logic [1:0] prec;
  //logic [6:0] ram_row;
  //logic [1:0] ram_col_1;
  //logic [1:0] ram_col_2;
  logic [7:0] input_2;
  logic [7:0] input_1;

  assign prec            = inst[1:0];
  assign in_type         = inst[2]; // Specify whether the input is signed (1'b1) or unsigned (1'b0)
  assign reset_dummy     = inst[3] && comp_en;
  assign start           = inst[4] && comp_en;
  assign copy_en         = inst[5] && comp_en;
  assign done            = inst[6] && comp_en;
  //assign ram_row_1     = inst[31:25];
  //assign ram_row_2     = inst[24:18];
  //assign ram_col       = inst[17:16];
  assign input_1         = inst[30:23];
  assign input_2         = inst[38:31];

  //----------------------------------------------------------------------
  // State Definitions
  //----------------------------------------------------------------------
  localparam STATE_IDLE     = 4'd0;  // Idle state, disable dummy array
  localparam STATE_INIT_ACC = 4'd1;  // Initialize accumulator to 0

  localparam STATE_COPY     = 4'd2;  // Read out W1 and W2 from BRAM and copy to two dummy array
                                     // also store input activations I1 and I2
  localparam STATE_PREADD   = 4'd3;  // Pre-add W1 and W2 in dummy array, also initialize Psum to 0
  localparam STATE_BUBBLE   = 4'd4;  // Bubble state for unsigned input activation
  localparam STATE_INV      = 4'd5;  // Inverting a row depending on the input activations
  localparam STATE_SUB      = 4'd6;  // Subtracting the inverted row from Psum
  localparam STATE_ASL      = 4'd7;  // Add-shift-left a row to psum depending on the input activations
  localparam STATE_ADD      = 4'd8;  // Add a row to psum depending on the input activations
  localparam STATE_ACC      = 4'd9;  // Add psum to accumulator
  localparam STATE_DONE_1   = 4'd10; // First half-cycle done, read out accumulator
  localparam STATE_DONE_2   = 4'd11; // Second half-cycle done, read out accumulator
  
  //----------------------------------------------------------------------
  // State
  //----------------------------------------------------------------------
  logic [3:0] state_now, state_next;
  logic [3:0] counter_now, counter_next;

  always_ff @( posedge clk ) begin
    if ( reset_dummy || reset_bram ) begin
      state_now    <= STATE_IDLE;
      counter_now  <= 0;
    end
    else begin
      state_now    <= state_next;
      counter_now  <= counter_next;
    end
  end

  //----------------------------------------------------------------------
  // Update MAC prec and Input Activations 
  //----------------------------------------------------------------------
  logic read_input;
  logic read_prec;
  logic read_intype;
  logic shift_input;
  
  assign read_input   = (state_now == STATE_INIT_ACC) || (state_now == STATE_ACC);
  assign read_prec    = (state_now == STATE_INIT_ACC);
  assign read_intype  = (state_now == STATE_INIT_ACC);
  assign shift_input  = (state_now == STATE_SUB) || (state_now == STATE_ASL);

  logic [7:0] input_dummy_1, input_dummy_2; // 2 input activations
  logic [1:0] mac_prec;
  logic       mac_intype;

  always_ff @( posedge clk ) begin
    if ( reset_dummy || reset_bram ) begin
      mac_prec       <= 2'b00;
      mac_intype     <= 1'b0;
      input_dummy_1  <= 8'd0;
      input_dummy_2  <= 8'd0;
    end
    else begin 
      if ( read_input ) begin
        input_dummy_1  <= input_1;
        input_dummy_2  <= input_2;
      end 
      else if ( shift_input ) begin   // Input stream bit by bit
        input_dummy_1  <= input_dummy_1 << 1'b1;
        input_dummy_2  <= input_dummy_2 << 1'b1;
      end
      if (read_prec) begin
        mac_prec <= prec;
      end
      if (read_intype) begin
        mac_intype <= in_type;
      end
    end
  end

  logic [3:0] mac_precision;

  always_comb begin
    if ( mac_prec == 2'b00 ) begin // undefined
      mac_precision = 4'd0;
    end
    else if ( mac_prec == 2'b01 ) begin // 2-bit prec
      mac_precision = 4'd2;
    end 
    else if ( mac_prec == 2'b10 ) begin // 4-bit prec
      mac_precision = 4'd4;
    end
    else if ( mac_prec == 2'b11 ) begin // 8-bit prec
      mac_precision = 4'd8;
    end
  end

  // Current MSB from input_1 and input_2, i.e. activation decoder
  logic [2:0] act_dec; 
  assign act_dec  = {1'b0, input_dummy_2[7], input_dummy_1[7]};

  //----------------------------------------------------------------------
  // State Transitions
  //----------------------------------------------------------------------
  logic start_mac;

  assign start_mac = start;

  always_comb begin
    // State transition logic
    case ( state_now )
      STATE_IDLE: 
        begin
          if ( start_mac ) begin    
            state_next    = STATE_INIT_ACC;
          end else begin
            state_next    = STATE_IDLE;
          end
          counter_next  = 0;
        end
      STATE_INIT_ACC: 
        begin
          state_next    = STATE_COPY;
          counter_next  = 0;
        end
      STATE_COPY: 
        begin
          state_next    = STATE_PREADD;
          counter_next  = 0;
        end
      STATE_PREADD: 
        begin
          if ( mac_intype == 1'b1 ) begin
            state_next    = STATE_INV;
          end else begin
            state_next    = STATE_BUBBLE;
          end
          counter_next  = counter_now + 1;
        end
      STATE_BUBBLE: 
        begin
          state_next    = STATE_ASL;
          counter_next  = counter_now + 1;
        end
      STATE_INV: 
        begin
          state_next    = STATE_SUB;
          counter_next  = counter_now + 1;
        end
      STATE_SUB: 
        begin
          if ( counter_now < mac_precision ) begin
            state_next    = STATE_ASL;
          end else begin
            state_next    = STATE_ADD;
          end
          counter_next  = counter_now + 1;
        end
      STATE_ASL: 
        begin
          if ( counter_now < mac_precision ) begin
            state_next    = STATE_ASL;
          end else begin
            state_next    = STATE_ADD;
          end
          counter_next  = counter_now + 1;
        end
      STATE_ADD: 
        begin
          state_next    = STATE_ACC;
          counter_next  = counter_now + 1;
        end
      STATE_ACC: 
        begin
          if ( done ) begin  
            state_next    = STATE_DONE_1;
          end else begin
            state_next    = STATE_COPY;
          end
          counter_next  = 0;
        end
      STATE_DONE_1: 
        begin          
          state_next    = STATE_DONE_2;
          counter_next  = 0;
        end
      STATE_DONE_2: 
        begin
          if ( reset_dummy ) begin 
            state_next    = STATE_IDLE;
          end else if (start_mac) begin
            state_next    = STATE_COPY;
          end else begin            
            state_next    = STATE_DONE_1;
          end 
          counter_next  = 0;
        end
      default: 
        begin
          state_next    = STATE_IDLE;
          counter_next  = 0;
        end
    endcase
  end

  //----------------------------------------------------------------------
  // State Outputs
  //----------------------------------------------------------------------
  function void cs
    (
      input logic       cs_carry_in,
      input logic       cs_ren_1_dummy,
      input logic       cs_ren_2_dummy,
      input logic       cs_wen_1_dummy,
      input logic       cs_wen_2_dummy,
      input logic [2:0] cs_raddr_1_dummy,
      input logic [2:0] cs_raddr_2_dummy,
      input logic [2:0] cs_waddr_1_dummy,
      input logic [2:0] cs_waddr_2_dummy,
      input logic [1:0] cs_wsel_1_dummy,
      input logic [1:0] cs_wsel_2_dummy,
      input logic       cs_readout_dummy
    );
    begin
      carry_in        = cs_carry_in;
      ren_1_dummy     = cs_ren_1_dummy;
      ren_2_dummy     = cs_ren_2_dummy;
      wen_1_dummy     = cs_wen_1_dummy;
      wen_2_dummy     = cs_wen_2_dummy;
      raddr_1_dummy   = cs_raddr_1_dummy;
      raddr_2_dummy   = cs_raddr_2_dummy;
      waddr_1_dummy   = cs_waddr_1_dummy;
      waddr_2_dummy   = cs_waddr_2_dummy;
      wsel_1_dummy    = cs_wsel_1_dummy;
      wsel_2_dummy    = cs_wsel_2_dummy;
      readout_dummy   = cs_readout_dummy;
    end
  endfunction
  
  // Local parameters for dummy array row address
  localparam addr_x    = 3'bx;
  localparam addr_0    = 3'd0;
  localparam addr_w1   = 3'd1;
  localparam addr_w2   = 3'd2;
  localparam addr_w12  = 3'd3;
  localparam addr_inv  = 3'd4;
  localparam addr_psum = 3'd5;
  localparam addr_acc  = 3'd6;

  localparam sel_sum   = 2'd0;
  localparam sel_sumr  = 2'd1;
  localparam sel_ram1  = 2'd2;  

  localparam sel_0     = 2'd0;
  localparam sel_inv   = 2'd1;
  localparam sel_ram2  = 2'd2;

  // Set outputs using a control signal "table"

  always_comb begin
    case ( state_now ) 
      //                        carry   ren  ren  wen  wen  raddr1     raddr2     waddr       waddr     wsel      wsel     read_acc
      //                           in    1    2    1    2   dummy1     dummy1        1          2        1         2       dummy
      STATE_IDLE:            cs(   0,    0,   0,   0,   0,  addr_x,    addr_x,    addr_x,    addr_x,    2'bx,     2'bx,     0   );
      STATE_INIT_ACC:        cs(   0,    0,   0,   0,   1,  addr_x,    addr_x,    addr_x,    addr_acc,  2'bx,     sel_0,    0   );
      STATE_COPY:            cs(   0,    0,   0,   1,   1,  addr_x,    addr_x,    addr_w1,   addr_w2,   sel_ram1, sel_ram2, 0   );

      STATE_PREADD:          cs(   0,    1,   1,   1,   1,  addr_w1,   addr_w2,   addr_w12,  addr_psum, sel_sum,  sel_0,    0   );
      STATE_BUBBLE:          cs(   0,    0,   0,   0,   0,  addr_x,    addr_x,    addr_x,    addr_x,    2'bx,     2'bx,     0   );
      STATE_INV:             cs(   0,    1,   0,   0,   1,  act_dec,   addr_x,    addr_x,    addr_inv,  2'bx,     sel_inv,  0   );
      STATE_SUB:             cs(   1,    1,   1,   1,   0,  addr_inv,  addr_psum, addr_psum, addr_x,    sel_sum,  2'bx,     0   );
      STATE_ASL:             cs(   0,    1,   1,   1,   0,  act_dec,   addr_psum, addr_psum, addr_x,    sel_sumr, 2'bx,     0   );
      STATE_ADD:             cs(   0,    1,   1,   1,   0,  act_dec,   addr_psum, addr_psum, addr_x,    sel_sum,  2'bx,     0   );
      STATE_ACC:             cs(   0,    1,   1,   1,   0,  addr_psum, addr_acc,  addr_acc,  addr_x,    sel_sum,  2'bx,     0   );
      
      STATE_DONE_1:          cs(   0,    0,   0,   0,   0,  addr_x,    addr_x,    addr_x,    addr_x,    2'bx,     2'bx,     0   );
      STATE_DONE_2:          
        if (start_mac)       cs(   0,    0,   1,   0,   1,  addr_x,    addr_acc,  addr_x,    addr_acc,  2'bx,     2'bx,     1   );
        else                 cs(   0,    0,   1,   0,   0,  addr_x,    addr_acc,  addr_x,    addr_x,    2'bx,     2'bx,     1   );

      default                cs(   0,    0,   0,   0,   0,  addr_x,    addr_x,    addr_x,    addr_x,    2'bx,     2'bx,     0   );
    endcase
  end

endmodule