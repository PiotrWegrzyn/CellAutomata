from controler.BaseController import BaseController
from controler.BinaryRuleSetController import BinaryRuleSetController
from controler.GameOfLifeController import GameOfLifeController


class MainController(BaseController):
    modes = {
        "Binary Rule": BinaryRuleSetController,
        "Game of Life": GameOfLifeController,
    }

    def __init__(self, view):
        super().__init__(view)
