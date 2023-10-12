import os

MELT_BINARY = ""

PATHS = [
    "melt",
    "/Applications/Shotcut.app/Contents/MacOS/melt",
    r"C:\Program Files\Shotcut\melt.exe"
    "/Applications/Shotcut.app/Contents/MacOS/qmelt",
    r"C:\Program Files\Shotcut\qmelt.exe",
]

for p in PATHS:
    if os.path.exists(p):
        MELT_BINARY = p
        break
