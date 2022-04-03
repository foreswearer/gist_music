import os
import shutil
from datetime import datetime

__level = 4


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


def log(message, level):
    if level <= __level:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f'{current_time} :Making Viz {message}')  # TODO refactor logging
