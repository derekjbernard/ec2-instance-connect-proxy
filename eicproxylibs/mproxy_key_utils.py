from os import chmod, listdir, makedirs
from os.path import expanduser
from os.path import isfile
from os.path import join as pathjoin

from eicproxylibs import key_utils

def generate_key_at(key_path=None):
    if key_path is not None:
        key = key_utils.generate_key(2048)
        with open(key_path, 'w') as f:
            f.write(key)
            os.chmod(key_path, 0o600)
