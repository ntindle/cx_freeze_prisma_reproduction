
from pkgutil import iter_modules

import os

from cx_Freeze import Executable, setup  # type: ignore

import prisma

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

# add the prisma directory if it exists
if os.path.exists("./prisma"):
    include_files.append(("./prisma", "prisma"))

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
