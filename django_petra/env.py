from dotenv import load_dotenv
import os

def load_env():
    load_dotenv()

def getEnv(key, default=None):
    return os.getenv(key, default)