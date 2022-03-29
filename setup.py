
import cx_Freeze

executables = [cx_Freeze.Executable('main.py',base ='Win32GUI',targetName = 'monitoria.exe', icon= 'imagem/map_icon.ico')]

cx_Freeze.setup(
    name="Monitoria",
    options={'build_exe': {'packages': [ 'PyQt5', 'psycopg2' ],
                           'include_files': ['imagem', 'vw']}},

    executables=executables

)
