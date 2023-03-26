import numpy as np
import pandas as pd
import math
import argparse

parser = argparse.ArgumentParser(description='Process network type: alexnet or resnet. \n')
parser.add_argument('--nn_type', type=str, required=True, default='alexnet',
                    help='Provide network type: alexnet or resnet. \n')

args = parser.parse_args()
nn_type = args.nn_type

######### M20K Configuration ##########
num_bram_row    = 128                                # Number of rows in a M20K
num_bram_col    = 160                                # Number of columns in a M20K
bram_mux_factor = 4                                  # M20K has a 4:1 mux
bram_dwidth     = num_bram_col // bram_mux_factor    # M20K data width
num_bram        = 1500
num_dsp         = 1518
precision_list  = [2, 4, 8]

# The network layer definition is in the form of (r, s, c, p, q, k)
# where
# r = filter width
# s = filter height
# c = input  channel
# p = output height
# q = output width
# k = output channel

######### AlexNet definition ##########

alexnet_dla = [('conv', [3, 3, 48, 55, 55, 96]), 
               ('conv', [5, 5, 96, 27, 27, 256]),
               ('conv', [3, 3, 256, 13, 13, 384]),
               ('conv', [3, 3, 384, 13, 13, 384]),
               ('conv', [3, 3, 384, 13, 13, 256]),
               ('fc', [4096, 4096]),
               ('fc', [4096, 4096]),
               ('fc', [4096, 1000])
               ]

alexnet_dlabramac = [('conv', [3, 1, 128, 55, 55, 96]), 
                     ('conv', [5, 5, 96, 27, 27, 256]),
                     ('conv', [3, 3, 256, 13, 13, 384]),
                     ('conv', [3, 3, 384, 13, 13, 384]),
                     ('conv', [3, 3, 384, 13, 13, 256]),
                     ('fc', [4096, 4096]),
                     ('fc', [4096, 4096]),
                     ('fc', [4096, 1000])
                    ]

alexnet_iofmap = [[227, 227, 3, 55, 55, 96],
                  [55, 55, 96, 27, 27, 96],
                  [27, 27, 96, 27, 27, 256],
                  [27, 27, 256, 13, 13, 256],
                  [13, 13, 256, 13, 13, 384],
                  [13, 13, 384, 13, 13, 384],
                  [13, 13, 384, 13, 13, 256],
                 ]

######### ResNet-34 definition #########

resnet_dla = [('conv', [3, 1, 49, 112, 112, 64]), 
              
              # ResnetBlock(64)
               ('conv', [3, 3, 64, 56, 56, 64]),
               ('conv', [3, 3, 64, 56, 56, 64]),
              # ResnetBlock(64)
               ('conv', [3, 3, 64, 56, 56, 64]),
               ('conv', [3, 3, 64, 56, 56, 64]),
              # ResnetBlock(64)
               ('conv', [3, 3, 64, 56, 56, 64]),
               ('conv', [3, 3, 64, 56, 56, 64]),

              # ResnetBlock(128)
               ('conv', [3, 3, 64,  28, 28, 128]),
               ('conv', [3, 3, 128, 28, 28, 128]),
               ('conv', [3, 1, 64,  28, 28, 43]), # 1x1 conv
              # ResnetBlock(128)
               ('conv', [3, 3, 128, 28, 28, 128]),
               ('conv', [3, 3, 128, 28, 28, 128]),
              # ResnetBlock(128)
               ('conv', [3, 3, 128, 28, 28, 128]),
               ('conv', [3, 3, 128, 28, 28, 128]),
              # ResnetBlock(128)
               ('conv', [3, 3, 128, 28, 28, 128]),
               ('conv', [3, 3, 128, 28, 28, 128]),
              
              # ResnetBlock(256)
               ('conv', [3, 3, 128, 14, 14, 256]),
               ('conv', [3, 3, 256, 14, 14, 256]),
               ('conv', [3, 1, 128, 14, 14, 86]), # 1x1 conv
              # ResnetBlock(256)
               ('conv', [3, 3, 256, 14, 14, 256]),
               ('conv', [3, 3, 256, 14, 14, 256]),
              # ResnetBlock(256)
               ('conv', [3, 3, 256, 14, 14, 256]),
               ('conv', [3, 3, 256, 14, 14, 256]),
              # ResnetBlock(256)
               ('conv', [3, 3, 256, 14, 14, 256]),
               ('conv', [3, 3, 256, 14, 14, 256]),
              # ResnetBlock(256)
               ('conv', [3, 3, 256, 14, 14, 256]),
               ('conv', [3, 3, 256, 14, 14, 256]),
              # ResnetBlock(256)
               ('conv', [3, 3, 256, 14, 14, 256]),
               ('conv', [3, 3, 256, 14, 14, 256]),            
              
              # ResnetBlock(512)
               ('conv', [3, 3, 256, 7,  7,  512]),
               ('conv', [3, 3, 512, 7,  7,  512]),
               ('conv', [3, 1, 256, 7,  7,  171]), # 1x1 conv
              # ResnetBlock(512)
               ('conv', [3, 3, 512, 7,  7,  512]),
               ('conv', [3, 3, 512, 7,  7,  512]),        
              # ResnetBlock(512)
               ('conv', [3, 3, 512, 7,  7,  512]),
               ('conv', [3, 3, 512, 7,  7,  512]),

               ('fc', [1000, 512]),
               ]

