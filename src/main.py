import sys
import asyncio
import random
from app import App
from pygame import display


async def main(a: App) -> None:
    await a.on_execute()

if __name__ == "__main__":
    random.seed()
    display.set_caption("pygame life simulation")
    a = None
    if len(sys.argv) == 2:
        a = App(save_file=sys.argv[1])
        asyncio.run(main(a))
    else:
        a = App()
        asyncio.run(main(a))
