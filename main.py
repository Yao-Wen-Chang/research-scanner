import subprocess

from scanner.python.bandit import Bandit
from utils.scrapper import Scrapper


def data_scrapping() -> list:
  scrapper = Scrapper()
  repos_list = scrapper.run()
  return repos_list

def bandit_scanning(repo_owner, repo_name):
  bandit = Bandit(repo_owner=repo_owner, repo_name=repo_name)
  # Scan master branch
  bandit.scan("master:")

def main():
  repos_list = data_scrapping() # this will be fed into Macaron
  # print(repos_list)
  for repo in repos_list:
    repo_owner, repo_name = repo.split("/")
    bandit_scanning(repo_owner, repo_name)
    break
  # SCRIPT_PATH = ".""/scanner/python/bandit.sh"
  # repos_str = " ".join(repos_list)
  # bandit_process = subprocess.run(["bash", SCRIPT_PATH, repos_str], capture_output=True, text=True)
  # if bandit_process.returncode == 0:
  #   print(bandit_process.stdout)
  # else:
  #   print("process fail")

if __name__ == "__main__":
  main()
