import glob
import os
import shutil
import re
import json
import requests
import logging

logging.basicConfig(filename="archive_reorg.log",
                    level=logging.WARNING,
                    filemode="w")

MISCDIC = {"Core_Supplement_New_990_Financial": "SUPPLEMENTAL-CORE-FINANCIAL-V2", 
           "Core_Supplement_05-14-2009_Financial": "SUPPLEMENTAL-CORE-FINANCIAL-V1", 
           "Core_Supplement_02-10-2009_Financial": "SUPPLEMENTAL-CORE", 
           "Core_Supplement_02-10-2009_Purpose_Program": "SUPPLEMENTAL-CORE-PROGRAM", 
           "Core_Supplement_02-10-2009_Key_Contact": "SUPPLEMENTAL-CORE-OFFICERS", 
           "NTEE-NAICS_crosswalk": "NTEE-NAICS-CROSSWALK", 
           "Current_Master_Ntee_Lookup_(April_2009)": "ALLNTEE-501CX-NONPROFIT-PX", 
           "AllEins_Master_Lookup": "ALLEINS-501CX-NONPROFIT-PX"}

def file_reorg(series, archive_folder):
    
    # Pywebcopy Archive Folder
    pywebcopy_dir = f"{archive_folder}/{series.lower()}/pywebcopy_archive"
    html_dir = f"{archive_folder}/{series.lower()}/{series.lower()}_archive_html"
    pywebcopy_foldernames = os.listdir(pywebcopy_dir)
    
    # URL Dictionary
    with open(f"{archive_folder}/{series.lower()}/{series.lower()}_urls.json") as f:
        url_dic = json.load(f)

    # Set file names
    filename_dic = {}

    for folder in pywebcopy_foldernames:

        if (series == "core") & ("Beta" not in folder):
        
            YEAR = folder[5:9]
            ORG = "CHARITIES"
            SCOPE = "3"
            FORM = "PZ"

            if "others" in folder:
                ORG = "NONPROFIT"
                SCOPE = "E"
            
            if "PF" in folder:
                ORG = "PRIVFOUND"
                FORM = "PF"

            if "Full" in folder: FORM = "PC"

            filename = f"CORE-{YEAR}-501C{SCOPE}-{ORG}-{FORM}"
        
        elif (series == "bmf"):

            if "1989" in folder: # year 1989 doesn't have a month on data dic
                month = "06"
                year = "1989"
            else:
                month = folder[4:6]
                year = folder[7:]

            filename = f"BMF-{year}-{month}-501CX-NONPROFIT-PX"

        elif (series == "trend"):

            if "PC" in folder: filename = "TREND-1989-2013-501C3-CHARITIES-PZ"
            elif "PF" in folder: filename = "TREND-1989-2013-501C3-PRIVFOUND-PZ"
            elif "Other" in folder: filename = 'TREND-1989-2013-501C3-NONPROFIT-PZ'

        elif (series == "digitizeddata"):

            if "Balance" in folder: info = "BALANCE"
            elif "Functional" in folder: info = "FUNCEXP"
            elif "Income" in folder: info = "INCPROD"
            elif "Master" in folder: info = "MHEADER"
            elif "Officers" in folder: info = "OFFICER"
            elif "Org_Purpose" in folder: info = "PURPOSE"
            elif "Other_Info" in folder: info = "OTHERIN"
            elif "Programs" in folder: info = "PROGRAM"
            elif "Revenue" in folder: info = "REVEXPS"
            elif "Schedule_A_Employees" in folder: info = "SCHAEMPS"
            elif "Schedule_A" in folder: info = "SCHAPTS"
            elif "Taxable" in folder: info = "TAXABLE"

            filename = f"DIG-{info}-1998-2003-501C3-CHARITIES-PZ"

        elif (series == "misc"):

            filename = MISCDIC[folder]

        else: filename = folder

        filename_dic[folder] = filename

    for pywebcopyfolder, newname in filename_dic.items():

        newhtml = newname + ".html"

        # Copy over webpage itself

        html_files = glob.glob(f"{pywebcopy_dir}/{pywebcopyfolder}/**/*.php.html", 
                            recursive = True)
        
        if len(html_files) > 0:
            
            for f in html_files:
                
                if archive_folder == "dictionary": file = re.search(r'dd2.*', f)
                elif archive_folder == "data": file = re.search(r"showDD.*", f)
                shutil.copy(f, html_dir)

                try:

                    os.rename(f"{html_dir}/{file.group()}",
                              f"{html_dir}/{newhtml}")

                except:

                    logging.warning("Cannot find html:")
                    logging.warning(f"{f}")

        else:

            dd_url = url_dic[pywebcopyfolder]
            dd_page = requests.get(dd_url)

            with open(f"{html_dir}/{newhtml}", "wb+") as f:
                f.write(dd_page.content)

    return("HTML saved")

def postprocessing(series, archive_folder):
    """
    Copy folders needed for website replication in github repository
    """
    series_dir = f"{archive_folder}/{series.lower()}"
    pywebcopy_dir = series_dir + "/pywebcopy_archive/"
    html_dir = series_dir + f"/{series.lower()}_archive_html/"
    pywebcopy_foldernames = os.listdir(pywebcopy_dir)

    int_dir = "nccs-data.urban.org"       

    for py_f in pywebcopy_foldernames:

        ext_dirs = os.listdir(f"{pywebcopy_dir + py_f}")
        
        for dir in ext_dirs: 

            src = pywebcopy_dir + py_f + "/" + dir + "/"
            dest = series_dir + "/" + dir + "/"
            
            if dir != int_dir:

                try: shutil.copytree(src, dest, dirs_exist_ok = True)

                except:

                    try: shutil.copytree(src, dest, dirs_exist_ok = False)
                    except: raise Warning(f"{pywebcopy_dir + py_f + dir} not found")

            elif dir == int_dir:
                
                root_dir = pywebcopy_dir + py_f + "/" + int_dir
                int_dirs = os.listdir(root_dir)                    
           
                for dir in int_dirs:

                    src = pywebcopy_dir + py_f + "/nccs-data.urban.org/" + dir
                    dest = html_dir + dir

                    if "." not in dir:
                        
                        try: shutil.copytree(src, dest, dirs_exist_ok = True)
                        
                        except:

                            try:
                                shutil.copytree(src, dest, dirs_exist_ok = False)
                                
                            except:
                                warn_dir = pywebcopy_dir + py_f + "/nccs-data.urban.org/" + dir
                                raise Warning(f"{warn_dir} not found")

                    elif dir == "favicon.ico": shutil.copy(src, dest)

        break
        
    return("Postprocessing complete")