#!/usr/bin/python
# coding=utf8
"""
# Author: meetbill
# Created Time : 2016-08-01 10:59:26

# File Name: blog.py
# Description:

"""
import sys
import logging
from logging.handlers import RotatingFileHandler
import os


class ColoredFormatter(logging.Formatter):
    '''A colorful formatter.'''

    def __init__(self, fmt=None, datefmt=None):
        logging.Formatter.__init__(self, fmt, datefmt)
        # Color escape string
        COLOR_RED = '\033[1;31m'
        COLOR_GREEN = '\033[1;32m'
        COLOR_YELLOW = '\033[1;33m'
        COLOR_BLUE = '\033[1;34m'
        COLOR_PURPLE = '\033[1;35m'
        COLOR_CYAN = '\033[1;36m'
        COLOR_GRAY = '\033[1;37m'
        COLOR_WHITE = '\033[1;38m'
        COLOR_RESET = '\033[1;0m'

        # Define log color
        self.LOG_COLORS = {
            'DEBUG': '%s',
            'INFO': COLOR_GREEN + '%s' + COLOR_RESET,
            'WARNING': COLOR_YELLOW + '%s' + COLOR_RESET,
            'ERROR': COLOR_RED + '%s' + COLOR_RESET,
            'CRITICAL': COLOR_RED + '%s' + COLOR_RESET,
            'EXCEPTION': COLOR_RED + '%s' + COLOR_RESET,
        }

    def format(self, record):
        level_name = record.levelname
        msg = logging.Formatter.format(self, record)

        return self.LOG_COLORS.get(level_name, '%s') % msg


class Log(object):

    '''
    log
    '''

    def __init__(self, filename, level="debug", logid="meetbill",
                 mbs=20, count=10, is_console=True):
        '''
        mbs: how many MB
        count: the count of remain
        '''
        try:
            self._level = level
            #print "init,level:",level,"\t","get_map_level:",self._level
            self._filename = filename
            self._logid = logid
            self._logger = logging.getLogger(self._logid)
            file_path = os.path.split(self._filename)[0]
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            if not len(self._logger.handlers):
                self._logger.setLevel(self.get_map_level(self._level))

                fmt = '[%(asctime)s] %(levelname)s %(message)s'
                datefmt = '%Y-%m-%d %H:%M:%S'
                formatter = logging.Formatter(fmt, datefmt)

                maxBytes = int(mbs) * 1024 * 1024
                file_handler = RotatingFileHandler(
                    self._filename, mode='a', maxBytes=maxBytes, backupCount=count)
                self._logger.setLevel(self.get_map_level(self._level))
                file_handler.setFormatter(formatter)
                self._logger.addHandler(file_handler)

                if is_console == True:
                    stream_handler = logging.StreamHandler(sys.stderr)
                    console_formatter = ColoredFormatter(fmt, datefmt)
                    stream_handler.setFormatter(console_formatter)
                    self._logger.addHandler(stream_handler)
            self._logger.propagate = False

        except Exception as expt:
            print expt

    def tolog(self, msg, level=None):
        try:
            level = level if level else self._level
            level = str(level).lower()
            level = self.get_map_level(level)
            if level == logging.DEBUG:
                self._logger.debug(msg)
            if level == logging.INFO:
                self._logger.info(msg)
            if level == logging.WARN:
                self._logger.warn(msg)
            if level == logging.ERROR:
                self._logger.error(msg)
            if level == logging.CRITICAL:
                self._logger.critical(msg)
        except Exception as expt:
            print expt

    def debug(self, msg):
        self.tolog(msg, level="debug")

    def info(self, msg):
        self.tolog(msg, level="info")

    def warn(self, msg):
        self.tolog(msg, level="warn")

    def error(self, msg):
        self.tolog(msg, level="error")

    def critical(self, msg):
        self.tolog(msg, level="critical")

    def get_map_level(self, level="debug"):
        level = str(level).lower()
        #print "get_map_level:",level
        if level == "debug":
            return logging.DEBUG
        if level == "info":
            return logging.INFO
        if level == "warn":
            return logging.WARN
        if level == "error":
            return logging.ERROR
        if level == "critical":
            return logging.CRITICAL


def init_log(log_path, level=logging.INFO, when="D", backup=7,
             format="%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s",
             datefmt="%m-%d %H:%M:%S"):
    """
    init_log - initialize log module

    Args:
      log_path      - Log file path prefix.
                      Log data will go to two files: log_path.log and log_path.log.wf
                      Any non-exist parent directories will be created automatically
      level         - msg above the level will be displayed
                      DEBUG < INFO < WARNING < ERROR < CRITICAL
                      the default value is logging.INFO
      when          - how to split the log file by time interval
                      'S' : Seconds
                      'M' : Minutes
                      'H' : Hours
                      'D' : Days
                      'W' : Week day
                      default value: 'D'
      format        - format of the log
                      default format:
                      %(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s
                      INFO: 12-09 18:02:42: log.py:40 * 139814749787872 HELLO WORLD
      backup        - how many backup file to keep
                      default value: 7

    Raises:
        OSError: fail to create log directories
        IOError: fail to open log file
    """
    formatter = logging.Formatter(format, datefmt)
    logger = logging.getLogger()
    logger.setLevel(level)

    dir = os.path.dirname(log_path)
    if not os.path.isdir(dir):
        os.makedirs(dir)

    handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log",
                                                        when=when,
                                                        backupCount=backup)
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log.wf",
                                                        when=when,
                                                        backupCount=backup)
    handler.setLevel(logging.WARNING)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


if __name__ == "__main__":
    # 通用模块日志
    init_log("./log/common.log")
    logging.info("info log")
    logging.warning("warning log")
    logging.error("error log")
    logging.debug("debug log")
    # 独立模块日志
    debug = True
    logpath = "./log/test.log"
    logger = Log(
        logpath,
        level="debug",
        logid="meetbill",
        is_console=debug,
        mbs=5,
        count=5)

    logstr = "helloworld"
    logger.error(logstr)
    logger.info(logstr)
    logger.warn(logstr)
    logger.debug(logstr)