resnet_dlabramac = [('conv', [3, 1, 49, 112, 112, 64]), 

                    # ResnetBlock(64)
                    ('conv', [3, 3, 64, 56, 56, 64]),
                    ('conv', [3, 3, 64, 56, 56, 64]),
                    # ResnetBlock(64)
                    ('conv', [3, 3, 64, 56, 56, 64]),
                    ('conv', [3, 3, 64, 56, 56, 64]),
                    # ResnetBlock(64)
                    ('conv', [3, 3, 64, 56, 56, 64]),
                    ('conv', [3, 3, 64, 56, 56, 64]),

                    # ResnetBlock(128)
                    ('conv', [3, 3, 64,  28, 28, 128]),
                    ('conv', [3, 3, 128, 28, 28, 128]),
                    ('conv', [3, 1, 64,  28, 28, 43]), # 1x1 conv
                    # ResnetBlock(128)
                    ('conv', [3, 3, 128, 28, 28, 128]),
                    ('conv', [3, 3, 128, 28, 28, 128]),
                    # ResnetBlock(128)
                    ('conv', [3, 3, 128, 28, 28, 128]),
                    ('conv', [3, 3, 128, 28, 28, 128]),
                    # ResnetBlock(128)
                    ('conv', [3, 3, 128, 28, 28, 128]),
                    ('conv', [3, 3, 128, 28, 28, 128]),

                    # ResnetBlock(256)
                    ('conv', [3, 3, 128, 14, 14, 256]),
                    ('conv', [3, 3, 256, 14, 14, 256]),
                    ('conv', [3, 1, 128, 14, 14, 86]), # 1x1 conv
                    # ResnetBlock(256)
                    ('conv', [3, 3, 256, 14, 14, 256]),
                    ('conv', [3, 3, 256, 14, 14, 256]),
                    # ResnetBlock(256)
                    ('conv', [3, 3, 256, 14, 14, 256]),
                    ('conv', [3, 3, 256, 14, 14, 256]),
                    # ResnetBlock(256)
                    ('conv', [3, 3, 256, 14, 14, 256]),
                    ('conv', [3, 3, 256, 14, 14, 256]),
                    # ResnetBlock(256)
                    ('conv', [3, 3, 256, 14, 14, 256]),
                    ('conv', [3, 3, 256, 14, 14, 256]),
                    # ResnetBlock(256)
                    ('conv', [3, 3, 256, 14, 14, 256]),
                    ('conv', [3, 3, 256, 14, 14, 256]),            

                    # ResnetBlock(512)
                    ('conv', [3, 3, 256, 7,  7,  512]),
                    ('conv', [3, 3, 512, 7,  7,  512]),
                    ('conv', [3, 1, 256, 7,  7,  171]), # 1x1 conv
                    # ResnetBlock(512)
                    ('conv', [3, 3, 512, 7,  7,  512]),
                    ('conv', [3, 3, 512, 7,  7,  512]),        
                    # ResnetBlock(512)
                    ('conv', [3, 3, 512, 7,  7,  512]),
                    ('conv', [3, 3, 512, 7,  7,  512]),

                    ('fc', [1000, 512]),
                    ]

resnet_iofmap = [[56,  56,  64,  56, 56, 64],
                 [56,  56,  64,  28, 28, 128],
                 [28,  28,  128, 28, 28, 128],
                 [28,  28,  128, 14, 14, 256],
                 [14,  14,  256, 14, 14, 256],
                 [14,  14,  256, 7,  7,  512],
                 [7,   7,   512, 7,  7,  512],
                ]

if nn_type == 'alexnet':
    nn_dla = alexnet_dla
    ifmap_ofmap_size = alexnet_iofmap
    nn_dlabramac = alexnet_dlabramac
elif nn_type == 'resnet':
    nn_dla = resnet_dla
    ifmap_ofmap_size = resnet_iofmap
    nn_dlabramac = resnet_dlabramac

def calc_dla_area(num_bram, num_dsp, precision=8):
    return ( num_bram*40 + num_dsp*30 )

def calc_dlabramac_area(num_bram, num_dsp, precision=8):
    return ( num_bram*40*1.17 + num_dsp*30 )

