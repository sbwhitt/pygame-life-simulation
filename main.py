import asyncio
import random
from app import App
from pygame import display


async def main(a: App) -> None:
    await a.on_execute()

if __name__ == "__main__":
    random.seed()
    display.set_caption("pygame life simulation")
    a = App()
    asyncio.run(main(a))
