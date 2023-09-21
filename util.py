import os


def getFilePathFromData(filename: str) -> str:
    return os.path.join("data", filename)