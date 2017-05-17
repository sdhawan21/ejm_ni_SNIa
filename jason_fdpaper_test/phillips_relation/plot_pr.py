import numpy as np
import matplotlib.pyplot as plt

valfile = np.loadtxt('pr_vals.txt', skiprows=1, usecols = (1, 3, 4, 6, 8))

mb = valfile[:,0] - valfile[:,1] - 4.1*(valfile[:,2]+valfile[:,3])

sbv = valfile[:,-1]

plt.plot(sbv, mb, 'rs')
plt.show()
