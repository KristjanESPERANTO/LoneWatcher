import logging
import threading
import tomllib
from logging.handlers import TimedRotatingFileHandler
from gui import StatusGUI

from check_process import is_script
from monitor import monitor_system

with open("config.toml", "rb") as file:
    config = tomllib.load(file)
    monitoring_targets = config["monitoring"]["entities"]

logging.addLevelName(logging.ERROR, '-E-')
logging.addLevelName(logging.INFO, '-I-')

# If run as script, log to console; otherwise log to file
if is_script():
    logging.basicConfig(format="%(levelname)s\t%(asctime)s\t%(message)s", level=logging.INFO, datefmt="%Y-%m-%d\t%H:%M:%S")
else:
    # Use TimedRotatingFileHandler for daily log rotation
    log_handler = TimedRotatingFileHandler("history.log", when="midnight", interval=1, backupCount=7)
    log_handler.setFormatter(logging.Formatter("%(levelname)s\t%(asctime)s\t%(message)s", datefmt="%Y-%m-%d\t%H:%M:%S"))

    logging.basicConfig(handlers=[log_handler], level=logging.INFO)

if __name__ == "__main__":
    gui = StatusGUI(monitoring_targets)

    # Start monitoring in separate thread
    monitoring_thread = threading.Thread(target=monitor_system, args=(monitoring_targets, gui, logging), daemon=True)
    monitoring_thread.start()

    gui.start_gui()
