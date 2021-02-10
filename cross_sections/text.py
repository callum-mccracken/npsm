"""for making images of state labels"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager
from matplotlib.ticker import MultipleLocator
mpl.rcParams['lines.linewidth'] = '2'
mpl.rcParams['axes.linewidth'] = '2'
mpl.rcParams['lines.dashed_pattern'] = (7, 2)
mpl.rcParams['lines.dotted_pattern'] = (1, 1.65)
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.weight"] = "bold"
plt.rc('text', usetex=True)
plt.rc('font', size=16)

j = "?"
pi = '?'
t = "?"

plt.text(0.2, 0.3, f"${j}^{pi}{t}$", fontsize=200)

plt.axis('off')
plt.savefig(f"?{pi}?.png", dpi=300, transparent=True)