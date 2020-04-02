from enum import Enum
import re


class ItemType(Enum):
    TITULO = 1
    CAPITULO = 2
    SECCION = 3
    ARTICULO = 4


# Patterns
tit_pattern = re.compile(r"^(Título|TÍTULO) (.+?) - (.+)$")
cap_pattern = re.compile(r"^(Capítulo|CAPÍTULO) (.+?) - (.+?)$")
sec_pattern = re.compile(r"^(Sección|SECCIÓN) (.+?) - (.+?)$")
art_pattern = re.compile(r"^(Artículo|ARTÍCULO) (\d+?) - (.+)$")


def identify_item(text: str) -> ItemType:
    """Identify a string as an item from the document.

    Returns a tuple with the following format:
    (ItemType, enumeration, text)"""
    item_match = tit_pattern.match(text)
    if item_match:
        return LegalDocItem(ItemType.TITULO, *item_match.groups()[1:])

    item_match = cap_pattern.match(text)
    if item_match:
        return LegalDocItem(ItemType.CAPITULO, *item_match.groups()[1:])

    item_match = sec_pattern.match(text)
    if item_match:
        return LegalDocItem(ItemType.SECCION, *item_match.groups()[1:])

    item_match = art_pattern.match(text)
    if item_match:
        return LegalDocItem(ItemType.ARTICULO, *item_match.groups()[1:])

    return None


class LegalDocItem:
    def __init__(self, itemtype, enumeration, text):
        self.itemtype = itemtype
        self.enumeration = enumeration
        if itemtype != ItemType.ARTICULO:
            self.text = text.title()
        else:
            self.text = text.title()
