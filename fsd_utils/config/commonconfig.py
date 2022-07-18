import os

class CommonConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")