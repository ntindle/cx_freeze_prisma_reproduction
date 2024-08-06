import asyncio
import os
import sys
from multiprocessing import freeze_support, set_start_method

from prisma import Prisma


async def main():
    set_start_method("spawn", force=True)

    prisma = Prisma(auto_register=True, datasource={'url': 'file:./database.db'})

    if not prisma.is_connected():
        await prisma.connect()
    await prisma.test.create({"name": "Test"})
    print(f"Number of items in db: {await prisma.test.count()}")
    if prisma.is_connected():
        await prisma.disconnect()

def install_runtime():
    import nodeenv
    import prisma.cli.prisma as cli

    cache_dir = cli.config.nodeenv_cache_dir.absolute()
    if not cache_dir.exists():
        print(f"Installing nodeenv to {cache_dir}")
        sys_argv = sys.argv.copy()
        sys.argv = ["nodeenv", str(cache_dir), *cli.config.nodeenv_extra_args]
        nodeenv.main()
        sys.argv = sys_argv

    # PRISMA_BINARY_CACHE_DIR
    binary_dir = cli.config.binary_cache_dir.absolute()
    if not binary_dir.exists():
        print(f"Installing prisma to {cache_dir}")
        cli.run(["generate"])

if __name__ == "__main__":
    freeze_support()
    # install node and prisma binaries on first run
    if getattr(sys, "frozen", False):
        install_runtime()
    # run the main function
    asyncio.run(main())
