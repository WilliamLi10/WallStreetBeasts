from pathlib import Path
from dotenv import load_dotenv
import environ
env = environ.Env()
environ.Env.read_env()

load_dotenv('email.env')


api_key = 