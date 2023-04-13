"""This module is aimed at making assisting methods or functions to help other main classes or functions."""
import random as rm
import re


class Sanitizer:
    """
    A class for text sanitization for security reasons.
    """

    def filevalid(self, file_name: str, allowed_formats: list | tuple) -> bool:
        """
        Checks if the file given is the one with the allowed formats.
        """

        for af in allowed_formats:
            if file_name.endswith(af):
                return True
        return False


    def sanitize(self, text: str, clean: str) -> str:
        """
        Cleans every symbol that is not allowed in a text.
        """

        symbols = re.compile(clean)

        return symbols.sub(text)


    def valid(self, text: str, not_allowed: str) -> bool:
        """
        Checks if the given text does not include any not allowed characters in it.
        """

        symbols = re.compile(not_allowed)
        if text:
            return True if not symbols.findall(text) else False
        else:
            return None


def generate_token(length: int = 20) -> str:
    """
    An assisting function that generates tokens used for different purposes.
    """

    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    output = ''
    while len(output) < length:
        chosen = rm.choice(characters)
        output += chosen
    
    return output


def is_space_only(string: str) -> bool:
    """
    An assisting function that checks if the string provided is a space-only string.
    """

    space = re.compile(r'^\s+$')

    return True if space.fullmatch(string) else False
