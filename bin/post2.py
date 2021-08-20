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
                
    mfr_mgps.append(1e3*post1['mfr_gps'])
    i_mean_ua.append(post1['i_mean_ua'])
    i_std_ua.append(post1['i_std_ua'])
    mfr_std_mgps.append(1./post1['duration_s'])

ax = lplot.init_fig('Carbon flow rate (mg/s)', 'Current ($\mu$A)', label_size=14)
ax.errorbar(mfr_mgps, i_mean_ua, yerr=i_std_ua, xerr=mfr_std_mgps, fmt='ko', mfc='k', lc=None, ecolor='k', elinewidth=1, capsize=6)
ax.get_figure().savefig('../export/im.png')

with open('../export/post2.param', 'w') as ff:
    for this in sys.argv:
        ff.write(this + ' ')
    ff.write('\n')
