import os
import logging

from archive_setup import folder_setup
from archive_dd_scraper import archive_dd_scraper
from archive_dd_dl import pyweb_archive
from archive_dd_fileorg import file_reorg
from archive_dd_fileorg import postprocessing

logger = logging
logger.basicConfig(filename="pywebcopy.log",
                    level=logging.WARNING,
                    filemode="w")

DIRS = ["dictionary", "data"]
SUBDIRS = ["home", "bmf", "core", "trend", "digitizeddata", "misc", "soi"]


if __name__ == "__main__":
    os.chdir("..")

    folder_setup(dirs = DIRS, subdirs = SUBDIRS)
    
    archive_dd_scraper(series = "home", folder = "data")
    pyweb_archive(series = "home", folder = "data")
    file_reorg(series = "home", archive_folder = "data")
    postprocessing(series = "home", archive_folder = "data")

    for dir in SUBDIRS: 
        archive_dd_scraper(series = dir, folder = "dictionary")
        pyweb_archive(series = dir, folder = "dictionary")
        file_reorg(series = dir, archive_folder = "dictionary")
        postprocessing(series = dir, archive_folder = "dictionary")
    