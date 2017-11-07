import os

MELT_BINARY = ''

MAC = '/Applications/Shotcut.app/Contents/MacOS/qmelt'
WIN = 'C:\Program Files\Shotcut\qmelt.exe'

if os.path.exists(MAC):
    MELT_BINARY = MAC
elif os.path.exists(WIN):
    MELT_BINARY = WIN
else:
    MELT_BINARY = 'melt'
