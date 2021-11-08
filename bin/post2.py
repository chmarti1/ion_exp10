#!/usr/bin/python3


import numpy as np
import lconfig as lc
import matplotlib.pyplot as plt
import os,sys
import lplot


datadir = '../data'
threshold = 40.
####

mfr_mgps = []
i_mean_ua = []
i_std_ua = []
mfr_std_mgps = []

with open('../export/post2.dat', 'w') as f2:
    f2.write('# Sourcedir  C(mg/s)  C_std(mg/s)  I(uA)  I_std(uA)\n')
    # Loop through the included datasets
    for arg in sys.argv[1:]:
        sourcedir = None
        for this in os.listdir(datadir):
            if this.endswith(arg):
                if sourcedir:
                    raise Exception(f'POST1.PY: found multiple data entries that end with {arg}')
                sourcedir = os.path.join(datadir,this)
        # Load the post1 results    
        post1_param = os.path.join(sourcedir, 'post1', 'post1.param')
        post1 = {}
        with open(post1_param, 'r') as ff:
            for thisline in ff:
                if not thisline.isspace():
                    param,value = thisline.split()
                    value = float(value)
                    post1[param] = value
        
        mfr = 1e3*post1['mfr_gps']
        mfr_std = 1./post1['duration_s']
        mfr_mgps.append(mfr)
        i_mean_ua.append(post1['i_mean_ua'])
        i_std_ua.append(post1['i_std_ua'])
        mfr_std_mgps.append(mfr_std)
        f2.write(f'{sourcedir}\t{mfr}\t{mfr_std}\t{post1["i_mean_ua"]}\t{post1["i_std_ua"]}\n')

C = np.polyfit(mfr_mgps, i_mean_ua, 1)
x = np.linspace(0,30,21)
y = np.polyval(C,x)

ax = lplot.init_fig('Carbon flow rate (mg/s)', 'Current ($\mu$A)', label_size=14)
ax.errorbar(mfr_mgps, i_mean_ua, yerr=i_std_ua, xerr=mfr_std_mgps, fmt='ko', mfc='k', lc=None, ecolor='k', elinewidth=1, capsize=6)
ax.plot(x,y,'k--')
ax.text(2,160,f'y = {C[0]:.3f} x + {C[1]:.3f}',fontsize=14,backgroundcolor='w')
ax.get_figure().savefig('../export/im.png')

with open('../export/post2.param', 'w') as ff:
    for this in sys.argv:
        ff.write(this + ' ')
    ff.write('\n')
