import os
import pickle
from static.settings import Settings as settings

def load_data() -> dict:
    path = os.path.join(os.path.dirname(__file__), "../../saves\\save.ent")
    if not os.path.exists(path):
        print("save file not found")
        return
    with open(path, "rb") as fin:
        obs = pickle.load(fin)
        fin.close()
        return obs

def load_settings() -> None:
    path = os.path.join(os.path.dirname(__file__), "../../saves\\save.ent")
    if not os.path.exists(path):
        print("save file not found")
        return
    with open(path, "rb") as fin:
        obs = pickle.load(fin)
        fin.close()
        if obs["settings"]:
            settings.ENT_WIDTH = obs["settings"]["ENT_WIDTH"]
            settings.WORLD_SIZE = obs["settings"]["WORLD_SIZE"]
            settings.DIRS = obs["settings"]["DIRS"]
