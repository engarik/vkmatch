import numpy as np
import matplotlib.pyplot as plt
import random

fig, ax = plt.subplots()

ref_p = [np.array([0, 0]), np.array([1, 0]), np.array([0, 1]), np.array([1, 1]), np.array([0, 0.5]), np.array([0.5, 0]),
         np.array([1, 0.5]), np.array([0.5, 1])]
rand_point = np.random.rand(2)

points = []

dots = np.array(ref_p)
cur_point = rand_point

for i in range(100000):
    rand_int = random.randint(0, 7)
    cur_point = (cur_point + 2 * ref_p[rand_int]) / 3
    points.append(cur_point)

to_draw = np.array(points)
ax.plot()
ax.scatter(to_draw[:, 0], to_draw[:, 1], c='black', s=2)
plt.show()
