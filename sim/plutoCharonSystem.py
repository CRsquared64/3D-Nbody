import nbody

# 75 / AU
PLUTO = nbody.Nbody(0, 0, 20, 1.30900 * 10 ** 22, (150, 133, 112), "pluto")

CHARON = nbody.Nbody(-1 * nbody.Nbody.PLUTO_TO_CHARON, 0, 12, 1.586 * 10 ** 21, (161, 116, 215), "charon")
CHARON.yv = 0.21 * 1000  # kms * 1000... why? old me please leave hints as to why it needs to be 1000

bodies = [CHARON, PLUTO]
video_name = "PlutoSystem"
