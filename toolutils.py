import os
import tempfile
from contextlib import contextmanager
import subprocess


def safe_subprocess(command_array):
    ''' return True/False, command output '''

    try:
        return True, subprocess.Popen(command_array,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT).communicate()[0]
    except OSError as e:
        return False, e.__str__()
    except subprocess.CalledProcessError as e:
        return False, e.output


@contextmanager
def atomic_write(filepath):
    """
        Writeable file object that atomically
        updates a file (using a temporary file).

        :param filepath: the file path to be opened
    """

    # Put tmp file to same directory as target file, to allow atomic move
    realpath = os.path.realpath(filepath)
    tmppath = os.path.dirname(realpath)
    with tempfile.NamedTemporaryFile(dir=tmppath, delete=False) as tf:
        with open(tf.name, mode='w+') as tmp:
            yield tmp
            tmp.flush()
            os.fsync(tmp.fileno())
        os.rename(tf.name, realpath)
