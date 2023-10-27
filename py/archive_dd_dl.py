from pywebcopy import save_webpage
import json
import logging

logger = logging.getLogger(__name__)


def pyweb_archive(series, folder):
    """
    Take a dictionary of data dictionary names: urls and archive
    each url. Storing archive in a folder named after the data dictionary
    """
    # Load in dictionary
    pywebcopy_dir = f"{folder}/{series.lower()}/pywebcopy_archive"


    with open(f"{folder}/{series.lower()}/{series.lower()}_urls.json") as f:
        url_dic = json.load(f)
    
    for dd, url in url_dic.items():
        try:
            save_webpage(
                url = url,
                project_folder = pywebcopy_dir,
                project_name = dd,
                bypass_robots = True,
                debug = True,
                open_in_browser = False,
                delay = 5,
                threaded = False,
            )
        
        except:
            logging.warning("Failed to save url:")
            logging.warning(url)
    
    return("Archival Complete")