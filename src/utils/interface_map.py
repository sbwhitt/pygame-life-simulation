import src.utils.utils as utils
from src.interface.interface_element import InterfaceElement


class InterfaceMap:
    def __init__(self):
        self.elements = []

    def add_element(self, element: InterfaceElement) -> None:
        self.elements.append(element)

    def within_element(self, pos: tuple) -> InterfaceElement|None:
        e: InterfaceElement
        for e in self.elements:
            if not e.hidden and utils.within_rect(pos, e.rect):
                return e
        return None
