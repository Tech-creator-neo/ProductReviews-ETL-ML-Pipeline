import os
from git import Repo

def push_folder_to_github(
    folder_path: str,
    repo_url: str,
    commit_message: str = "Auto commit",
    branch: str = "main",
):
    # If folder is not already a git repo, initialize it
    git_dir = os.path.join(folder_path, ".git")
    if not os.path.exists(git_dir):
        print("Initializing new Git repository...")
        repo = Repo.init(folder_path)
        repo.create_remote("origin", repo_url)
    else:
        repo = Repo(folder_path)
        # Ensure remote exists / is correct
        if "origin" not in [r.name for r in repo.remotes]:
            repo.create_remote("origin", repo_url)
        else:
            repo.remotes.origin.set_url(repo_url)

    # Ensure we're on the correct branch
    if branch not in repo.heads:
        repo.git.checkout("-b", branch)
    else:
        repo.git.checkout(branch)

    # Add all files
    repo.git.add(all=True)

    # Commit (if there are changes)
    if repo.is_dirty(untracked_files=True):
        repo.index.commit(commit_message)
        print("Committed successfully.")
    else:
        print("Nothing to commit (no changes).")

    # Push to GitHub
    print("Pushing to GitHub...")
    origin = repo.remote(name="origin")
    origin.push(refspec=f"{branch}:{branch}")
    print("Push completed.")


if __name__ == "__main__":
    FOLDER_TO_PUSH = "/Users/jessica/Desktop/APP/ProductReviews-ETL-ML-Pipeline"
    GITHUB_REPO_URL = " https://github.com/Tech-creator-neo/ProductReviews-ETL-ML-Pipeline.git"
    COMMIT_MSG = "Initial commit"

    push_folder_to_github(FOLDER_TO_PUSH, GITHUB_REPO_URL, COMMIT_MSG)
