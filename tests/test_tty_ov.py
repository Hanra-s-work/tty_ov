# tests/test_tty_ov.py
from sys import stderr
from tty_ov import TTY
from tty_ov import ColouriseOutput
from tty_ov import AskQuestion

# print(f"(module help) = {help('modules')}")
# print(f"(help: TTY) = {help(TTY)}")
# print(f"(help: ColouriseOutput) = {help(ColouriseOutput)}")
# print(f"(help: AskQuestion) = {help(AskQuestion)}")

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
    """ Get the name of the author of the program """
    TTYI = TTY(
        ERR,
        ERROR,
        SUCCESS,
        COLOUR_LIB,
        ASK_QUESTION,
        CONSTANTS,
        COLOURISE_OUTPUT
    )
    TTYI.load_basics()
    response = TTYI.author([])
    print_debug(f"response = {response}")
    TTYI.unload_basics()
    assert response == TTYI.success


def test_get_version() -> None:
    """ Get the version of the library """
    TTYI = TTY(
        ERR,
        ERROR,
        SUCCESS,
        COLOUR_LIB,
        ASK_QUESTION,
        CONSTANTS,
        COLOURISE_OUTPUT
    )
    TTYI.load_basics()
    response = TTYI.version([])
    print_debug(f"response = {response}")
    TTYI.unload_basics()
    assert response == TTYI.success
