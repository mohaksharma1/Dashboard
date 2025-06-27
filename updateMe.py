import os
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

# Example usage
if __name__ == "__main__":
    github_url = "https://github.com/mohaksharma1/Dashboard.git"  # Replace with your desired repo
    clone_repo(github_url)
