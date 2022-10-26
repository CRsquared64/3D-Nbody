import nbody

global bodies, scale


distance_to_moon = 3.84399 * 10 ** 8
SCALE = 100 / distance_to_moon  # 75 / AU
EARTH = nbody.Nbody(0,0, 20, 5.9742 * 10 ** 24, (0, 0, 255), "earth")

MOON = nbody.Nbody(-1 * distance_to_moon, 0, 12,  7.34767309 * 10 ** 22, (150, 150, 150), "moon")
MOON.yv = 1.022 * 1000 #kms * 1000... why? old me please leave hints as to why it needs to be 1000

bodies = [EARTH, MOON]
video_name = "MoonSystem"