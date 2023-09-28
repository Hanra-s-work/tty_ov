# tests/test_tty_ov.py
import os
import sys
import pytest
import unittest
import unittest.mock
from sys import stderr
from platform import system
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


def test_get_help() -> None:
    """ Get the help section """
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
    response = TTYI.help([])
    print_debug(f"response = {response}")
    TTYI.unload_basics()
    assert response == TTYI.success


def test_get_help_hello_world() -> None:
    """ Get help about the hello_world function """
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
    response = TTYI.help(["hello_world"])
    print_debug(f"response = {response}")
    TTYI.unload_basics()
    assert response == TTYI.success


def test_list_to_str() -> None:
    """ Convert a list to a string """
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
    test_input = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
                  "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    expected_response = "a b c d e f g h i j k l m n o p q r s t u v w x y z"
    response = TTYI.list_to_str(test_input)
    print_debug(f"response = {response}")
    TTYI.unload_basics()
    assert response == expected_response


def test_get_history() -> None:
    """ Get the history of the library """
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
    TTYI.user_input = "help"
    TTYI.process_input()
    response = TTYI.show_history([])
    print_debug(f"response = {response}")
    TTYI.unload_basics()
    assert response == TTYI.success


def test_ls() -> None:
    """ Test the ls function """
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
    response = TTYI.bind_ls(["."])
    print_debug(f"response = {response}")
    TTYI.unload_basics()
    assert response == TTYI.success


def test_change_directory() -> None:
    """ Test the change of a directory """
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
    response1 = TTYI.change_directory(["/tmp"])
    response2 = TTYI.change_directory(["-"])
    print_debug(f"response = {response1}")
    TTYI.unload_basics()
    assert response1 == TTYI.success
    assert response2 == TTYI.success


def test_make_directory() -> None:
    """ Test the creation of a directory """
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
    response1 = TTYI.change_directory(["/tmp"])
    response2 = TTYI.make_directory(["/tmp/test"])
    response3 = TTYI.change_directory(["-"])
    print_debug(f"response = {response1}")
    TTYI.unload_basics()
    assert response1 == TTYI.success
    assert response2 == TTYI.success
    assert response3 == TTYI.success


def test_create_file() -> None:
    """ Test the creation of a file """
    TTYI = TTY(
        ERR,
        ERROR,
        SUCCESS,
        COLOUR_LIB,
        ASK_QUESTION,
        CONSTANTS,
        COLOURISE_OUTPUT
    )
    file_name = "./test_file_test_tty_ov"
    TTYI.load_basics()
    response = TTYI.touch([file_name])
    print_debug(f"response = {response}")
    TTYI.unload_basics()
    if system() == "Windows":
        os.system(f"del {file_name}")
    else:
        os.system(f"rm -f {file_name}")
    assert response == TTYI.success


@unittest.mock.patch('builtins.input', side_effect=["y"])
def test_remove_directory(mock_input) -> None:
    """ Test the removal of a directory """
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
    response = TTYI.remove_directory(["/tmp/test"])
    print_debug(f"response = {response}")
    TTYI.unload_basics()
    assert response == TTYI.success


@unittest.mock.patch('builtins.input', side_effect=["y"])
def test_remove_file(mock_input) -> None:
    """ Test the removal of a file """
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
    file_name = "test_file_tty_ov"
    if system() == "Windows":
        os.system(f"echo. > {file_name}")
    else:
        os.system(f"touch {file_name}")
    response = TTYI.remove_file([file_name])
    print_debug(f"response = {response}")
    TTYI.unload_basics()
    assert response == TTYI.success


def test_pwd() -> None:
    """ Test the removal of a file """
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
    response = TTYI.pwd([])
    print_debug(f"response = {response}")
    TTYI.unload_basics()
    assert response == TTYI.success


def test_status_code() -> None:
    """ Test the removal of a file """
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
    response = TTYI.display_status_code([])
    print_debug(f"response = {response}")
    TTYI.unload_basics()
    assert response == TTYI.success


def test_run_command() -> None:
    """ Test the run function """
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
    response = TTYI.run_command(["echo", "'Hello", "World'"])
    print_debug(f"response = {response}")
    TTYI.unload_basics()
    assert response == TTYI.success


