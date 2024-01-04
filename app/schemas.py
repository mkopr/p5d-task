from dataclasses import dataclass
from typing import Optional


@dataclass
class ProjectInfo:
    """
    Data class to store information about a project.
    """

    hash: str
    name: str
    floor_count: int
    room_count: int


@dataclass
class ParsedData:
    """
    Generic data class to store parsed data.
    """

    project_info: Optional[ProjectInfo] = None
    extracted_param: Optional[str] = None
