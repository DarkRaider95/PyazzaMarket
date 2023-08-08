class GameStatus:
    def __init__(self):
        self.__throw_dices_turn = True
        self.__throw_dices_special = True
        self.__buy_property = False
        self.__pass_turn = False

    def set_throw_dices_turn(self, value: bool) -> None:
        self.__throw_dices_turn = value

    def set_throw_dices_special(self, value: bool) -> None:
        self.__throw_dices_special = value

    def set_buy_property(self, value: bool) -> None:
        self.__buy_property = value

    def set_pass_turn(self, value: bool) -> None:
        self.__pass_turn = value
