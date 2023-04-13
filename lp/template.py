from django.template import Library
import re


register = Library()

# Simple tags go here
@register.simple_tag
def get_file_name(path: str) -> str:
    """
    A tag for returning the name of the given file from the full path.
    """
    if path:
        return str(path).split('/')[-1] if str(path).index('/') > -1 else str(path).split('\\')[-1]
    else:
        return 'Not found'


@register.simple_tag
def get_name(string: str, name_position: int) -> str:
    """
    A tag for retrieving the specific name of the user.
    """

    return string.split()[name_position]
