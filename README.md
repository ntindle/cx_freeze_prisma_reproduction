# cx_freeze_prisma_reproduction

To Repro the issue run

```bash
poetry install
poetry shell
```

Then

```bash
prisma db push
python .\cx_freeze_prisma_reproduction\app.py
```

To see that it works. It should increment the count of items in the db every time its ran.

Then run

```bash
python setup.py bdist_msi
```

Open the folder `dist` and run the installer. Mine installs to `C:\Users\nicka\AppData\Local\Programs\prisma_repoduction\`

It should be in your Windows path as `prisma_repoduction.exe`. Opening a terminal should allow you to execute. Notice that the count will increment as expected.

```bash
prisma_repoduction.exe
```

Uninstall the software by searching Settings > Apps > Installed Apps > prisma_repoduction > Uninstall

Then, Open the pipelines for this software and download the MSI File that was built using the same setup.py file. Install the software and run the same test. The db will not connect and the count will not increment.

```bash
prisma_repoduction.exe
```
