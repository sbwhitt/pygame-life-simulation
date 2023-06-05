import os
import pickle
from static.settings import Settings as settings

def load_data(file_name: str) -> dict:
    try:
        path = os.path.join(os.path.dirname(__file__), "../../saves\\" + file_name)
        with open(path, "rb") as fin:
            obs = pickle.load(fin)
            fin.close()
            if obs:
                settings.ENT_WIDTH = obs["ENT_WIDTH"]
                settings.WORLD_SIZE = obs["WORLD_SIZE"]
                settings.DIRS = obs["DIRS"]
                return obs
    except FileNotFoundError:
        print("save file not found")
        return
