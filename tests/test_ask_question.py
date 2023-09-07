# tests/test_ask_question.py
import unittest.mock
from sys import stderr
from tty_ov import TTY, ColouriseOutput, AskQuestion

ERR = 84
ERROR = ERR
SUCCESS = 0
COLOUR_LIB = ColouriseOutput()
COLOUR_LIB.init_pallet()
ASK_QUESTION = AskQuestion()
CONSTANTS = {
    "default": "0A",
    "prompt": "0B",
    "error": "0C",
    "success": "03",
    "info": "0D",
    "reset": "rr",
    "help_title_colour": "0E",
    "help_command_colour": "0A",
    "help_description_colour": "0F",
    "env_term_colour": "09",
    "env_shell_colour": "03",
    "env_definition_colour": "0B",
    "session_name_colour": "0D"
}
COLOURISE_OUTPUT = True


def print_debug(string: str = "") -> None:
    """ Print debug messages """
    debug = False
    if debug is True:
        print(f"DEBUG: {string}", file=stderr)


def test_get_author() -> None:
    TTYI = TTY(
        ERR,
        ERROR,
        SUCCESS,
        COLOUR_LIB,
        ASK_QUESTION,
        CONSTANTS,
        COLOURISE_OUTPUT
    )
    response = TTYI.author([])
    print_debug(f"response = {response}")
    assert response == TTYI.success

def test_get_version() -> None:
    TTYI = TTY(
        ERR,
        ERROR,
        SUCCESS,
        COLOUR_LIB,
        ASK_QUESTION,
        CONSTANTS,
        COLOURISE_OUTPUT
    )
    response = TTYI.version([])
    print_debug(f"response = {response}")
    assert response == TTYI.success

