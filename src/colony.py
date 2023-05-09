import static.settings as settings
from src.entity import Entity


class Colony:
    def __init__(self):
        self.members = {}
    
    def add_member(self, entity: Entity) -> None:
        self.members[entity.loc] = entity
