from enum import Enum

class Category(Enum):
    FOOD = 'food'
    TRANSPORT = 'transport'
    ENTERTAINMENT = 'entertainment'
    BILLS = 'bills'
    OTHER = 'inne'


    @classmethod
    def list_names(cls):
        """Returns list of enums"""
        return [c.value for c in cls]

