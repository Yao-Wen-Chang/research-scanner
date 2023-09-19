import logging

import requests

logger: logging.Logger = logging.getLogger(__name__)

class API:
  def __init__(self, url:str, query, variables:dict, headers:dict, timeout:int=10) -> None:
    """Initialize the API client.

    Args:
      url (str): Remote identification
      query (_type_): _description_
      variables (dict): _description_
      headers (dict): _description_
      timeout (int, optional): Defaults to 10.
    """
    self.url = url
    self.query = query
    self.variables = variables
    self.headers = headers
    self.timeout = timeout

  def post(self) -> dict:
    """This is a POST method for fetching data.

    Returns:
      dict: _description_
    """
    response = requests.post(
      self.url,
      timeout=self.timeout,
      json={"query": self.query, "variables": self.variables},
      headers=self.headers,
    )
    # print(response.text)
    if response.status_code == 200:
      return response.json()
    else:
      logger.error("%s, %s", response.status_code, response.text)
