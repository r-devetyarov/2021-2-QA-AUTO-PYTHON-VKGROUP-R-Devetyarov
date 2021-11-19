import enum
from pathlib import Path


class ConstantsForTests(str, enum.Enum):
    PATH_TO_ACCESS_LOG = Path("/home/renatdevetyarov/downloads/access.log")
