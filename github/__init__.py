import logging
import os

logger: logging.Logger = logging.getLogger(__name__)

class Config:
  def __init__(self) -> None:
    gh_token_env = "GITHUB_TOKEN"

    # Check if the environment variable exists
    self.access_token = os.environ.get(gh_token_env)
    if self.access_token is not None:
        # The environment variable exists
      logger.info(f"{self.access_token} exists with value: {self.access_token}")
    else:
        # The environment variable does not exist
      logger.warning(f"{self.access_token} does not exist.")
