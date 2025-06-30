import os, sys, shutil
from git import Repo

def clone_repo(repo_url, destination_folder=None):
    try:
        if destination_folder is None:
<<<<<<< Updated upstream
<<<<<<< Updated upstream
            destination_folder = os.path.join(os.getcwd(), repo_url.rstrip('/').split('/')[-1].replace('.git', ''))

=======
            destination_folder = os.path.join(os.getcwd(),"")
>>>>>>> Stashed changes
=======
            destination_folder = os.path.join(os.getcwd(),"")
>>>>>>> Stashed changes
        print(f"Cloning {repo_url} into {destination_folder}...")
        Repo.clone_from(repo_url, destination_folder)
        print("Repository cloned successfully!")
    except Exception as e:
        print(f"Error cloning repository: {e}")






# Example usage
if __name__ == "__main__":
    print("updating...")
    github_url = "https://github.com/mohaksharma1/Dashboard.git"  # Replace with your desired repo
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    clone_repo(github_url)
=======
    os.system('copy "./src/orders.db" "C:\\Users\\mohak\\Documents"')
    clone_repo(github_url)
=======
    os.system('copy "./src/orders.db" "C:\\Users\\mohak\\Documents"')
    clone_repo(github_url)
>>>>>>> Stashed changes
    shutil.rmtree("src")
    os.mkdir("src")
    shutil.copytree(os.path.join(os.getcwd(),"Dashboard\\src"), os.path.join(os.getcwd(),"src"))
    os.system(f'copy  "C:\\Users\\mohak\\Documents\\orders.db" {os.path.join(os.getcwd(),"src")}')
    print("update complete")
    sys.exit(1)
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
