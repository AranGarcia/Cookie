# Module for parsing Legal documents
import yaml

from items import ItemType, LegalDocItem


class LegalFileStructure:
    def __init__(self):
        self.content = {}

        # State variables
        self.__last_item = None
        self.__current_item = None
        self.__stack = []

    def write_file(self, fname) -> None:
        with open(fname, "w", encoding="utf-8") as f:
            yaml.dump(self.content, stream=f, encoding="utf-8", allow_unicode=True)

    def add_item(self, item: LegalDocItem) -> None:
        if not isinstance(item, LegalDocItem):
            raise ValueError(f"invalid type {item}")

        self.__last_item = self.__current_item
        self.__current_item = item
        if self.__last_item is None:
            if self.__current_item is not None:
                # Initial state
                self.__stack.append(item.itemtype)
                self.content["level"] = item.itemtype.name
                self.content["items"] = [
                    {"text": item.text, "enum": item.enumeration, "content": {}}
                ]
            return
        else:
            self.__calculate_state()
            self.__update()

    def __calculate_state(self):
        # State machine
        last_item = self.__last_item.itemtype
        current_item = self.__current_item.itemtype

        if last_item.value < current_item.value:
            # Current item is a child of last item
            self.__stack.append(current_item)
        elif last_item.value > current_item.value:
            # Find a node in the same level
            while self.__stack[-1].value > current_item.value:
                self.__stack.pop()

    def __update(self):
        content = self.content["items"][-1]["content"]
        for i in range(len(self.__stack) - 2):
            content = content["items"][-1]["content"]

        item_dict = {
            "text": self.__current_item.text,
            "enum": self.__current_item.enumeration,
        }
        # Item of type ARTICULO don't have 'items' nor 'content'
        if self.__current_item.itemtype != ItemType.ARTICULO:
            item_dict["items"] = []
            item_dict["content"] = {}

        if not content:
            content["level"] = self.__current_item.itemtype.name
            content["items"] = [item_dict]
        else:
            content["items"].append(item_dict)
