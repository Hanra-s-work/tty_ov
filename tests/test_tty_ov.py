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


def print_debug(string: str = "") -> None:
    """ Print debug messages """
    debug = False
    if debug is True:
        print(f"DEBUG: {string}", file=stderr)


def _initialise_class(argv: list) -> TTY:
    """ Load the main class of the program for testing """
    colourise_output = True
    if "-nc" in argv or "--no-colour" in argv:
        colourise_output = False
    ttyi = TTY(
        ERR,
        ERROR,
        SUCCESS,
        COLOUR_LIB,
        ASK_QUESTION,
        CONSTANTS,
        colourise_output
    )
    ttyi.load_basics()
    return ttyi


def _de_initialise_class(tty: TTY) -> int:
    """ Unload the tty class of the program """
    status = tty.unload_basics()
    tty = None
    return status


def _list_dict_to_dict(list_dict: list[dict]) -> dict:
    """ Transform a list of dictionary into a dictionary """
    result = {}
    for i in list_dict:
        result.update(i)
    return result


def _list_to_dict(list_input: list, filler: any) -> dict:
    """ Transform a list into a dictionary """
    filler_list = [filler] * len(list_input)
    tuples = zip(list_input, filler_list)
    result = dict(tuples)
    return result


def compile_hello_world_arguments(input_args: list[str]) -> str:
    """ Compile the arguments for the hello_world function """
    function_prompt = "Hello World !\n"
    invalid_option_prompt = "Invalid option\n"
    result = ""
    prev = ""
    current_index = 0
    for index, item in enumerate(input_args[1:]):
        if item == "@#" and prev == "@#":
            result += invalid_option_prompt
        if item == "@#":
            current_index = index + 1
            prev = item
            continue
        if item == "exit":
            return result
        if item == "hello_world":
            current_index += 1
            result += function_prompt
            prev = item
            continue
        result += f"{index-current_index}: '{item}'\n"
        prev = item
    return result


def test_get_author() -> None:
    """ Get the name of the author of the program """
    TTYI = _initialise_class([])
    response = TTYI.author([])
    print_debug(f"response = {response}")
    status = _de_initialise_class(TTYI)
    assert response == TTYI.success
    assert status == TTYI.success


def test_get_version() -> None:
    """ Get the version of the library """
    TTYI = _initialise_class([])
    response = TTYI.version([])
    print_debug(f"response = {response}")
    status = _de_initialise_class(TTYI)
    assert response == TTYI.success
    assert status == TTYI.success


def test_get_help() -> None:
    """ Get the help section """
    TTYI = _initialise_class([])
    response = TTYI.help([])
    print_debug(f"response = {response}")
    status = _de_initialise_class(TTYI)
    assert response == TTYI.success
    assert status == TTYI.success


def test_get_help_hello_world() -> None:
    """ Get help about the hello_world function """
    TTYI = _initialise_class([])
    response = TTYI.help(["hello_world"])
    print_debug(f"response = {response}")
    status = _de_initialise_class(TTYI)
    assert response == TTYI.success
    assert status == TTYI.success


def test_list_to_str() -> None:
    """ Convert a list to a string """
    TTYI = _initialise_class([])
    test_input = [
        "a", "b", "c", "d", "e", "f", "g",
        "h", "i", "j", "k", "l", "m", "n",
        "o", "p", "q", "r", "s", "t", "u",
        "v", "w", "x", "y", "z"
    ]
    expected_response = "a b c d e f g h i j k l m n o p q r s t u v w x y z"
    response = TTYI.list_to_str(test_input)
    print_debug(f"response = {response}")
    status = _de_initialise_class(TTYI)
    assert response == expected_response
    assert status == TTYI.success


def test_get_history() -> None:
    """ Get the history of the library """
    TTYI = _initialise_class([])
    TTYI.user_input = "help"
    TTYI.process_input()
    response = TTYI.show_history([])
    print_debug(f"response = {response}")
    status = _de_initialise_class(TTYI)
    assert response == TTYI.success
    assert status == TTYI.success


def test_ls() -> None:
    """ Test the ls function """
    TTYI = _initialise_class([])
    response = TTYI.bind_ls(["."])
    print_debug(f"response = {response}")
    status = _de_initialise_class(TTYI)
    assert response == TTYI.success
    assert status == TTYI.success


def test_change_directory() -> None:
    """ Test the change of a directory """
    TTYI = _initialise_class([])
    response1 = TTYI.change_directory(["/tmp"])
    response2 = TTYI.change_directory(["-"])
    print_debug(f"response = {response1}")
    status = _de_initialise_class(TTYI)
    assert response1 == TTYI.success
    assert response2 == TTYI.success
    assert status == TTYI.success


