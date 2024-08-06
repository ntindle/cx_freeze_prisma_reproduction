import asyncio
import os
import sys
from multiprocessing import freeze_support, set_start_method

from prisma import Prisma


async def main():
    set_start_method("spawn", force=True)
    freeze_support()

    if getattr(sys, "frozen", False):
        os.environ["PRISMA_BINARY_CACHE_DIR"] = os.path.dirname(sys.executable)

    if getattr(sys, "frozen", True):
        # If the application is run as a bundle, the set the postgres up if DATABASE_URL is not set
        # if "DATABASE_URL" not in os.environ:
        # port = # random high unused port
        # os.environ["DATABASE_URL"] = "postgresql://autogpt_server:autogpt_server_password@localhost:5432/autogpt_server"
        # if first time running, create the database
        if not os.path.exists("postgres_data"):

            def init_postgres(password: str):
                print("Initializing PostgreSQL")
                # arguments
                # -D, --pgdata DATADIR
                #     location for this database cluster
                # -U, --username=NAME
                #     cluster superuser name
                # --pwfile=FILE
                #     read password for the superuser from file
                # --no-instructions
                #    do not display instructions for creating a database cluster

                # write the password to a file
                with open("pg_pass.txt", mode="w+") as f:
                    f.write(password)
                    print("Password file created")

                if sys.platform == "win32":
                    os.system(
                        ".\\pgsql\\bin\\initdb.exe --pgdata=postgres_data --username=autogpt_server --pwfile=pg_pass.txt --no-instructions"
                    )

                os.remove("pg_pass.txt")
                print("PostgreSQL Database initialization complete")
                # Register the database
                # os.system('.\\pgsql\\bin\\pgctl.exe register -D postgres_data -N "AutoGPT Server PostgreSQL" -w -S demand')
                # Start the database
                os.system(
                    ".\\pgsql\\bin\\pg_ctl.exe start -D postgres_data -l postgres_data\\logfile.txt"
                )
                # Create a new database
                os.system(
                    ".\\pgsql\\bin\\pg_ctl.exe start -D postgres_data -l postgres_data\\logfile.txt"
                )

            init_postgres("autogpt_server_password")

        else:
            print("PostgreSQL data directory already exists")

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

        install_runtime()
    prisma = Prisma(
        auto_register=True,
    )

    if not prisma.is_connected():
        await prisma.connect()
    await prisma.test.create({"name": "Test"})
    print(f"Number of items in db: {await prisma.test.count()}")
    if prisma.is_connected():
        await prisma.disconnect()


if __name__ == "__main__":
    # run the main function
    asyncio.run(main())
