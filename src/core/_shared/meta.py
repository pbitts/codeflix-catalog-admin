from dataclasses import dataclass


@dataclass
class ListOutputMeta:
    current_page: int
    per_page: int
    total: int