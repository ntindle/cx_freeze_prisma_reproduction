import asyncio
from multiprocessing import freeze_support, set_start_method

from prisma import Prisma


async def main():
    set_start_method("spawn", force=True)
    freeze_support()

    prisma = Prisma(auto_register=True)

    if not prisma.is_connected():
        await prisma.connect()
    await prisma.test.create({"name": "Test"})
    print(f"Number of items in db: {await prisma.test.count()}")
    if prisma.is_connected():
        await prisma.disconnect()

if __name__ == "__main__":
    # run the main function
    asyncio.run(main())
