"""
Generate a 2D infotaxis trajectory as the insect flies through a basic plume.

The settings and parameters of this demo are located in config/basic_plume_2d.py.
"""

import numpy as np
import matplotlib.pyplot as plt
plt.ion()

from insect import Insect
from plume import BasicPlume
from trial import Trial
from plotting import plume_and_traj_3d as plot_trial

from config.basic_plume_2d import *


# create plume
pl = BasicPlume(env=ENV, dt=DT)
pl.set_params(**PLUME_PARAMS)
pl.set_src_pos(SRCPOS, is_idx=True)

# create insect
ins = Insect(env=ENV, dt=DT)
ins.set_params(**PLUME_PARAMS)
ins.loglike_function = LOGLIKE
ins.set_pos(STARTPOS, is_idx=True)

# create trial
pl.initialize()
ins.initialize()
nsteps = int(np.floor(RUNTIME/DT))

trial = Trial(pl=pl, ins=ins, nsteps=nsteps)

# open figure and axes
_, axs = plt.subplots(3, 1, **PLOTKWARGS)
plt.draw()

# run trial, plotting along the way if necessary
for step in xrange(nsteps):
    trial.step()
    if (step % PLOTEVERY == 0) or (step == nsteps - 2):
        plot_trial(axs, trial)
        plt.draw()

    if trial.at_src:
        print 'Found source!'
        break

    if PAUSEEVERY:
        if step % PAUSEEVERY == 0:
            raw_input('Press enter to continue...')

raw_input()