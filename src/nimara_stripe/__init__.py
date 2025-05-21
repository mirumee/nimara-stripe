from importlib.metadata import metadata, version

PROJECT_NAME = metadata(__name__)["Name"]
VERSION = version(__name__)
