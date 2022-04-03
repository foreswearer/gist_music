import os
import shutil


def reset_dir(dir_to_be_reset):
    # make the top level directory
    try:
        shutil.rmtree(dir_to_be_reset)
    except OSError:
        pass
    try:
        os.mkdir(dir_to_be_reset)
    except OSError:
        pass