class DLA(object):
    def __init__(self, qvec=2, cvec=8, kvec=48, rvec=3, lw=1, lh=1,
                 num_dsp=num_dsp, num_bram_row=num_bram_row, num_bram_col=num_bram_col, bram_dwidth=32, precision=8):
        super(DLA, self).__init__()
        self.qvec         = qvec
        self.cvec         = cvec
        self.kvec         = kvec
        self.rvec         = rvec
        self.lw           = lw
        self.lh           = lh
        self.num_bram_row = num_bram_row
        self.num_bram_col = num_bram_col
        self.bram_dwidth  = bram_dwidth
        self.precision    = precision
        self.num_multiplier_per_dsp = {2: 8, 4: 4, 8: 2} # Apply DSP packing
    
    def count_dsp(self):
        return math.ceil( ( self.qvec * self.rvec * self.cvec * self.kvec ) 
                         / self.num_multiplier_per_dsp[self.precision] )
 
    def count_streambuf_bram(self, cin, pin, qin, cout, pout, qout, network_type='alexnet'):
        if ( network_type != 'alexnet' ) and ( network_type != 'resnet' ):
            raise Exception('Currently, the stream buffer model only supports alexnet and resnet !')
            
        ifmap_width = (self.qvec - 1) * math.ceil( qout/qin ) + self.rvec
        num_bank    = ifmap_width * self.cvec
        
        if network_type == 'alexnet':
            ifmap_depth = math.ceil( (cin*pin*qin + cout*pout*qout) / num_bank )
        elif network_type == 'resnet':
            ifmap_depth = math.ceil( (cin*pin*qin + 2*cout*pout*qout) / num_bank )
            
        bram_depth  = self.num_bram_row * 4 * (32 / self.precision)
        return math.ceil( ifmap_depth / bram_depth ) * num_bank
    
    def count_fcache_bram(self, r, s, c, k):
        num_row_bram   = self.num_bram_row
        num_depth_bram = 4
        num_bram_rvec  = self.rvec
        num_cvec_per_data = self.bram_dwidth / self.precision
        num_bram_cvec_kvec = math.ceil(num_bram_rvec * self.cvec / num_cvec_per_data) * self.kvec
        num_bram_r     = math.ceil( r / self.rvec )
        num_bram_s     = s       
        num_bram_c     = math.ceil( c / self.cvec )
        num_bram_k     = math.ceil( k / self.kvec )
        num_bram_c_s_k = math.ceil( (num_bram_r * num_bram_s * num_bram_c * num_bram_k) / 
                                   (num_depth_bram * num_row_bram) )
        return ( num_bram_cvec_kvec * num_bram_c_s_k )

    def dsp_eff(self, r, s, c, p, q, k):
        eff =  q / ( math.ceil(q / (self.qvec*self.lw)) * self.qvec * self.lw ) * \
                p / ( math.ceil(p / self.lh) * self.lh ) * \
                k / ( math.ceil(k / self.kvec) * self.kvec ) * \
                c / ( math.ceil(c / self.cvec) * self.cvec ) * \
                r / ( math.ceil(r / self.rvec) * self.rvec )
        return eff
    
    def count_convlayer_cycle(self, r, s, c, p, q, k):
        num_flop  = 2 * r * s * c * p * q * k / self.dsp_eff(r, s, c, p, q, k)
        num_cycle = num_flop / ( 2*self.count_dsp()*self.num_multiplier_per_dsp[self.precision] )
        return math.ceil(num_cycle)
    
    def count_fclayer_cycle(self, c, k):
        batch_size = self.kvec * 2
        num_flop  = 2 * c * k * batch_size
        num_cycle = num_flop / ( 2*self.count_dsp()*self.num_multiplier_per_dsp[self.precision] )
        return math.ceil(num_cycle / batch_size)   

