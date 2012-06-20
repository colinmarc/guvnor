from zodiac import build_patch
from guvnor.guvnor import *

socket = build_patch('guvnor.socket', 'socket')
ssl = build_patch('guvnor.ssl', 'ssl')


