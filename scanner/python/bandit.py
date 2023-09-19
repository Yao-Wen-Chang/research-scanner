import logging
import os
import re
import subprocess
import sys
import tempfile

logger: logging.Logger = logging.getLogger(__name__)

current_dir = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.join(current_dir, "..", "utils")

sys.path.append(utils_dir)

import utils
from utils.api import API


class Bandit:
  def __init__(self, repo_owner: str, repo_name: str) -> None:
    self.repo_owner = repo_owner
    self.repo_name = repo_name
    self.variables = {
        "owner": self.repo_owner,
        "name": self.repo_name,
      }
    self.headers = {
        "Authorization": f"Bearer {utils.getenv('GITHUB_TOKEN')}",
        "Content-Type": "application/json",
      }
    self.query = """
        query ($owner: String!, $name: String!, $expression: String!) {
          repository(owner: $owner, name: $name) {
            object(expression: $expression) {
              ... on Tree {
                entries {
                  name
                  type
                  object {
                    ... on Blob {
                      text
                    }
                  }
                }
              }
            }
          }
        }
      """
    self.timeout = 10

  def scan(self, expression: str) -> None:
    """Recursively scan through all files in repo

    Args:
        expression (str): Path to the file. Also able to be commit sha, but required modified
    """
    self.variables["expression"] = expression
    self.api = API(
      url="https://api.github.com/graphql",
      query= self.query,
      variables=self.variables,
      headers=self.headers,
      timeout=self.timeout
    )
    data = self.api.post()
    try:
      for entry in data["data"]["repository"]["object"]["entries"]:
        name = entry["name"]
        if entry["type"] == "blob":
          pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*\.py$'
          if re.match(pattern, name):
            print("check")
            text = entry["object"]["text"]
            # Do something with the source code (e.g., save to files)
            # print(f"File Name: {name}")
            # print(f"Source Code:\n{text}\n{'=' * 50}\n")
            # print(text)
            with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
              # Write your plain text content to the temporary file
              temp_file.write(text)
            bandit_command = [
              'bandit',
              temp_file.name  # You can also directly pass the code string here using '-' as the filename
            ]
            result = subprocess.run(bandit_command, capture_output=True, text=True)
            if result.returncode == 0:
              print(result.stdout)
            else:
              print("process fail")
            temp_file.close()  # Close the file handle
            temp_file.unlink()  # Delete the file
        elif entry["type"] == "tree":
          # Recursively fetch source code from subdirectories
          self.scan(f"{expression}{name}/")
    except:
      return None
      # print(f"error: {data}")
    # created_at = data["data"]["repository"]["created_at"]
    # logger.info(f"[+] {created_at}")
