from starlette.config import Config
config = Config(".env")

# General
API_PREFIX = config("API_PREFIX", default="/api/mom")
PROJECT_NAME = config("PROJECT_NAME", default="MoM Service")
DEBUG = config("DEBUG", cast=bool, default=True)
VERSION = config("VERSION", default="")