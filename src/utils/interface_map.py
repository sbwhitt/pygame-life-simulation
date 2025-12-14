import utils.utils as utils
from interface.interface_element import InterfaceElement


class InterfaceMap:
    def __init__(self):
        self.elements = []
        self.active = False

    def add_element(self, element: InterfaceElement) -> None:
        self.elements.append(element)

    def within_element(self, pos: tuple) -> InterfaceElement|None:
        e: InterfaceElement
        for e in self.elements:
            if not e.hidden and utils.within_rect(pos, e.rect):
                self.active = True
                return e
        self.active = False
        return None
