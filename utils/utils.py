'''Utils file'''
from settings.base import ENV


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

    @classmethod
    def display(cls, text: str, color: str) -> None:
        '''Display the text with color if not in production'''
        if ENV == 'production':
            print(f'{text}')
        print(f'{BColors.BOLD}{color}{text}{BColors.ENDC}')


# pylint: disable=too-few-public-methods
class BColors:
    '''Design default colors value to be used when printing messages'''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
