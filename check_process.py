import os
import logging
import psutil


def check():
    """Determine if an instance of the program is already running. If so, the old instance will be terminated."""

    # only execute if not running as script
    if is_script() is False:

        logging.addLevelName(logging.ERROR, "-E-")
        logging.addLevelName(logging.INFO, "-I-")
        logging.basicConfig(
            format="%(levelname)s\t%(asctime)s\t%(message)s",
            level=logging.INFO,
            datefmt="%Y-%m-%d\t%H:%M:%S",
            filename="lonewatch.log",
        )

        # Get information of the own process
        own_pid = os.getpid()  # process ID
        own_name = psutil.Process(own_pid).name()  # name
        own_started = psutil.Process(own_pid).create_time()  # start time

        # Iterate process list
        for process in psutil.process_iter():

            # get the name of the current process
            other_name = process.name()

            # check if the current process has the the same name as the own process
            if other_name == own_name:
                # get the start time of the current process
                other_started = process.create_time()

                # determine the difference between the start times
                dif2now = own_started - other_started

                # terminate the process if it's x seconds older than than the own process (necessary because there are always two processes and the second opens later then the first)
                if dif2now > 5.0:
                    logging.error(
                        "Older instance of %s will be terminated.", process.name()
                    )
                    process.terminate()


def is_script():
    """Determine if running as script or exe.
    This is used at two places:
     1. Logging: If running as script > show logs in console, if as exe > write logs to file.
     2. Checking if program is already running.
    """
    own_pid = os.getpid()
    own_name = psutil.Process(own_pid).name()
    if own_name in ["python", "python.exe", "python3"]:
        return True
    return False
