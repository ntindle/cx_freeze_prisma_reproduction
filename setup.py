import glob
from pkgutil import iter_modules

import os
import sys

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


def find_latest_node_folder(base_path):
    pattern = os.path.join(base_path, "node-v*")
    matching_folders = glob.glob(pattern)
    if matching_folders:
        return max(matching_folders, key=os.path.getctime)
    return None


# Determine the base path
if sys.platform.startswith("win"):
    base_path = os.path.expanduser("~/.cache/prisma-python/nodeenv/src")
else:
    # For non-Windows platforms, adjust the path accordingly
    base_path = os.path.expanduser("~/.cache/prisma-python/nodeenv/src")

# Find the latest node folder
node_folder = find_latest_node_folder(base_path)

if node_folder and os.path.exists(node_folder):
    include_files.append((node_folder, "prisma-nodeenv"))
else:
    raise Exception("Node folder not found")


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
