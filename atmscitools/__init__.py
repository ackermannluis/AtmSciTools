from __future__ import absolute_import, division, print_function, unicode_literals
from pathlib import Path
import warnings
import sys

warnings.filterwarnings("ignore")

__version__ = '1.7.0'

# Get path to mymodule
AtmSciTools_path = str(Path(__file__).parent)
sys.path.append(AtmSciTools_path)

# # import subpackages
# try:
#     import cdsapi
# except:
#     print('no cdsapi')
#
# try:
#     import IMProToo_mod
# except:
#     print('no IMProToo_mod')
#
# try:
#     import SkewT_V2 as SkewT
# except:
#     print('no SkewT_V2')

from .main import *
