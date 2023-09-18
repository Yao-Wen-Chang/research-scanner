import sys
import github
import requests

class Scrapper:
  def __init__(self):
    self.access_token = github.Config().access_token
    self.url = "https://api.github.com/search/repositories"
    self.language = ['java', 'python']
    self.params = {
      'q': f'language:{self.language}',  # Filter for repositories with more than 0 stars
      'sort': 'stars',  # Sort by stars
      'order': 'desc',  # Sort in descending order (most stars first)
      'per_page': 100,  # Number of results per page (max is 100)
      'page': 1,  # Page number (start with 1)
    }
    self.headers = {
      'Authorization': f'token {self.access_token}',
    }
    
  def run(self) -> list:
    if self.access_token is None:
      print(f"Warning: {self.access_token} environment variable is not set.")
      sys.exit(1)    

    repos = []
    
    # Send the GET request to the GitHub API
    response = requests.get(self.url, params=self.params, headers=self.headers)

    # Check if the request was successful
    if response.status_code == 200:
      # Parse the JSON response
      data = response.json()
      for repo in data['items']:
        owner, repo_name = repo['owner']['login'], repo['name']
        repos.append(f"{owner}/{repo_name}")
        
      return repos
    else:
      print(f"Error: {response.status_code} - {response.text}")