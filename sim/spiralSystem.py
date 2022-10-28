import random
from math import *
from pylab import *
import numpy as np


def coord(n):  # math credit to https://stackoverflow.com/questions/38562144/simulating-a-logarithmic-spiral-galaxy-in-python
    theta = np.radians(np.linspace(0, 360 * 5, 1000))
    n = 1000
    a = 1
    b = 0.4
    th = np.random.randn(n)
    x = a * exp(b * th) * cos(th)
    y = a * exp(b * th) * sin(th)
    x1 = a * exp(b * (th)) * cos(th + pi)
    x1 = a * exp(b * (th)) * cos(th + pi)
    y1 = a * exp(b * (th)) * sin(th + pi)

    sx = np.random.normal(0, a * 0.25, n)
    sy = np.random.normal(0, a * 0.25, n)
    plot(x + sy, y + sx, "*")
    plot(x1 + sx, y1 + sy, "*")
    show()

    x = x + sy
    y = y + sx

    x1 = x1 + sx
    y1 = y1 + sy

    return x, y, x1, y1





