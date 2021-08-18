#!/usr/bin/python3

import os,sys
import time

data_dir = '../data'

target = os.path.join(data_dir, time.strftime('%Y%m%d%H%M%S'))
flowfile = os.path.join(target, 'flow.dat')
burnfile = os.path.join(target, 'burn')

# Make the target directory
os.mkdir(target)

# Prompt the user for input
go_f = True
while go_f:
    standoff_in = float(input('Standoff (in):'))
    cut_o2_psig = float(input('Cutting O2 pressure (psig):'))
    n2_psig = float(input('Fluidizer N2 pressure (psig):'))
    weight1_g = float(input('Carbon weight before test (g):'))
    print('Are the above entries correct?')
    go_f = not (input('(Y/n):') == 'Y')

# Run the flow measurement
print('Flow measurement')
os.system('lcburst -c flow.conf -d ' + flowfile)

# Run the measurement
print('Measuring...')
os.system(f'lcrun -c burn.conf -d {burnfile} -f n2_psig={n2_psig} -f weight1_g={weight1_g} -f weight2_g={0.0} -f standoff_in={standoff_in} -f cut_o2_psig={cut_o2_psig}')
