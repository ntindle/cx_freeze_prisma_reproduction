# cx_freeze_prisma_reproduction

To Repro the issue run

```pwsh
poetry install
poetry shell
```

Then

```pwsh
prisma db push
python .\cx_freeze_prisma_reproduction\app.py
```

To see that it works. It should increment the count of items in the db every time its ran.

Then run

```pwsh
python setup.py bdist_msi
```

Open the folder `dist` and run the installer. Mine installs to `C:\Users\nicka\AppData\Local\Programs\prisma_repoduction\`

You may need to allow it to run as it is not signed. You can do this by clicking `More Info` and then `Run Anyway`.

It should be in your Windows path as `prisma_repoduction.exe`. Opening a terminal should allow you to execute. Notice that the count will increment as expected.

```pwsh
prisma_repoduction.exe
```

Uninstall the software by searching Settings > Apps > Installed Apps > prisma_repoduction > Uninstall

The pipeline `ci.yml` builds two artifacts. One sets the Environment Variables and the other does not.

Then, Open the [latest pipeline for this repo](https://github.com/ntindle/cx_freeze_prisma_reproduction/actions/) and download the MSI File that was built using the same setup.py file.

Then, select the `prisma_reproduction-no-env-set-msi-windows` artifact and run the below commands. Update the below to your install location that was installed by the MSI file.

```pwsh
prisma_repoduction.exe
```

The db will not connect and the count will not increment.

Error Message:

```pwsh
PS C:\Users\nicka> prisma_repoduction.exe
Traceback (most recent call last):
  File "C:\Users\runneradmin\AppData\Local\pypoetry\Cache\virtualenvs\cx-freeze-prisma-reproduction-NZnYsTqa-py3.10\Lib\site-packages\cx_Freeze\initscripts\__startup__.py", line 141, in run
  File "C:\Users\runneradmin\AppData\Local\pypoetry\Cache\virtualenvs\cx-freeze-prisma-reproduction-NZnYsTqa-py3.10\Lib\site-packages\cx_Freeze\initscripts\console.py", line 25, in run
  File "cx_freeze_prisma_reproduction\app.py", line 22, in <module>
  File "C:\hostedtoolcache\windows\Python\3.10.11\x64\lib\asyncio\runners.py", line 44, in run
  File "C:\hostedtoolcache\windows\Python\3.10.11\x64\lib\asyncio\base_events.py", line 649, in run_until_complete
  File "cx_freeze_prisma_reproduction\app.py", line 14, in main
  File "C:\Users\runneradmin\AppData\Local\pypoetry\Cache\virtualenvs\cx-freeze-prisma-reproduction-NZnYsTqa-py3.10\lib\site-packages\prisma\_base_client.py", line 430, in connect
  File "C:\Users\runneradmin\AppData\Local\pypoetry\Cache\virtualenvs\cx-freeze-prisma-reproduction-NZnYsTqa-py3.10\lib\site-packages\prisma\engine\_query.py", line 349, in connect
  File "C:\Users\runneradmin\AppData\Local\pypoetry\Cache\virtualenvs\cx-freeze-prisma-reproduction-NZnYsTqa-py3.10\lib\site-packages\prisma\engine\_query.py", line 58, in _ensure_file
  File "C:\Users\runneradmin\AppData\Local\pypoetry\Cache\virtualenvs\cx-freeze-prisma-reproduction-NZnYsTqa-py3.10\lib\site-packages\prisma\engine\utils.py", line 111, in ensure
