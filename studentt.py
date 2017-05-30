import sys
import numpy as np
from scipy.stats import t
import matplotlib.pyplot as plt
import myrootlib2 as mrl

fig, ax = plt.subplots(1, 1)

x = np.linspace(-10, 10, 1000)
y = mrl.fitfunc_studentt(x, 0.0, 11, 1e6)
plt.plot(x, y)


plt.savefig(sys.argv[0][:-3] + '.pdf')
