<!--
-- +==== BEGIN tty_ov =================+
-- LOGO: 
-- ..@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
-- .@...........................#@
-- @############################.@
-- @...........................@.@
-- @..#######################..@.@
-- @.#########################.@.@
-- @.##>_#####################.@.@
-- @.#########################.@.@
-- @.#########################.@.@
-- @.#########################.@.@
-- @.#########################.@.@
-- @..#######################..@.@
-- @...........................@.@
-- @..+----+______________.....@.@
-- @..+....+______________+....@.@
-- @..+----+...................@.@
-- @...........................@.#
-- @@@@@@@@@@@@@@@@@@@@@@@@@@@@@#.
-- /STOP
-- PROJECT: tty_ov
-- FILE: README.md
-- CREATION DATE: 06-11-2025
-- LAST Modified: 19:32:2 11-02-2026
-- DESCRIPTION: 
-- A tiny terminal (just the functions I need) cross-platform implemented in python.
-- /STOP
-- COPYRIGHT: (c) Henry Letellier
-- PURPOSE: The readme file in charge of explaining how to use the module.
-- // AR
-- +==== END tty_ov =================+
-->
# tty_ov

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tty_ov)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/tty_ov)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/tty_ov)
![PyPI - Version](https://img.shields.io/pypi/v/tty_ov?label=pypi%20package:%20tty_ov)
![PyPI - Downloads](https://img.shields.io/pypi/dm/tty_ov)
![PyPI - License](https://img.shields.io/pypi/l/tty_ov)
![Execution status](https://github.com/Hanra-s-work/tty_ov/actions/workflows/python-package.yml/badge.svg)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/Hanra-s-work/tty_ov/python-package.yml)
![GitHub repo size](https://img.shields.io/github/repo-size/Hanra-s-work/tty_ov)
![GitHub Repo stars](https://img.shields.io/github/stars/Hanra-s-work/tty_ov)
![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/m/Hanra-s-work/tty_ov)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/Hanra-s-work/tty_ov/main)

[![Static Badge](https://img.shields.io/badge/Buy_me_a_tea-Hanra-%235F7FFF?style=flat-square&logo=buymeacoffee&label=Buy%20me%20a%20coffee&labelColor=%235F7FFF&color=%23FFDD00&link=https%3A%2F%2Fwww.buymeacoffee.com%2Fhanra)](https://www.buymeacoffee.com/hanra)

## Take a look

This project now has automated documentation that gets generated, this manually written one will remain for legacy reasons, but you can now take a look at the automatic documentation here: [https://hanra-s-work.github.io/tty_ov/](https://hanra-s-work.github.io/tty_ov/)

## Description

## Table of Content

1. [tty_ov](#tty_ov)
2. [Description](#description)
3. [Table of Content](#table-of-content)
4. [Installation](#installation)
    1. [Using pip](#using-pip)
    2. [Using python](#using-python)
5. [Usage](#usage)
    1. [Running as a script](#running-as-a-script)
    2. [Importing](#importing)
    3. [Initialising](#initialising)
    4. [Using built-in commands](#using-built-in-commands)
6. [Features](#features)
    1. [Core Commands](#core-commands)
    2. [Advanced Features](#advanced-features)
    3. [Extensibility](#extensibility)
7. [Documentation](#documentation)
8. [Author](#author)
9. [Version](#version)

## Installation

### Using pip

```sh
pip install -U tty_ov
```

### Using python

Under Windows:

```bat
py -m pip install -U tty_ov
```

Under Linux/Mac OS:

```sh
python3 -m pip install -U tty_ov
```

## Usage

### Running as a script

You can run tty_ov directly as a script to start an interactive terminal session:

```sh
python -m tty_ov
```

This will launch the interactive TTY interface where you can execute commands.

### Importing

```py
from tty_ov import TTY
```

### Initialising

The generic class is: `TTY(err: int, error: int, success: int, colour_lib: ColouriseOutput, ask_question: AskQuestion, colours: Dict, colourise_output: bool = True)`

For your convenience, you can initialize the class with default parameters:

```py
from tty_ov import TTY, ColouriseOutput, AskQuestion

ERR = 84
ERROR = ERR
SUCCESS = 0
COLOUR_LIB = ColouriseOutput()
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

tty_instance = TTY(
    ERR,
    ERROR,
    SUCCESS,
    COLOUR_LIB,
    ASK_QUESTION,
    CONSTANTS,
    COLOURISE_OUTPUT
)
tty_instance.load_basics()
tty_instance.mainloop("Custom session")
tty_instance.unload_basics()
```

### Using built-in commands

Once initialized, you can use various built-in commands programmatically. Here are some examples:

#### File System Navigation

```py
# Change directory
tty_instance.change_directory(["/path/to/directory"])

# Print working directory
tty_instance.pwd([])

# List files
tty_instance.bind_ls([])
```

#### Environment Management

```py
# Display environment variables
tty_instance.env([])

# Set an environment variable
tty_instance.setenv(["MY_VAR", "my_value"])

# Unset an environment variable
tty_instance.unsetenv(["MY_VAR"])
```

#### Running External Commands

```py
# Run a system command
tty_instance.run_command(["echo", "Hello World"])
```

#### Session Management

```py
# Change session name
tty_instance.process_session_name(["new_session_name"])

# Show command history
tty_instance.show_history([])
```

## Features

tty_ov includes a variety of built-in commands and features:

### Core Commands

- **File System Navigation**: `cd`, `pwd`, `ls` (with colorized output)
- **File Operations**: `mkdir`, `touch`, `rm`, `rmdir`
- **System Interaction**: `run` (execute external commands), `super_run` (run with elevated privileges)
- **Environment Management**: `env`, `env++`, `setenv`, `unsetenv`
- **Session Management**: `session_name`, `history`
- **Information**: `version`, `author`, `client`, `is_admin`
- **Utilities**: `hello_world`, `?` (display last status code)

### Advanced Features

- **Piping Support**: Chain commands using pipes
- **Argument Input**: Full support for command-line arguments
- **Colorized Output**: Configurable color schemes for different output types
- **Command History**: Track and display previous commands
- **Help System**: Built-in help for all commands
- **Auto-completion**: Tab completion for commands
- **Multi-command Execution**: Execute multiple commands in sequence
- **Comment Support**: Ignore lines starting with comment tokens

### Extensibility

- **Custom Commands**: Import additional functions into the shell
- **Session Management**: Multiple named sessions
- **Configurable Tokens**: Customize command separators and comment tokens

## Documentation

Comprehensive Doxygen-generated documentation is available online at [https://hanra-s-work.github.io/tty_ov/](https://hanra-s-work.github.io/tty_ov/). This includes detailed API references, class documentation, and usage examples.

To generate the documentation locally, navigate to the `doxygen_generation` directory and run the provided scripts.

## Author

This module was written by (c) Henry Letellier
Attributions are appreciated.

## Version

The current version is 1.0.0

An easy way to display the version is:

```py
import tty_ov
print(f"Version : {tty_ov.__version__}")
```
