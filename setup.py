import glob
from pkgutil import iter_modules
import urllib

import os
import sys
import zipfile

from cx_Freeze import Executable, setup  # type: ignore

import prisma
import prisma.generator
import prisma.generator.schema

GUID = "{323a1ee5-317d-4423-8490-effd8f5bedcf}"

packages = [
    m.name
    for m in iter_modules()
    if m.ispkg and m.module_finder and "poetry" in m.module_finder.path  # type: ignore
]


# source, destination in the bundle
include_files = [
    (prisma.BINARY_PATHS.query_engine["windows"], "prisma-query-engine-windows.exe")
]


# Add postgres binary
# windows: https://sbp.enterprisedb.com/getfile.jsp?fileid=1259104
# mac: https://sbp.enterprisedb.com/getfile.jsp?fileid=1259020


# Download and extract PostgreSQL binary
def download_and_extract_postgres(url, filename="pgsql.zip"):
    print(f"Downloading PostgreSQL from {url}")
    with urllib.request.urlopen(url) as response, open(filename, "wb") as out_file:
        out_file.write(response.read())

    print("Extracting PostgreSQL")
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall("pgsql")

    os.remove(filename)
    print("PostgreSQL extraction complete")



if sys.platform == "win32":
    postgres_url = "https://sbp.enterprisedb.com/getfile.jsp?fileid=1259104"
    download_and_extract_postgres(postgres_url)
    include_files.append(("pgsql", "pgsql"))
elif sys.platform == "darwin":
    postgres_url = "https://sbp.enterprisedb.com/getfile.jsp?fileid=1259020"
    download_and_extract_postgres(postgres_url)
    include_files.append(("pgsql", "pgsql"))


# add the prisma directory if it exists
if os.path.exists("./prisma"):
    include_files.append(("./prisma", "prisma"))

if os.path.exists("./database.db"):
    include_files.append(("./database.db", "database.db"))


# copy the prisma schema into the folder /prisma/schema.prisma
if os.path.exists("./schema.prisma"):
    include_files.append(("./schema.prisma", "prisma/schema.prisma"))

if os.path.exists("./postgres.schema.prisma"):
    include_files.append(("./postgres.schema.prisma", "prisma/postgres.schema.prisma"))

setup(
    name="AutoGPT Server",
    url="https://agpt.co",
    # The entry points of the application
    executables=[
        Executable(
            "cx_freeze_prisma_reproduction/app.py",
            target_name="prisma_repoduction",
            base="console",
        ),
    ],
    options={
        # Options for building all the executables
        "build_exe": {
            "packages": packages,
            "includes": [
                "cx_freeze_prisma_reproduction",
                "prisma",
            ],
            # Exclude the two module from readability.compat as it causes issues
            "excludes": ["readability.compat.two"],
            "include_files": include_files,
        },
        # Windows .msi specific options
        "bdist_msi": {
            "target_name": "prisma_repoduction",
            "add_to_path": True,
            "upgrade_code": GUID,
        },
    },
)
