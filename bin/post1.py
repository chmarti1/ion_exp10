#!/usr/bin/python3

import numpy as np
import lconfig as lc
import matplotlib.pyplot as plt
import os,sys
from multiprocessing import Pool
import lplot

def worker(target):
    print(target)
    os.system(f'./post1.py quiet force {target}')

#
# These are lines of code you may want to edit before running post.py
#
datadir = '../data'
threshold = 40.
####


force = 'force' in sys.argv[1:]
quiet = 'quiet' in sys.argv[1:]
arg = sys.argv[-1]
sourcedir = None

if arg == 'all':
    contents = os.listdir(datadir)
    contents.sort()
    with Pool(processes=8) as pool:
       pool.map(worker, contents)
    exit(0)

for this in os.listdir(datadir):
    if this.endswith(arg):
        if sourcedir:
            raise Exception(f'POST1.PY: found multiple data entries that end with {arg}')
        sourcedir = os.path.join(datadir,this)
        
if not quiet:
    print('Working on: ' + sourcedir)


source = os.path.join(sourcedir,'burn.dat')

# Check for prior post1 results
# Make the post1 directory if it doesn't already exist
targetdir = os.path.join(sourcedir, 'post1')
if os.path.isdir(targetdir):
    if not force and 'y' != input('Overwrite previous post1 results? (y/n):'):
        raise Exception('Disallowed from overwriting prior post1 results')
    os.system(f'rm -rf {targetdir}')
os.mkdir(targetdir)

# LOAD DATA!
data = lc.LConf(source, data=True, cal=True)

# Get channels
voltage = data.get_channel(1)
current = data.get_channel(0)
t = data.get_time()

# Get the parameters
m1 = data.get_meta(0,'weight1_g')
m2 = data.get_meta(0, 'weight2_g')
m_g = m1 - m2

# Find the signal
I = current > threshold

start = 0
stop = 0
N = 10
count = 0
# Filter for start and stop
# The start must be True for at least N samples
for index, value in enumerate(I):
    # If we haven't found the starting index yet
    if start == 0:
        if value:
            count += 1
            if count == N:
                start = index - N
                count = 0
        else:
            count = 0
    elif stop == 0:
        if value:
            count = 0
        else:
            count += 1
            if count == N:
                stop = index - N
                count = 0

if start == 0 or stop == 0:
    raise Exception(f'Failed to find a trigger signal on {arg}.')

# What was the test duration?
duration_s = t[stop] - t[start]
# Get the mean current signal
i_mean_ua = np.mean(current[start:stop])
i_std_ua = np.std(current[start:stop])

# mass flow rate
mfr_gps = m_g / duration_s

target = os.path.join(targetdir, 'post1.param')
with open(target, 'w') as ff:
    ff.write(f'start_s {t[start]}\n')
    ff.write(f'stop_s {t[stop]}\n')
    ff.write(f'mass_g {m_g}\n')
    ff.write(f'duration_s {duration_s}\n')
    ff.write(f'mfr_gps {mfr_gps}\n')
    ff.write(f'i_mean_ua {i_mean_ua}\n')
    ff.write(f'i_std_ua {i_std_ua}\n')
    ff.write(f'\n')


target = os.path.join(targetdir, 'total.png')
f = plt.figure(1, figsize=(6,4))
f.clf()
ax = f.subplots(1,1)
ax.plot(t, current)
ax.set_xlabel('Time (s)', fontsize=14)
ax.set_ylabel('Current (uA)', fontsize=14)
ax.grid(True)
f.savefig(target)

target = os.path.join(targetdir, 'signal.png')
f = plt.figure(1, figsize=(6,4))
f.clf()
ax = f.subplots(1,1)
ax.plot(t[start:stop], current[start:stop])
ax.set_xlabel('Time (s)', fontsize=14)
ax.set_ylabel('Current (uA)', fontsize=14)
ax.grid(True)
f.savefig(target)
