import os
import pickle
import src.utils.utils as utils

def save_data(to_save: dict):
    name = "save_" + utils.get_current_date_str() + ".ent"
    with open(os.path.join(os.path.dirname(__file__), "..\\..\\saves\\" + name), "wb") as fout:
        pickle.dump(to_save, fout)
        fout.close()
