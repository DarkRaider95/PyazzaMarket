"""This module is used to store the status of the game and the status of the player"""


class ActionsStatus:
    """This class is used to store the status of the game and the status of the player"""

    def __init__(self):
        # This are the booleand for the button of the game and
        # they are used also to check what the player can do
        self.__throw_dices = False
        self.__buy_property = False
        self.__show_stock = False
        self.__pass_turn = False
        self.__saved_actions = []

    def disable_actions(self) -> None:
        "This function save all istances of the class and then set them to false"

        # Get the dictionary of instance variables using vars()
        attributes = vars(self)

        # Check if the action are already saved
        if not self.__saved_actions:
            # Iterate over the boolean attributes
            for attribute_name, value in attributes.items():
                if isinstance(value, bool):
                    self.__saved_actions.append(value)
                    setattr(self, attribute_name, False)

    def renable_actions(self) -> None:
        "This function restore all the actions saved in the saved_actions list"

        # Get the dictionary of instance variables using vars()
        attributes = vars(self)

        # Iterate over the boolean attributes
        for attribute_name, value in attributes.items():
            if isinstance(value, bool):
                # Leave the saved actions empty in order to know when the actions are already saved
                setattr(self, attribute_name, self.__saved_actions.pop(0))

    def get_actions_status(self) -> list:
        """Return the list of the boolean values of the actions"""

        # Get the dictionary of instance variables using vars()
        attributes = vars(self)

        # Iterate over the boolean attributes and return the values
        return [value for value in attributes.values() if isinstance(value, bool)]

    def set_throw_dices(self, value: bool) -> None:
        """Set the value of the throw_dices_turn boolean"""
        self.__throw_dices = value

    def set_buy_property(self, value: bool) -> None:
        """Set the value of the buy_property boolean"""
        self.__buy_property = value

    def set_show_stock(self, value: bool) -> None:
        """Set the value of the show_stock boolean"""
        self.__show_stock = value

    def set_pass_turn(self, value: bool) -> None:
        """Set the value of the pass_turn boolean"""
        self.__pass_turn = value

    def get_throw_dices(self) -> bool:
        """Return the value of the throw_dices_turn boolean"""
        return self.__throw_dices

    def get_buy_property(self) -> bool:
        """Return the value of the buy_property boolean"""
        return self.__buy_property

    def get_show_stock(self) -> bool:
        """Return the value of the show_stock boolean"""
        return self.__show_stock

    def get_pass_turn(self) -> bool:
        """Return the value of the pass_turn boolean"""
        return self.__pass_turn