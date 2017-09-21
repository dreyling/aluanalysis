import sys
import numpy as np
import matplotlib.pyplot as plt

import my_fitfuncs as mff


fig, ax = plt.subplots(1, 1)

x = np.linspace(-10, 10, 1000)

y = mff.fitfunc_studentt(x, 0.0, 1., 1)
plt.plot(x, y, label='Students t (standard.)')

y = mff.fitfunc_gauss(x, 0.0, 1, 0.5)
plt.plot(x, y, label='Gauss, height = 0.5')

y = mff.fitfunc_gauss_normed(x, 0.0, 1)
plt.plot(x, y, label='Gauss normed')

y = mff.fitfunc_studentt_nonstand_normed(x, 0.0, 1., 1.)
plt.plot(x, y, label='Students t (non-standard.)', ls='--', lw=5)

y = mff.fitfunc_combined_gauss_studentt(x, 0.0, 1., 1., 1., 0.5, 1.)
plt.plot(x, y, label='Combined (50:50)', ls=':', lw=3)

plt.legend()

plt.savefig('output/' + sys.argv[0][:-3] + '.pdf')
