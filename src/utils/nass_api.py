from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables from .env file
# Load from project root regardless of where script is called from
# __file__ is the path of this script
# .parent.parent.parent goes up three levels to project root
# / '.env' appends the .env file
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Expose configuration
NASS_API_KEY = os.getenv('NASS_API_KEY')