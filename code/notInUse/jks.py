import numpy as np
import jenkspy
import matplotlib.pyplot as plt

normal = np.random.normal(loc=0.0, scale=1.0, size=100)

plt.figure(figsize = (10,8))
hist = plt.hist(normal, align='left', color='g')

breaks = jenkspy.jenks_breaks(normal, nb_class=10)
print(breaks)

for b in breaks:
    plt.vlines(b, ymin=0, ymax = max(hist[0]))
plt.show()
print(normal)