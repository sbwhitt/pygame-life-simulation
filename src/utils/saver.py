import os
import pickle

def save_data(to_save: dict):
    with open(os.path.join(os.path.dirname(__file__), "..\\..\\saves\\save.ent"), "wb") as fout:
        pickle.dump(to_save, fout)
        fout.close()
