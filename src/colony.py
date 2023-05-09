from src.entity import Entity


class Colony:
    def __init__(self):
        self.members = []
        self.total_members = 0
    
    def add_member(self, entity: Entity) -> None:
        self.members.append(entity)
        self.total_members += 1
    
    def remove_member(self, entity: Entity) -> None:
        self.members.remove(entity)
