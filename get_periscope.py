from subprocess import PIPE, Popen
import os
import time


def download_periscope(url):
    # -r does rotate but not in the correct direction
    # command = "pyriscope " + url + " -C"
    # Popen(command, shell=True, stdout=PIPE).stdout.read()

    # on video complete send notification
    # return download location path
    time.sleep(30)
    return os.path.dirname(os.path.realpath(__file__))
