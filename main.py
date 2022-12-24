from pygame import display
import random
import app

if __name__ == "__main__":
    random.seed()
    display.set_caption("simulation")
    a = app.App()
    a.on_execute()