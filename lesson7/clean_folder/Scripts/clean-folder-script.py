#!d:\pyton\hw7\clean_folder\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'clean-folder==0.0.1','console_scripts','clean-folder'
__requires__ = 'clean-folder==0.0.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('clean-folder==0.0.1', 'console_scripts', 'clean-folder')()
    )
