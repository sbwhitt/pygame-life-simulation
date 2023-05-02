from pygame import display
import random
import app
import asyncio

async def main(a):
    await a.on_execute()

if __name__ == "__main__":
    random.seed()
    display.set_caption("pygame life simulation")
    a = app.App()
    asyncio.run(main(a))