class DLA_BRAMAC(object):
    def __init__(self, qvec=2, cvec=12, kvec=60, rvec=3, svec=1, lw=1, lh=1,
                 num_dsp=num_dsp, num_bramac=num_bram, 
                 num_bram_row=num_bram_row, num_bram_col=num_bram_col, bram_dwidth=bram_dwidth, precision=8):
        super(DLA_BRAMAC, self).__init__()
        self.qvec         = qvec
        self.cvec         = cvec
        self.kvec         = math.floor( math.ceil(kvec / (bram_dwidth / precision)) * (bram_dwidth / precision) )
        self.rvec         = rvec
        self.svec         = svec
        self.lw           = lw
        self.lh           = lh
        self.num_dsp      = num_dsp
        self.num_bramac   = num_bramac
        self.num_bram_row = num_bram_row
        self.num_bram_col = num_bram_col
        self.bram_dwidth  = bram_dwidth
        self.precision    = precision

        self.num_multiplier_per_dsp = {2: 8, 4: 4, 8: 2} 
        
        self.num_mac_per_bramac_per_iter = {2: bram_dwidth//2*2, 4: bram_dwidth//4*2, 8: bram_dwidth//8*2}
        self.bramac_num_cycle_per_iter   = {2: 3,  4: 4,  8: 6}
        self.dsp_num_idle_cycle_per_iter = {2: 3,  4: 4,  8: 6}
        
        if self.qvec == 4:
            # Since 2-bit precision will give very high parallelism at kvec, which is not
            # suitable for ResNet whose first (also the most comute-intensive) block has K=64,
            # we increase the bramac computation parallelism along qvec by duplicating the model
            # storage. This effectively duplicate the number of dummy arrays to support computing
            # 2 outputs like BRAMAC-2SA
            if self.precision == 2: 
                self.bramac_qvec = 2
                self.dsp_qvec    = 2
            else:
                self.bramac_qvec = 1
                self.dsp_qvec    = 3
        elif self.qvec == 3:
            self.bramac_qvec = 1
            self.dsp_qvec    = 2
        elif self.qvec == 2:
            self.bramac_qvec = 1
            self.dsp_qvec    = 1
        else: 
            raise Exception('ERROR! Qvec can only be 2, 3 or 4 !!!')
            
        self.partition_workload()

        dsp_num_mac_per_cycle     = {}
        self.dsp_num_mac_per_iter = {}
                
        #bramac_num_mac_per_cycle = {}
        self.bramac_num_mac_per_iter  = {}
        for n in [2, 4, 8]:
            self.bramac_num_mac_per_iter[n]  = self.count_fcache_bram() * self.num_mac_per_bramac_per_iter[n]
            #bramac_num_mac_per_cycle[n]      = self.bramac_num_mac_per_iter[n] / self.bramac_num_cycle_per_iter[n]
            dsp_num_mac_per_cycle[n]         = self.count_dsp() * self.num_multiplier_per_dsp[n]
            self.dsp_num_mac_per_iter[n]     = dsp_num_mac_per_cycle[n] * self.dsp_num_idle_cycle_per_iter[n]

    def partition_workload(self):
        n = self.precision
        self.dsp_cvec_per_iter = self.dsp_num_idle_cycle_per_iter[n] * self.cvec
        
        self.bramac_cvec_per_iter = self.dsp_cvec_per_iter
        self.bramac_kvec_per_iter = self.kvec
        self.cvec_per_iter        = self.dsp_cvec_per_iter
        self.kvec_per_iter        = self.kvec

    def count_dsp(self):
        return math.ceil( ( self.dsp_qvec * self.rvec * self.cvec * self.kvec ) 
                         / self.num_multiplier_per_dsp[self.precision] )
    
    def count_streambuf_bram(self, cin, pin, qin, cout, pout, qout, network_type='alexnet'):
        if ( network_type != 'alexnet' ) and ( network_type != 'resnet' ):
            raise Exception('Currently, the stream buffer model only supports alexnet and resnet !')
            
        ifmap_width = (self.qvec - 1) * math.ceil( qout/qin ) + self.rvec
        num_bank    = ifmap_width * self.cvec
        
        if network_type == 'alexnet':
            ifmap_depth = math.ceil( (cin*pin*qin + cout*pout*qout) / num_bank )
        elif network_type == 'resnet':
            ifmap_depth = math.ceil( (cin*pin*qin + 2*cout*pout*qout) / num_bank )
            
        bram_depth  = self.num_bram_row * 4 * (32 / self.precision)
        return math.ceil( ifmap_depth / bram_depth ) * num_bank

    def count_fcache_bram(self):
        return math.ceil(self.bramac_cvec_per_iter / 2) * self.rvec * self.bramac_qvec * \
                math.ceil( self.bramac_kvec_per_iter / (self.bram_dwidth / self.precision) )
    
    def count_convlayer_cycle(self, r, s, c, p, q, k):
        n = self.precision
        num_iter_cvec  = math.ceil(c / self.cvec_per_iter)
        num_cycle_cvec = num_iter_cvec * self.bramac_num_cycle_per_iter[n] 
        num_cycle_read_acc = 4
        num_iter_kvec  = math.ceil(k / self.kvec_per_iter)
        num_cycle      = ( num_cycle_cvec * s * math.ceil(r / self.rvec) + num_cycle_read_acc ) * num_iter_kvec * \
                         ( math.ceil(q / (self.qvec*self.lw)) ) * \
                         ( math.ceil(p / self.lh) )

        return math.ceil(num_cycle)
    
    def count_fclayer_cycle(self, c, k):
        n = self.precision
        batch_size = self.kvec * 2
        num_flop  = 2 * c * k * batch_size
        num_mac_per_iter = self.dsp_num_mac_per_iter[n] + self.bramac_num_mac_per_iter[n]
        num_cycle = num_flop / (2*num_mac_per_iter) * self.bramac_num_cycle_per_iter[n]
        return math.ceil(num_cycle / batch_size)  

def calc_dla_performance(precision=8, nn_dla=None, 
                         num_dsp=1518, num_bram=1500,
                         ifmap_ofmap_size=None, network_type='alexnet'):
    if nn_dla == None or ifmap_ofmap_size == None:
        raise Exception('Please provide a correct neural network topology !')
        return
    if ( network_type != 'alexnet' ) and ( network_type != 'resnet' ):
        raise Exception('Please provide a valid network type: alexnet ot resnet !')
        return
    
    if precision == 8:
        dla = DLA(lw=1, lh=1, precision=precision, qvec=2, cvec=4, kvec=48)
    elif precision == 4:
        dla = DLA(lw=1, lh=1, precision=precision, qvec=2, cvec=8, kvec=48)
    elif precision == 2:
        dla = DLA(lw=1, lh=1, precision=precision, qvec=4, cvec=8, kvec=48)
    
    dla_latency = {}
    count = 1
    
    streambuf_dla_layer = {'cin': 0, 'pin': 0, 'qin': 0, 'cout': 0, 'pout': 0, 'qout': 0}
    for iofmap_size in ifmap_ofmap_size:
        pin  = iofmap_size[0]
        qin  = iofmap_size[1]
        cin  = iofmap_size[2]
        pout = iofmap_size[3]
        qout = iofmap_size[4]
        cout = iofmap_size[5]
        
        current_ifmap_depth = streambuf_dla_layer['cin']*streambuf_dla_layer['pin']*streambuf_dla_layer['qin'] + \
                            streambuf_dla_layer['cout']*streambuf_dla_layer['pout']*streambuf_dla_layer['qout']
        if ( pin*qin*cin + pout*qout*cout ) > current_ifmap_depth:
            streambuf_dla_layer['pin']  = pin
            streambuf_dla_layer['qin']  = qin
            streambuf_dla_layer['cin']  = cin
            streambuf_dla_layer['pout'] = pout
            streambuf_dla_layer['qout'] = qout
            streambuf_dla_layer['cout'] = cout
    
    fcache_dla_layer = {'r': 0, 's': 0, 'c': 0, 'k': 0} 
    for layer_type, config in nn_dla:
        if layer_type == 'conv':
            r = config[0]
            s = config[1]
            c = config[2]
            p = config[3]
            q = config[4]
            k = config[5]
            
            if ( r*s*c*k ) > ( fcache_dla_layer['r'] * fcache_dla_layer['s'] * 
                              fcache_dla_layer['c'] * fcache_dla_layer['k'] ):
                fcache_dla_layer['r'] = r
                fcache_dla_layer['s'] = s
                fcache_dla_layer['c'] = c
                fcache_dla_layer['k'] = k
            
            layer_name = 'conv_' + str(count)
            dla_latency[layer_name] = dla.count_convlayer_cycle(r, s, c, p, q, k)
        elif layer_type == 'fc':
            c = config[0]
            k = config[1]
            
            layer_name = 'fc_' + str(count)
            dla_latency[layer_name] = dla.count_fclayer_cycle(c, k)
        else:
            raise Exception("NN layer type can only be 'conv' or 'fc' !")
        
        count += 1
    
    dla_latency_total = sum(dla_latency.values())

    # The filter cache size is determined by Conv 4 layer of AlexNet
    num_fcache_bram_dla    = dla.count_fcache_bram(r=fcache_dla_layer['r'], s=fcache_dla_layer['s'], 
                                            c=fcache_dla_layer['c'], k=fcache_dla_layer['k'])
    num_streambuf_bram_dla = dla.count_streambuf_bram(cin=streambuf_dla_layer['cin'], 
                                                      pin=streambuf_dla_layer['pin'],
                                                      qin=streambuf_dla_layer['qin'],
                                                      cout=streambuf_dla_layer['cout'],
                                                      pout=streambuf_dla_layer['pout'],
                                                      qout=streambuf_dla_layer['qout'],
                                                      network_type=network_type
                                                     )
    dla_area           = calc_dla_area(num_bram=num_fcache_bram_dla + num_streambuf_bram_dla, 
                                      num_dsp=dla.count_dsp(), precision=precision)
    
    qvec_list    = []
    cvec_list    = []
    kvec_list    = []
    
    speedup_list = {}
    for key in dla_latency:
        speedup_list[key] = []
    
    speedup_total_list    = []
    area_ratio_list       = []
    speedup_per_area_list = []

    qf_list = []
    
    num_streambuf_bram_list = []
    num_fcache_bram_list    = []
    num_dsp_list            = []
    
    # qvec constraint due to dsp packing
    if precision == 8 or precision == 4:
        qvec_searchspace = [1,2,3,4]
    else:
        qvec_searchspace = [2,4]

    for qvec in qvec_searchspace:
        for cvec in range(4, 17, 2):
            for kvec in range(4, 100, 2):
                mem_invalid = ( ((kvec / cvec) % 2) != 0 )
                dlanew = DLA(lw=1, lh=1, 
                             precision=precision, qvec=qvec, cvec=cvec, kvec=kvec)
                num_fcache_bram    = dlanew.count_fcache_bram(r=fcache_dla_layer['r'], s=fcache_dla_layer['s'], 
                                    c=fcache_dla_layer['c'], k=fcache_dla_layer['k'])
                if (dlanew.count_dsp() > num_dsp) or (num_fcache_bram > num_bram) or mem_invalid:
                    continue

                count = 1
                dlanew_latency_total = 0

                for layer_type, config in nn_dla:
                    if layer_type == 'conv':
                        r = config[0]
                        s = config[1]
                        c = config[2]
                        p = config[3]
                        q = config[4]
                        k = config[5]

                        layer_name = 'conv_' + str(count)
                        layer_latency_dlanew = dlanew.count_convlayer_cycle(r, s, c, p, q, k) 
                        speedup_list[layer_name].append( dla_latency[layer_name] / layer_latency_dlanew )
                        dlanew_latency_total += layer_latency_dlanew
                    elif layer_type == 'fc':
                        c = config[0]
                        k = config[1]

                        layer_name = 'fc_' + str(count)
                        layer_latency_dlanew = dlanew.count_fclayer_cycle(c, k)
                        speedup_list[layer_name].append( dla_latency[layer_name] / layer_latency_dlanew )
                        dlanew_latency_total += layer_latency_dlanew
                    else:
                        raise Exception("NN layer type can only be 'conv' or 'fc' !")

                    count += 1
                    # Assume we don't use BrAMAC to accelerate Conv 1 layer
                    #dla_tmp = DLA(lw=1, lh=1, precision=precision, qvec=qvec, cvec=cvec, kvec=kvec)
                    #dla_tmp_conv1_latency   = dla_tmp.count_convlayer_cycle(3, 3, 42, 55, 55, 96)
                
                num_fcache_bram    = dlanew.count_fcache_bram(r=fcache_dla_layer['r'], s=fcache_dla_layer['s'], 
                                                                c=fcache_dla_layer['c'], k=fcache_dla_layer['k'])
                num_streambuf_bram = dlanew.count_streambuf_bram(cin=streambuf_dla_layer['cin'], 
                                                                  pin=streambuf_dla_layer['pin'],
                                                                  qin=streambuf_dla_layer['qin'],
                                                                  cout=streambuf_dla_layer['cout'],
                                                                  pout=streambuf_dla_layer['pout'],
                                                                  qout=streambuf_dla_layer['qout'],
                                                                  network_type=network_type
                                                                 )
                dlanew_area     = calc_dla_area(num_bram=num_fcache_bram + num_streambuf_bram, 
                                                 num_dsp=dlanew.count_dsp(), precision=precision)
                
                speedup_total = dla_latency_total / dlanew_latency_total
                
                num_streambuf_bram_list.append(num_streambuf_bram)
                num_fcache_bram_list.append(num_fcache_bram)
                num_dsp_list.append(dlanew.count_dsp())
                
                qvec_list.append(qvec)
                cvec_list.append(cvec)
                kvec_list.append(kvec)

                area_ratio = dlanew_area / dla_area
                area_ratio_list.append(area_ratio)

                speedup_per_area = speedup_total / area_ratio
                if speedup_total > 1:
                    speedup_per_area_list.append(speedup_per_area)
                    qf_list.append(speedup_total * speedup_per_area)
                else:
                    speedup_per_area_list.append(0)
                    qf_list.append(0)

                speedup_total_list.append(speedup_total)

    result_dict = {'qvec': qvec_list, 'cvec': cvec_list, 'kvec': kvec_list, 
                   'num_streambuf_bram': num_streambuf_bram_list, 'num_fcache_bram': num_fcache_bram_list, 
                   'num_dsp': num_dsp_list,
                   'speedup_total': speedup_total_list, 'area_ratio': area_ratio_list, 
                   'speedup_per_area': speedup_per_area_list, 'qf': qf_list}
    for key in speedup_list:
        result_dict[key] = speedup_list[key]

    df = pd.DataFrame(result_dict)
    df_result = df.sort_values(by='qf', axis=0, ascending=False)
    
    return df_result.iloc[0,:].to_dict()


dla_config = {}

for precision in precision_list:
    dla_config[precision] = calc_dla_performance(precision=precision, nn_dla=nn_dla, 
                                                 num_dsp=num_dsp, num_bram=num_bram,
                                                 ifmap_ofmap_size=ifmap_ofmap_size, 
                                                 network_type=nn_type)

def calc_dlabramac_performance(precision=8, dla_config={},
                               nn_dla=None, nn_dlabramac=None, 
                               num_dsp=num_dsp, num_bramac=num_bram,
                               num_bram_col=num_bram_col, bram_dwidth=bram_dwidth, 
                               ifmap_ofmap_size=None, network_type='alexnet'):
    if nn_dla == None or nn_dlabramac == None or ifmap_ofmap_size == None:
        raise Exception('Please provide a correct neural network topology !')
        return
    if ( network_type != 'alexnet' ) and ( network_type != 'resnet' ):
        raise Exception('Please provide a valid network type: alexnet ot resnet !')
        return
    if dla_config == {}:
        raise Exception('Please provide a valid DLA configuration for comparison with DLA-BRAMAC !')
        return
        
    dla_qvec = int(dla_config[precision]['qvec'])
    dla_cvec = int(dla_config[precision]['cvec'])
    dla_kvec = int(dla_config[precision]['kvec'])
    dla = DLA(lw=1, lh=1, precision=precision, qvec=dla_qvec, cvec=dla_cvec, kvec=dla_kvec)

    dla_latency = {}
    count = 1
    
    streambuf_dla_layer = {'cin': 0, 'pin': 0, 'qin': 0, 'cout': 0, 'pout': 0, 'qout': 0}
    for iofmap_size in ifmap_ofmap_size:
        pin  = iofmap_size[0]
        qin  = iofmap_size[1]
        cin  = iofmap_size[2]
        pout = iofmap_size[3]
        qout = iofmap_size[4]
        cout = iofmap_size[5]
        
        current_ifmap_depth = streambuf_dla_layer['cin']*streambuf_dla_layer['pin']*streambuf_dla_layer['qin'] + \
                            streambuf_dla_layer['cout']*streambuf_dla_layer['pout']*streambuf_dla_layer['qout']
        if ( pin*qin*cin + pout*qout*cout ) > current_ifmap_depth:
            streambuf_dla_layer['pin']  = pin
            streambuf_dla_layer['qin']  = qin
            streambuf_dla_layer['cin']  = cin
            streambuf_dla_layer['pout'] = pout
            streambuf_dla_layer['qout'] = qout
            streambuf_dla_layer['cout'] = cout
    
    fcache_dla_layer = {'r': 0, 's': 0, 'c': 0, 'k': 0} 
    for layer_type, config in nn_dla:
        if layer_type == 'conv':
            r = config[0]
            s = config[1]
            c = config[2]
            p = config[3]
            q = config[4]
            k = config[5]
            
            if ( r*s*c*k ) > ( fcache_dla_layer['r'] * fcache_dla_layer['s'] * \
                              fcache_dla_layer['c'] * fcache_dla_layer['k'] ):
                fcache_dla_layer['r'] = r
                fcache_dla_layer['s'] = s
                fcache_dla_layer['c'] = c
                fcache_dla_layer['k'] = k
            
            layer_name = 'conv_' + str(count)
            dla_latency[layer_name] = dla.count_convlayer_cycle(r, s, c, p, q, k)
        elif layer_type == 'fc':
            c = config[0]
            k = config[1]
            
            layer_name = 'fc_' + str(count)
            dla_latency[layer_name] = dla.count_fclayer_cycle(c, k)
        else:
            raise Exception("NN layer type can only be 'conv' or 'fc' !")
        
        count += 1
    
    dla_latency_total = sum(dla_latency.values())

    # The filter cache size is determined by Conv 4 layer of AlexNet
    num_fcache_bram_dla    = dla.count_fcache_bram(r=fcache_dla_layer['r'], s=fcache_dla_layer['s'], 
                                            c=fcache_dla_layer['c'], k=fcache_dla_layer['k'])
    num_streambuf_bram_dla = dla.count_streambuf_bram(cin=streambuf_dla_layer['cin'], 
                                                      pin=streambuf_dla_layer['pin'],
                                                      qin=streambuf_dla_layer['qin'],
                                                      cout=streambuf_dla_layer['cout'],
                                                      pout=streambuf_dla_layer['pout'],
                                                      qout=streambuf_dla_layer['qout'],
                                                      network_type=network_type
                                                     )
    dla_area           = calc_dla_area(num_bram=num_fcache_bram_dla + num_streambuf_bram_dla, 
                                      num_dsp=dla.count_dsp(), precision=precision)
    
    qvec_list    = []
    cvec_list    = []
    kvec_list    = []
    
    num_streambuf_bram_list = []
    num_fcache_bram_list    = []
    num_dsp_list            = []
    
    speedup_list = {}
    for key in dla_latency:
        speedup_list[key] = []
    
    speedup_total_list    = []
    area_ratio_list       = []
    speedup_per_area_list = []

    qf_list = []
    
    qvec_searchspace = [2, 3, 4]

    kvec_step    = bram_dwidth // precision
    kvec_lbound  = kvec_step * 2
    kvec_ubound  = kvec_step * 30
        
    for qvec in qvec_searchspace:
        for cvec in range(4, 65, 2):
            for kvec in range(kvec_lbound, kvec_ubound, kvec_step):
                dlabramac = DLA_BRAMAC(lw=1, lh=1,
                                       num_dsp=num_dsp, num_bramac=num_bram, 
                                       num_bram_col=num_bram_col, bram_dwidth=bram_dwidth,
                                       precision=precision, qvec=qvec, cvec=cvec, kvec=kvec)
                num_fcache_bram    = dlabramac.count_fcache_bram()
                if num_fcache_bram < num_fcache_bram_dla:
                    num_fcache_bram = math.ceil( num_fcache_bram_dla/num_fcache_bram ) * num_fcache_bram
                if dlabramac.count_dsp() > dlabramac.num_dsp or num_fcache_bram > num_bramac:
                    continue

                count = 1
                dlabramac_latency_total = 0

                for layer_type, config in nn_dlabramac:
                    if layer_type == 'conv':
                        r = config[0]
                        s = config[1]
                        c = config[2]
                        p = config[3]
                        q = config[4]
                        k = config[5]

                        layer_name = 'conv_' + str(count)
                        layer_latency_dlabramac = dlabramac.count_convlayer_cycle(r, s, c, p, q, k) 
                        speedup_list[layer_name].append( dla_latency[layer_name] / layer_latency_dlabramac )
                        dlabramac_latency_total += layer_latency_dlabramac
                    elif layer_type == 'fc':
                        c = config[0]
                        k = config[1]

                        layer_name = 'fc_' + str(count)
                        layer_latency_dlabramac = dlabramac.count_fclayer_cycle(c, k)
                        speedup_list[layer_name].append( dla_latency[layer_name] / layer_latency_dlabramac )
                        dlabramac_latency_total += layer_latency_dlabramac
                    else:
                        raise Exception("NN layer type can only be 'conv' or 'fc' !")

                    count += 1
                    # Assume we don't use BrAMAC to accelerate Conv 1 layer
                    #dla_tmp = DLA(lw=1, lh=1, precision=precision, qvec=qvec, cvec=cvec, kvec=kvec)
                    #dla_tmp_conv1_latency   = dla_tmp.count_convlayer_cycle(3, 3, 42, 55, 55, 96)

                num_streambuf_bram = dlabramac.count_streambuf_bram(cin=streambuf_dla_layer['cin'], 
                                                                    pin=streambuf_dla_layer['pin'],
                                                                    qin=streambuf_dla_layer['qin'],
                                                                    cout=streambuf_dla_layer['cout'],
                                                                    pout=streambuf_dla_layer['pout'],
                                                                    qout=streambuf_dla_layer['qout'],
                                                                    network_type=network_type
                                                                   )
                dlabramac_area     = calc_dlabramac_area(num_bram=num_fcache_bram + num_streambuf_bram, 
                                                        num_dsp=dlabramac.count_dsp(), precision=precision)
                
                speedup_total = dla_latency_total / dlabramac_latency_total

                num_streambuf_bram_list.append(num_streambuf_bram)
                num_fcache_bram_list.append(num_fcache_bram)
                num_dsp_list.append(dlabramac.count_dsp())
                
                qvec_list.append(qvec)
                cvec_list.append(cvec)
                kvec_list.append(kvec)

                area_ratio = dlabramac_area / dla_area
                area_ratio_list.append(area_ratio)

                speedup_per_area = speedup_total / area_ratio
                if speedup_total > 1:
                    speedup_per_area_list.append(speedup_per_area)
                    qf_list.append(speedup_total * speedup_per_area)
                else:
                    speedup_per_area_list.append(0)
                    qf_list.append(0)

                speedup_total_list.append(speedup_total)

    result_dict = {'qvec': qvec_list, 'cvec': cvec_list, 'kvec': kvec_list, 
                   'num_streambuf_bram': num_streambuf_bram_list, 'num_fcache_bram': num_fcache_bram_list, 
                   'num_dsp': num_dsp_list,
                   'speedup_total': speedup_total_list, 'area_ratio': area_ratio_list, 
                   'speedup_per_area': speedup_per_area_list, 'qf': qf_list}
    for key in speedup_list:
        result_dict[key] = speedup_list[key]

    df = pd.DataFrame(result_dict)
    df_result = df.sort_values(by='qf', axis=0, ascending=False)
    
    return df_result.iloc[0,:].to_dict()


qvec_dlabramac = {}
cvec_dlabramac = {}
kvec_dlabramac = {}
numdsp_dlabramac = {}
numbram_dlabramac = {}

speedup_total    = {}
area_ratio       = {}
speedup_total    = {}
speedup_per_area = {}

for precision in precision_list:
    dlabramac_config = calc_dlabramac_performance(precision=precision, dla_config=dla_config, 
                                                  num_dsp=num_dsp, num_bramac=num_bram,
                                                  num_bram_col=num_bram_col, bram_dwidth=bram_dwidth,
                                                  network_type=nn_type, 
                                                  nn_dla=nn_dla, nn_dlabramac=nn_dlabramac, 
                                                  ifmap_ofmap_size=alexnet_iofmap)
    qvec_dlabramac[precision]    = int(dlabramac_config['qvec'])
    cvec_dlabramac[precision]    = int(dlabramac_config['cvec'])
    kvec_dlabramac[precision]    = int(dlabramac_config['kvec'])
    numdsp_dlabramac[precision]  = int(dlabramac_config['num_dsp'])
    numbram_dlabramac[precision] = int(dlabramac_config['num_streambuf_bram']) + int(dlabramac_config['num_fcache_bram'])
    speedup_total[precision]     = round(dlabramac_config['speedup_total'], 2)
    area_ratio[precision]        = round(dlabramac_config['area_ratio'], 2)
    speedup_per_area[precision]  = round(dlabramac_config['speedup_per_area'], 2)
    
    

with open('bramac_1da_speedup.txt', 'w') as f:
    f.write('DLA Configuration \n\n')
    f.write('Prec'.ljust(8) + 'qvec'.ljust(6) + 'cvec'.ljust(6) + 'kvec'.ljust(6) + 
            'num_dsp'.ljust(10) + 'num_bram'.ljust(11) + '\n')
    for precision in precision_list:
        qvec = str(int(dla_config[precision]['qvec']))
        cvec = str(int(dla_config[precision]['cvec']))
        kvec = str(int(dla_config[precision]['kvec']))
        numdsp  = str(int(dla_config[precision]['num_dsp']))
        numbram = str(int(dla_config[precision]['num_streambuf_bram']) + int(dla_config[precision]['num_fcache_bram']))
        
        f.write(str(str(precision)+'-bit').ljust(8) + 
                qvec.ljust(6) + cvec.ljust(6) + kvec.ljust(6) + 
                numdsp.ljust(10) + numbram.ljust(11) + '\n')
        
    f.write('\n\n')
    f.write('DLA-BRAMAC Configuration \n\n')
    f.write('Prec'.ljust(8) + 'qvec'.ljust(6) + 'cvec'.ljust(6) + 'kvec'.ljust(6) + 
            'num_dsp'.ljust(10) + 'num_bram'.ljust(11) +
            'Speedup'.ljust(10) + 'AreaRatio'.ljust(13) + 'Speedup/Area'.ljust(15) + '\n')
    for precision in precision_list:
        qvec = str(qvec_dlabramac[precision])
        cvec = str(cvec_dlabramac[precision])
        kvec = str(kvec_dlabramac[precision])
        numdsp  = str(numdsp_dlabramac[precision])
        numbram = str(numbram_dlabramac[precision])
        speedup   = str(speedup_total[precision])
        areaRatio = str(area_ratio[precision])
        speedupPerArea = str(speedup_per_area[precision])
        
        f.write(str(str(precision)+'-bit').ljust(8) + 
                qvec.ljust(6) + cvec.ljust(6) + kvec.ljust(6) + 
                numdsp.ljust(10) + numbram.ljust(11) + 
                speedup.ljust(10) + areaRatio.ljust(13) + speedupPerArea.ljust(15) + '\n')

