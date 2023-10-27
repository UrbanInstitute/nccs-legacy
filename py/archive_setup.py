import os

def folder_setup(dirs, subdirs):
    """
    Function to set up folder structure for archival tasks
    """
    for dir in dirs:
        
        if not os.path.exists(f"{dir}"): os.mkdir(f"{dir}")

        for subdir in subdirs:

            if (dir == "dictionary") or ((dir != "dictionary") & (subdir == "home")):

                folders = [f"{dir}/{subdir}",
                           f"{dir}/{subdir}/pywebcopy_archive",
                           f"{dir}/{subdir}/{subdir}_archive_html"]
                
                for folder in folders:
                    if not os.path.exists(folder): os.mkdir(folder)

    return("Folders setup")