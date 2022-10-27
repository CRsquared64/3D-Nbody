# basic solar system example
import nbody

global bodies


SUN = nbody.Nbody(0, 0, 15, 1.98892 * 10 ** 30, (255, 165, 0), "sun")
SUN2 = nbody.Nbody(2 * nbody.Nbody.AU, 2, 8, 1.98892 * 10 ** 30, (255, 165, 0), "sun2")
SUN2.yv = 200.236 * 1000
EARTH = nbody.Nbody(-1 * nbody.Nbody.AU, 2, 4, 5.9742 * 10 ** 24, (0, 0, 255), "earth")
EARTH.yv = 29.783 * 1000
MARS = nbody.Nbody(-1.524 * nbody.Nbody.AU, 0, 3, 6.39 * 10 ** 23, (255, 25, 0), "mars")
MARS.yv = 24.077 * 1000
VENUS = nbody.Nbody(0.723 * nbody.Nbody.AU, 0, 3, 4.865 * 10 ** 24, (255, 255, 255), "venus")
VENUS.yv = -35.02 * 1000

MOON = nbody.Nbody(-1.02 * nbody.Nbody.AU, 2, 2, 1.73477e22, (150, 150, 150), "moon")
MOON.yv = 2.9783e4

asteroid = nbody.Nbody(5 * nbody.Nbody.AU, 2, 1, 5 * 10 ** 17, (100, 100, 100), "asteroid")
asteroid.yv = 10.40 * 1000

MERCURY = nbody.Nbody(0.387 * nbody.Nbody.AU, 0, 2, 3.30 * 10 ** 23, (150, 150, 150), "mercurry")
MERCURY.yv = -47.4 * 1000

JUPITER = nbody.Nbody(-5.203 * nbody.Nbody.AU, 0, 8, 1.9 * 10 ** 27, (125, 84, 84), "jupiter")
JUPITER.yv = 13.07 * 1000

SATURN = nbody.Nbody(-9.5 * nbody.Nbody.AU, 0, 6, 5.683 * 10 ** 26, (255, 253, 208), "saturn")
SATURN.yv = 9.69 * 1000

STARMAN = nbody.Nbody(1.264 * nbody.Nbody.AU, 5, 1, 1315.418, (0, 255, 25), "starman")
STARMAN.yv = -27.67 * 1000
STARMAN.xv = 6.82 * 1000

bodies = [SUN, MARS, VENUS, MERCURY, EARTH, asteroid, JUPITER, SATURN, STARMAN]
video_name = "SolarSystem"