'''Utils file'''

# pylint: disable=too-few-public-methods
class Utils:
    '''A class field with useful small methods'''

    @classmethod
    def is_integer(cls, value: str) -> bool:
        '''Check if the value is an integer'''
        try:
            float(value)
        except ValueError:
            return False
        return float(value).is_integer()