prisma.engine.errors.BinaryNotFoundError: Expected C:\Users\nicka\prisma-query-engine-windows.exe, C:\Users\nicka\.cache\prisma-python\binaries\5.11.0\efd2449663b3d73d637ea1fd226bafbcf45b3102\prisma-query-engine-windows.exe or C:\Users\runneradmin\.cache\prisma-python\binaries\5.11.0\efd2449663b3d73d637ea1fd226bafbcf45b3102\node_modules\prisma\query-engine-windows.exe to exist but none were found or could not be executed.
Try running prisma py fetch
```

Uninstall the software by searching Settings > Apps > Installed Apps > prisma_repoduction > Uninstall

Then select the `prisma_reproduction-msi-windows` artifact and run the below commands. Update the below to your install location that was installed by the MSI file.

```pwsh
$env:PRISMA_HOME_DIR = "C:\Users\nicka\AppData\Local\Programs\prisma_repoduction\prisma"
$env:PRISMA_BINARY_CACHE_DIR = "C:\Users\nicka\AppData\Local\Programs\prisma_repoduction\prisma\node_modules\prisma"
prisma_repoduction.exe
```

Error Message:

```pwsh
PS C:\Users\nicka> prisma_repoduction.exe
Traceback (most recent call last):
  File "C:\Users\runneradmin\AppData\Local\pypoetry\Cache\virtualenvs\cx-freeze-prisma-reproduction-NZnYsTqa-py3.10\Lib\site-packages\cx_Freeze\initscripts\__startup__.py", line 141, in run
  File "C:\Users\runneradmin\AppData\Local\pypoetry\Cache\virtualenvs\cx-freeze-prisma-reproduction-NZnYsTqa-py3.10\Lib\site-packages\cx_Freeze\initscripts\console.py", line 25, in run
  File "cx_freeze_prisma_reproduction\app.py", line 22, in <module>
  File "C:\hostedtoolcache\windows\Python\3.10.11\x64\lib\asyncio\runners.py", line 44, in run
  File "C:\hostedtoolcache\windows\Python\3.10.11\x64\lib\asyncio\base_events.py", line 649, in run_until_complete
  File "cx_freeze_prisma_reproduction\app.py", line 14, in main
  File "C:\Users\runneradmin\AppData\Local\pypoetry\Cache\virtualenvs\cx-freeze-prisma-reproduction-NZnYsTqa-py3.10\lib\site-packages\prisma\_base_client.py", line 430, in connect
  File "C:\Users\runneradmin\AppData\Local\pypoetry\Cache\virtualenvs\cx-freeze-prisma-reproduction-NZnYsTqa-py3.10\lib\site-packages\prisma\engine\_query.py", line 349, in connect
  File "C:\Users\runneradmin\AppData\Local\pypoetry\Cache\virtualenvs\cx-freeze-prisma-reproduction-NZnYsTqa-py3.10\lib\site-packages\prisma\engine\_query.py", line 58, in _ensure_file
  File "C:\Users\runneradmin\AppData\Local\pypoetry\Cache\virtualenvs\cx-freeze-prisma-reproduction-NZnYsTqa-py3.10\lib\site-packages\prisma\engine\utils.py", line 111, in ensure
prisma.engine.errors.BinaryNotFoundError: Expected C:\Users\nicka\prisma-query-engine-windows.exe, C:\Users\nicka\AppData\Local\Programs\prisma_repoduction\prisma\node_modules\prisma\prisma-query-engine-windows.exe or D:\a\cx_freeze_prisma_reproduction\cx_freeze_prisma_reproduction\prisma\node_modules\prisma\query-engine-windows.exe to exist but none were found or could not be executed.
Try running prisma py fetch
```

The db will not connect and the count will not increment.

Next, open the folder for your `PRISMA_BINARY_CACHE_DIR` (mine is `C:\Users\nicka\AppData\Local\Programs\prisma_repoduction\prisma\node_modules\prisma`) and rename the `query-engine-windows.exe` to `prisma-query-engine-windows.exe`.

Then run the below command. Update the below to your install location that was installed by the MSI file.

```pwsh
$env:PRISMA_HOME_DIR = "C:\Users\nicka\AppData\Local\Programs\prisma_repoduction\prisma"
$env:PRISMA_BINARY_CACHE_DIR = "C:\Users\nicka\AppData\Local\Programs\prisma_repoduction\prisma\node_modules\prisma"
prisma_repoduction.exe
```

This gives a different error message:

```pwsh
{"is_panic":false,"message":"Error querying the database: Error code 14: Unable to open the database file","backtrace":"   0: <unknown>\n   1: <unknown>\n   2: <unknown>\n   3: <unknown>\n   4: <unknown>\n   5: <unknown>\n   6: <unknown>\n   7: <unknown>\n   8: BaseThreadInitThunk\n   9: RtlUserThreadStart\n"}
```
