import pickle

with open('nb_run.dat', 'rb') as handle:
    data = pickle.load(handle)

print(data)