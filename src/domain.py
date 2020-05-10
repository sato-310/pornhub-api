from dataclasses import dataclass


@dataclass
class Video:
    id: int
    title: str
    thumbnail_url: str
    view_key: str