def test_make_directory() -> None:
    """ Test the creation of a directory """
    TTYI = _initialise_class([])
    response1 = TTYI.change_directory(["/tmp"])
    response2 = TTYI.make_directory(["/tmp/test"])
    response3 = TTYI.change_directory(["-"])
    print_debug(f"response = {response1}")
    status = _de_initialise_class(TTYI)
    assert response1 == TTYI.success
    assert response2 == TTYI.success
    assert response3 == TTYI.success
    assert status == TTYI.success


def test_create_file() -> None:
    """ Test the creation of a file """
    TTYI = _initialise_class([])
    file_name = "./test_file_test_tty_ov"
    response = TTYI.touch([file_name])
    print_debug(f"response = {response}")
    status = _de_initialise_class(TTYI)
    if system() == "Windows":
        os.system(f"del {file_name}")
    else:
        os.system(f"rm -f {file_name}")
    assert response == TTYI.success
    assert status == TTYI.success


@unittest.mock.patch('builtins.input', side_effect=["y"])
def test_remove_directory(mock_input) -> None:
    """ Test the removal of a directory """
    TTYI = _initialise_class([])
    response = TTYI.remove_directory(["/tmp/test"])
    print_debug(f"response = {response}")
    status = _de_initialise_class(TTYI)
    assert response == TTYI.success
    assert status == TTYI.success


@unittest.mock.patch('builtins.input', side_effect=["y"])
def test_remove_file(mock_input) -> None:
    """ Test the removal of a file """
    TTYI = _initialise_class([])
    file_name = "test_file_tty_ov"
    if system() == "Windows":
        os.system(f"echo. > {file_name}")
    else:
        os.system(f"touch {file_name}")
    response = TTYI.remove_file([file_name])
    print_debug(f"response = {response}")
    status = _de_initialise_class(TTYI)
    assert response == TTYI.success
    assert status == TTYI.success


def test_pwd() -> None:
    """ Test the removal of a file """
    TTYI = _initialise_class([])
    response = TTYI.pwd([])
    print_debug(f"response = {response}")
    status = _de_initialise_class(TTYI)
    assert response == TTYI.success
    assert status == TTYI.success


def test_status_code() -> None:
    """ Test the removal of a file """
    TTYI = _initialise_class([])
    response = TTYI.display_status_code([])
    print_debug(f"response = {response}")
    status = _de_initialise_class(TTYI)
    assert response == TTYI.success
    assert status == TTYI.success


def test_run_command() -> None:
    """ Test the run function """
    TTYI = _initialise_class([])
    response = TTYI.run_command(["echo", "'Hello", "World'"])
    print_debug(f"response = {response}")
    status = _de_initialise_class(TTYI)
    assert response == TTYI.success
    assert status == TTYI.success


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

expected_result_1 = "Hello World !\n0: 'hi'\n1: 'how'\n2: 'are'\n3: 'you'\nLeaving program\n"


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
        status = _de_initialise_class(TTYI)
    finally:
        sys.argv = original_argv
    assert response == TTYI.success
    assert status == TTYI.success


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
multy_oneliner_expected_result_1 = "Hello World !\n0: 'hi'\n1: 'how'\n2: 'are'\n3: 'you'\nLeaving program\n"
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
multy_oneliner_expected_result_2 = ""
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
multy_oneliner_expected_result_3 = "Hello World !\nHello World !\n0: 'hi'\n1: 'how'\n2: 'are'\n3: 'you'\n4: 'you'\n5: '@#@#'\n6: 'hello_world'\n7: 'you'\nLeaving program\n"


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
        status = _de_initialise_class(TTYI)
    finally:
        sys.argv = original_argv
    assert response == TTYI.success
    assert status == TTYI.success


def test_help() -> None:
    """ Test the help functions in order to see if some are miss programmed """
    TTYI = _initialise_class([""])
    help_options = _list_dict_to_dict(TTYI.options)
    help_result = _list_to_dict(list(help_options), SUCCESS)
    for i in help_options:
        if i == "desc":
            continue
        TTYI.process_complex_input(["help", i])
        help_result[i] = TTYI.current_tty_status
    status0 = _de_initialise_class(TTYI)

    help_result_list = list(help_result.values())
    if ERR or ERROR in help_result_list:
        print(f"Help analysis result: {help_result}")
    assert ERROR not in help_result_list
    assert ERR not in help_result_list
    assert status0 == SUCCESS
