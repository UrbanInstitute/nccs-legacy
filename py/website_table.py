import os
import pandas as pd

DIRS = ["dictionary", "data", "homepages"]
SUBDIRS = ["home", "bmf", "core", "trend", "digitizeddata", "misc", "soi"]

GITHUB_BASE_URL = "https://urbaninstitute.github.io/nccs-legacy/"

if __name__ == "__main__":

    df_dic = {"Old Website Section": [],
              "Page Name": [],
              "NCCS Legacy Link": []}

    os.chdir("..")

    for dir in DIRS:

        if dir == "dictionary":

            for subdir in SUBDIRS:

                html_dir = dir + "/" + subdir + "/" + f"{subdir}_archive_html/"
                htmldir_ls = os.listdir(html_dir)

                for f in htmldir_ls:
                    if "html" in f:
                        github_url = GITHUB_BASE_URL + html_dir + f
                        page_name = f.replace(".html", "")
                        df_dic["NCCS Legacy Link"].append(github_url)
                        df_dic["Page Name"].append(page_name)
                        df_dic["Old Website Section"].append(dir.capitalize())

        
        else:
            subdir = "home"
            html_dir = dir + "/" + subdir + "/" + f"{subdir}_archive_html/"
            htmldir_ls = os.listdir(html_dir)

            for f in htmldir_ls:
                if "html" in f:
                    github_url = GITHUB_BASE_URL + html_dir + f
                    page_name = f.replace(".html", "")
                    df_dic["NCCS Legacy Link"].append(github_url)
                    df_dic["Page Name"].append(page_name)
                    df_dic["Old Website Section"].append(dir.capitalize())


    df = pd.DataFrame(df_dic)
    md_table = df.to_markdown()
    
    with open("Archive.md", "w+") as f:
        f.write(md_table)








