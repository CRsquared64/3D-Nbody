# takes file of stored poses and then gets them ready for main.py
import pickle


def fileLoad(file):
    try:
        with open(file, 'rb') as handle:
            poses = pickle.load(handle)
        return poses
    except Exception as e:
        print(f"Error Loading File {file}")
        print(e)

