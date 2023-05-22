from src.entities.entity import Entity


class Colony:
    def __init__(self):
        self.members = []
        self.total_members = 0
        self.border = []
    
    def add_member(self, entity: Entity) -> None:
        self.members.append(entity)
        entity.colony = self
        self.total_members += 1
    
    def remove_member(self, entity: Entity) -> None:
        self.members.remove(entity)
    
    def broken(self) -> bool:
        pass

    def _build_border(self) -> None:
        e: Entity
        for e in self.members:
            edges = e.get_edges()
