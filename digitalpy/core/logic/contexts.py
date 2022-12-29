from enum import Enum


class Contexts(Enum):
    ATTRIBUTE_CTX = "resolve_attribute"
    ITEM_CTX = "resolve_item"