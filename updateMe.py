import os, sys, shutil
from git import Repo

def clone_repo(repo_url, destination_folder=None):
    try:
        if destination_folder is None:
            destination_folder = os.path.join(os.getcwd(), repo_url.rstrip('/').split('/')[-1].replace('.git', ''))
        print(f"Cloning {repo_url} into {destination_folder}...")
        Repo.clone_from(repo_url, destination_folder)
        print("Repository cloned successfully!")
    except Exception as e:
        print(f"Error cloning repository: {e}")


import requests

def check_update():
    version=""
    with open('src\\version', 'r') as file:
        data = file.read()
        version=data
    url = "https://raw.githubusercontent.com/mohaksharma1/Dashboard/refs/heads/main/src/version"
    response = requests.get(url)
    if response.status_code == 200:
        file_content = response.json()
        if int(file_content) > int(version):
            print("Update available")
            return 1
        elif int(file_content) == int(version):
            print("Version Up to Date")
            return 0
        else:
            print("Update error contact Dev team")
            return 2
    else:
        return 2



# Example usage
if __name__ == "__main__":
    if check_update()==1:
        print("updating...")
        github_url = "https://github.com/mohaksharma1/Dashboard.git"  # Replace with your desired repo
        clone_repo(github_url)
        os.system('copy "./src/orders.db" "C:\\Users\\mohak\\Documents"')
        shutil.rmtree("src")
        shutil.copytree(os.path.join(os.getcwd(),"Dashboard\\src"), os.path.join(os.getcwd(),"src"))
        os.system(f'copy  "C:\\Users\\mohak\\Documents\\orders.db" {os.path.join(os.getcwd(),"src")}')
        print("update complete")
        shutil.rmtree(github_url.rstrip('/').split('/')[-1].replace('.git', ''))
        sys.exit(1)
    else:
        print("Update not required")

