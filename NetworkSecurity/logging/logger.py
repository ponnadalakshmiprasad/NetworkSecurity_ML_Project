import logging
import os
from datetime import datetime

log_file_name = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" #log file in the format of "12_30_2025_15_35_12.log".
log_path=os.path.join(os.getcwd(),"logs") #creates log path in the current directory with the logs like user/prasad/networksecurity/logs.
os.makedirs(log_path, exist_ok=True) #makes the log path (user/prasad/networksecurity/logs) directory if it does not exist in current working directory.

log_file_path=os.path.join(log_path,log_file_name) #creates log file path in the log path (user/prasad/networksecurity/logs) directory with the log file name (month_day_year_hour_minute_second.log) that is /Users/prasad/networksecurity/logs/12_30_2025_15_35_12.log.
 

logging.basicConfig(
    filename=log_file_path,
    format="[%(asctime)s] %(lineno)d  %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,  #The logging level acts as a severity filter for log messages.Setting level=logging.INFO means that INFO and higher-severity messages(INFO, WARNING, ERROR, and CRITICAL) will be logged.
    ) #basic configuration for logging (this is what with the file name and , format,level  (logging info) stores in the logs directory in the log_file_path(/Users/prasad/networksecurity/logs/12_30_2025_15_35_12.log) as logging configuration like "[2025-12-30 14:45:12,345] 55 root - INFO - Logging system initialized")


"""
Logger.py file creation and usage:

You are not creating logging yourself
You are using Python's built-in logging library
In logger.py, you:
Configure logging once
Create a directory (logs/)
Create a log file
Tell the logging library where and how to store logs


How it Operates:

If you import logging directly everywhere, logging behavior can become inconsistent
Different files may:
configure logging differently
log to different places
or log to console instead of files
To avoid this, you:
configure logging once in logger.py
import that configuration everywhere

"""