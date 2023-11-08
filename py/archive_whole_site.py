from pywebcopy import save_website
import os

if __name__ == "__main__":

    os.chdir("..")

    save_website(
    url="https://nccs.urban.org/",
    project_folder="nccs_drupal/",
    project_name="NCCS Drupal",
    bypass_robots=True,
    debug=True,
    open_in_browser=True,
    delay=None,
    threaded=False,
    )