input_args_1 = [
    "script_name.py",
    "hello_world",
    "hi",
    "how",
    "are",
    "you",
    "@#",
    "exit"
]


def compile_hello_world_arguments(input_args: list[str]) -> str:
    """ Compile the arguments for the hello_world function """
    function_prompt = "Hello World !\n"
    result = ""
    current_index = 0
    for index, item in enumerate(input_args[1:]):
        if item == "@#":
            current_index = index + 1
        if item == "hello_world":
            current_index += 1
            result += function_prompt
        result += f"{index-current_index}: '{item}'\n"
    return result


expected_result_1 = f"{compile_hello_world_arguments(input_args_1)}Leaving Parent session\n"


@pytest.mark.parametrize(
    "command_line_args, expected_result",
    [
        (
            input_args_1,
            expected_result_1
        )
    ]
)
def test_commands_via_arguments(command_line_args, expected_result) -> None:
    """ Test the run function """
    original_argv = sys.argv.copy()
    try:
        # Set sys.argv to the command_line_args for this test case
        sys.argv = command_line_args.copy()
        TTYI = TTY(
            ERR,
            ERROR,
            SUCCESS,
            COLOUR_LIB,
            ASK_QUESTION,
            CONSTANTS,
            False
        )

        TTYI.load_basics()
        # The function that will call sys.argv (inside of it)
        response = TTYI.mainloop("main")
        print_debug(f"response = {response}")
        TTYI.unload_basics()
    finally:
        sys.argv = original_argv
    assert response == TTYI.success


multy_oneliner_input_args_1 = [
    "script_name.py",
    "hello_world",
    "hi",
    "how",
    "are",
    "you",
    "@#",
    "exit"
]
multy_oneliner_expected_result_1 = compile_hello_world_arguments(
    multy_oneliner_input_args_1[:len(multy_oneliner_input_args_1)]
)
multy_oneliner_expected_result_1 += "Leaving Parent session\n"
multy_oneliner_input_args_2 = [
    "script_name.py",
    "hello_world",
    "@#",
    "hello_world",
    "@#@#",
    "hello_world",
    "@#",
    "@#",
    "hello_world",
    "@#",
    "exit"
]
multy_oneliner_expected_result_2 = compile_hello_world_arguments(
    multy_oneliner_input_args_2[:len(multy_oneliner_input_args_1)]
)
multy_oneliner_expected_result_2 += "Leaving Parent session\n"
multy_oneliner_input_args_3 = [
    "script_name.py",
    "hello_world",
    "@#",
    "hello_world",
    "hi",
    "how",
    "are",
    "you",
    "you",
    "@#@#",
    "hello_world",
    "you",
    "@#",
    "hello_world",
    "you",
    "@#",
    "exit"
]
multy_oneliner_expected_result_3 = compile_hello_world_arguments(
    multy_oneliner_input_args_3[:len(multy_oneliner_input_args_1)]
)
multy_oneliner_expected_result_3 += "Leaving Parent session\n"


@pytest.mark.parametrize(
    "command_line_args, expected_result",
    [
        (
            multy_oneliner_input_args_1,
            multy_oneliner_expected_result_1
        ),
        (
            multy_oneliner_input_args_2,
            multy_oneliner_expected_result_2
        ),
        (
            multy_oneliner_input_args_3,
            multy_oneliner_expected_result_3
        )
    ]
)
def test_multy_oneliner_commands_via_arguments(command_line_args, expected_result) -> None:
    """ Test the run function """
    original_argv = sys.argv.copy()
    try:
        # Set sys.argv to the command_line_args for this test case
        sys.argv = command_line_args.copy()
        TTYI = TTY(
            ERR,
            ERROR,
            SUCCESS,
            COLOUR_LIB,
            ASK_QUESTION,
            CONSTANTS,
            False
        )

        TTYI.load_basics()
        # The function that will call sys.argv (inside of it)
        response = TTYI.mainloop("main")
        print_debug(f"response = {response}")
        TTYI.unload_basics()
    finally:
        sys.argv = original_argv
    assert response == TTYI.success
