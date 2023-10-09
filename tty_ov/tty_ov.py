"""
File in charge of emulating a basic tty to universalise the interface
"""
import os
import sys
import stat
import time
import locale
import shutil
import prompt_toolkit
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.history import InMemoryHistory
from prettytable import PrettyTable
from ask_question import AskQuestion
from colourise_output import ColouriseOutput


class HLLs:
    """
    The basics of the ls function
    This code is borrowed from: https://github.com/connormason/lspython/tree/master
    I :
        - fixed this code's errors
        - made it cross-platform
        - implemented it into the program
        - adapted the code to fit into the shell's functionalities
    """

    def __init__(self, success: int = 0, error: int = 84) -> None:
        # ---- The colours for the TUI ----
        self.colors = {
            "default": "",
            "white": "\x1b[01;37m",
            "gray": "\x1b[00;37m",
            "purple": "\x1b[00;35m",
            "cyan": "\x1b[01;36m",
            "green": "\x1b[01;32m",
            "red": "\x1b[01;05;37;41m"
        }
        # ---- The status code ----
        self.success = success
        self.error = error

    def has_colors(self, stream) -> bool:
        """ Check if the ncurse library is present in the system for the colour management """
        if not hasattr(stream, "isatty"):
            return False
        if not stream.isatty():
            return False
        return False

    def get_mode_info(self, mode, filename):
        """ Get the type of document in order to apply some colour """
        perms = "-"
        color = "default"
        link = ""

        if stat.S_ISDIR(mode):
            perms = "d"
            color = "cyan"
        elif stat.S_ISLNK(mode):
            perms = "l"
            color = "purple"
            link = os.readlink(filename)
            if not os.path.exists(filename):
                color = "red"
        elif stat.S_ISREG(mode):
            if mode & (stat.S_IXGRP | stat.S_IXUSR | stat.S_IXOTH):
                color = "green"
            else:
                if filename[0] == '.':
                    color = "gray"
                else:
                    color = "white"

        mode = stat.S_IMODE(mode)

        for who in "USR", "GRP", "OTH":
            for what in "R", "W", "X":
                if mode & getattr(stat, "S_I" + what + who):
                    perms = perms + what.lower()
                else:
                    perms = perms + "-"

        return (perms, color, link)

    def get_user_info(self, uid) -> str:
        """ Get the info of the user """
        try:
            import pwd
            user_info = pwd.getpwuid(uid)
            return user_info.pw_name
        except ImportError:
            return str(uid)

    def get_group_info(self, gid) -> str:
        """ Get the pid of the active groupe """
        try:
            import grp
            group_info = grp.getgrgid(gid)
            return group_info.gr_name
        except ImportError:
            return str(gid)

    def list_files(self, files: list) -> int:
        """ List the files contained in the path """
        global_status = self.success
        table = PrettyTable(
            [
                "Permissions",
                "# Links",
                "Owner",
                "Group",
                "Size",
                "Last Mod",
                "Name"
            ]
        )

        locale.setlocale(locale.LC_ALL, '')
        files.sort(key=lambda x: x.lower())

        now = int(time.time())
        recent = now - (6 * 30 * 24 * 60 * 60)

        does_have_colors = self.has_colors(sys.stdout)

        for filename in files:
            try:
                stat_info = os.lstat(filename)
            except OSError:
                sys.stderr.write(f"{filename}: No such file or directory\n")
                global_status = self.error
                continue

            perms, color, link = self.get_mode_info(
                stat_info.st_mode,
                filename
            )

            nlink = f"{stat_info.st_nlink:4d}%4d"
            name = self.get_user_info(stat_info.st_uid)
            group = self.get_group_info(stat_info.st_gid)
            size = f"{stat_info.st_size:8d}"

            time_stamp = stat_info.st_mtime
            if (time_stamp < recent) or (time_stamp > now):
                time_fmt = "%b %e  %Y"
            else:
                time_fmt = "%b %e %R"
            time_str = time.strftime(time_fmt, time.gmtime(time_stamp))

            if self.colors[color] and does_have_colors:
                filename_str = self.colors[color] + filename + "\x1b[00m"
            else:
                filename_str = filename

            if link:
                filename_str += " -> "
            filename_str += link

            table.add_row(
                [
                    perms,
                    nlink,
                    name,
                    group,
                    size,
                    time_str,
                    filename_str
                ]
            )

        table.align["Permissions"] = 'l'
        table.align["# Links"] = 'r'
        table.align["Owner"] = 'l'
        table.align["Group"] = 'l'
        table.align["Size"] = 'r'
        table.align["Last Mod"] = 'l'
        table.align["Name"] = 'l'
        print(table)
        return global_status

    def ls(self, path: str or list = "") -> int:
        """ 
        A basic loop manager to make this P.O.S POC a minimum functional and feel like the core of the real ls
        """
        try:
            if path in ("", "."):
                content = os.listdir(".")
                return self.list_files(content)
            if ".." in path:
                tmp = os.getcwd()
                os.chdir(path)
                content = os.listdir(".")
                status = self.list_files(content)
                os.chdir(tmp)
                return status
            if isinstance(path, list):
                global_status = self.success
                for item in path:
                    print(f"Content of: {item}")
                    content = [item]
                    if os.path.isdir(item):
                        content = os.listdir(item)
                    status = self.list_files(content)
                    if status != self.success:
                        global_status = self.error
                return global_status
            if os.path.isdir(path):
                files = os.listdir(path)
                return self.list_files(files)
            files = [path]
            return self.list_files(files)
        except Exception as err:
            print(f"The pseudo Ls has crashed: {err}")
            return self.error


class TTY:
    """ The class in charge of simulating a tty """

    def __init__(self, err: int, error: int, success: int, colour_lib: ColouriseOutput, ask_question: AskQuestion, colours: dict, colourise_output: bool = True) -> None:
        # ---- The version of the program ----
        self.__version__ = "1.0.0"
        # ---- TTY general info ----
        self.program_version = self.__version__
        self.client_name = "(c) OpenValue"
        self.program_author = "(c) Henry Letellier"
        # ---- Command history ----
        self.history = []
        self.prompt_history = InMemoryHistory()
        self.history_index = 0
        # ---- The status codes ----
        self.success = success
        self.err = err
        self.error = error
        # ---- TTY layer tracking ----
        self.continue_tty_loop = True
        self.current_tty_status = self.success
        # ---- The dependency libraries ----
        self.colour_lib = colour_lib
        self.ask_question = ask_question
        # ---- The commands of the layer in which the TTY is currently located ----
        self.options = []
        # ---- Available TTY colours ----
        self.colours = self.colour_lib.unix_colour_pallet
        self.tty_colours = colours
        # ---- Pre-set TTY colours ----
        self.reset_colour = None
        self.prompt_colour = None
        self.default_colour = None
        self.error_colour = None
        self.success_colour = None
        self.info_colour = None
        # ---- User input tracking ----
        self.user_input = ""
        self.user_session = prompt_toolkit.PromptSession()
        self.input_split_char = " "
        # ---- function requirering help from the help function ----
        self.help_function_child_name = "help"
        # ---- Help colour ----
        self.help_title_colour = None
        self.help_command_colour = None
        self.help_description_colour = None
        # ---- Colour toggle ----
        self.colourise_output = colourise_output
        # ---- Environement variables colours ----
        self.env_term_colour = None
        self.env_shell_colour = None
        self.env_definition_colour = None
        # ---- Session Name ----
        self.session_name = "main"
        self.session_name_colour = None
        # ---- cd management ----
        self.old_pwd = os.getcwd()
        self.home = None
        # ---- A tiny ls implementation ----
        self.ls = HLLs(self.success, self.error)
        # ---- Master session name ----
        self.master_session = "main"
        # ---- Argument command tracking ----
        self.command_seperator_token = "@#"
        # ---- Comment Tracking ----
        self.comment_token = "--"
        # ---- Pipe input ----
        self.pipe_input = None
        # ---- Working on the auto-complete functionalities ----
        self.auto_complete_list = []
        self.auto_complete_index = 0
        self.auto_complete_usr_input = ""
        self.auto_complete_default_usr_input = ""

    def print_on_tty(self, colour: str, string: str) -> None:
        """ The function in charge of displaying a string on the tty """
        if self.colourise_output:
            self.colour_lib.display(colour, (), string)
        else:
            print(string, end="")

    def run_external_command(self, command: str) -> int:
        """ The function in charge of executing command on the host system in a contained manner """
        try:
            return os.system(command)
        except IOError:
            return self.error

    def list_to_str(self, hl_list: list[any], join: str = " ") -> str:
        """ Convert a list to a string """
        res = ""
        list_length = len(hl_list)-1
        for index, item in enumerate(hl_list):
            res += str(item)
            if index < list_length:
                res += join
        return res

    def version(self, args: list) -> int:
        """ Display the version of the program """
        func_name = "version"
        if self.help_function_child_name == func_name:
            help_description = f"""
Display the version of the program.
Usage Example:
Input:
    {func_name}
Output:
    {self.program_version}
"""
            self.function_help(func_name, help_description)
            self.current_tty_status = self.success
            return self.success
        self.print_on_tty(self.default_colour, "The program's version is: ")
        self.print_on_tty(self.success_colour, f"{self.program_version}\n")
        self.current_tty_status = self.success
        return self.success

    def show_history(self, args: list) -> int:
        """ Display the history of the commands """
        func_name = "history"
        if self.help_function_child_name == func_name:
            help_description = f"""
Display the history of the commands.
Usage Example:
Input:
    {func_name}
Output:
    The history of the commands
"""
            self.function_help(func_name, help_description)
            self.current_tty_status = self.success
            return self.success
        self.print_on_tty(
            self.default_colour,
            "The history of the commands:\n"
        )
        if len(self.history) > 0:
            for index, command in enumerate(self.history):
                self.print_on_tty(self.help_command_colour, f"{index}")
                self.print_on_tty(self.help_title_colour, ": ")
                self.print_on_tty(
                    self.help_description_colour, f"'{command}'\n")
        else:
            self.print_on_tty(self.error_colour, "No history available\n")
        self.current_tty_status = self.success
        return self.success

    def process_session_name(self, args: list) -> int:
        """ Change the name of the current session """
        func_name = "session_name"
        if self.help_function_child_name == func_name:
            help_description = f"""
Change the name of the current session.
If no arguments are passed, the name of the session is displayed
If one argument is passed, the name of the session is changed to the passed in argument
Usage Example:
Input:
    {func_name}
Output:
    The name of the session is: {self.session_name}
Input:
    {func_name} test
Output:
    The name of the session is changed to: 'test'
"""
            self.function_help(func_name, help_description)
            self.current_tty_status = self.success
            return self.success
        if len(args) == 0 or args[0] == '':
            self.print_on_tty(
                self.default_colour,
                "The name of the session is: "
            )
            self.print_on_tty(self.success_colour, f"'{self.session_name}'\n")
            self.current_tty_status = self.success
            return self.success
        self.session_name = self.list_to_str(args)
        self.print_on_tty(
            self.default_colour,
            "The name of the session is changed to: "
        )
        self.print_on_tty(self.success_colour, f"'{self.session_name}'\n")
        self.current_tty_status = self.success
        return self.success

    def author(self, args: list) -> int:
        """ Display the author of the program """
        func_name = "author"
        if self.help_function_child_name == func_name:
            help_description = f"""
Display the author of the program.
Usage Example:
Input:
    {func_name}
Output:
    {self.program_author}
"""
            self.function_help(func_name, help_description)
            self.current_tty_status = self.success
            return self.success
        self.print_on_tty(self.default_colour, "The program's author is: ")
        self.print_on_tty(self.success_colour, f"{self.program_author}\n")
        self.current_tty_status = self.success
        return self.success

    def client(self, args: list) -> int:
        """ Display the client of the program """
        func_name = "client"
        if self.help_function_child_name == func_name:
            help_description = f"""
Display the client of the program.
Usage Example:
Input:
    {func_name}
Output:
    This program was created for: {self.client_name}
"""
            self.function_help(func_name, help_description)
            self.current_tty_status = self.success
            return self.success
        self.print_on_tty(
            self.default_colour,
            "This program was created for: "
        )
        self.print_on_tty(self.success_colour, f"{self.client_name}\n")
        self.current_tty_status = self.success
        return self.success

    def env(self, args: list) -> int:
        """ Display the environement variables """
        func_name = "env"
        if self.help_function_child_name == func_name:
            help_description = f"""
Display the environement variables.
Usage Example:
Input:
    {func_name}
Output:
    The environement variables
"""
            self.function_help(func_name, help_description)
            self.current_tty_status = self.success
            return self.success
        for key, value in os.environ.items():
            self.print_on_tty(self.default_colour, f"{key}: {value}\n")
        self.current_tty_status = self.success
        return self.success

    def session_admin(self) -> None:
        """ Display the level of the program """
        self.print_on_tty(
            self.default_colour,
            "This program has admin privileges: "
        )
        self.print_on_tty(self.success_colour, f"{self.is_admin()}\n")
        self.current_tty_status = self.success

    def env_plus_plus(self, args: list) -> int:
        """ Display the environement variables """
        func_name = "env++"
        if self.help_function_child_name == func_name:
            help_description = f"""
Display the environement variables.
Usage Example:
Input:
    {func_name}
Output:
    The environement variables
    # terms in one colour and definitions in another
"""
            self.function_help(func_name, help_description)
            self.current_tty_status = self.success
            return self.success
        for key, value in os.environ.items():
            self.print_on_tty(self.env_term_colour, f"{key}")
            self.print_on_tty(self.env_shell_colour, ": ")
            self.print_on_tty(self.env_definition_colour, f"{value}")
            self.print_on_tty(self.default_colour, "\n")
        self.current_tty_status = self.success
        return self.success

    def setenv(self, args: list) -> int:
        """ Function in charge of setting a variable in the environement of the shell """
        func_name = "setenv"
        if self.help_function_child_name == func_name:
            help_description = f"""
Set an environement variable.
If no arguments are passed, the name and value of the variable will be asked
If one argument is passed, an empty variable is set
If two or more argument are passed, the first argument becomes the name of the variable, the rest is compiled into a string seperated by spaces and become the value of that variable
Usage Example:
Input:
    {func_name}
Output:
    Please enter the name of the variable: a
    Please enter the value of the variable: b
    Variable set

Input:
    {func_name} a
Output:
    Variable set

Input:
    {func_name} a b
Output:
    Variable set
"""
            self.function_help(func_name, help_description)
            self.current_tty_status = self.success
            return self.success
        self.print_on_tty(self.reset_colour, "Welcome to Setenv\n")
        arg_length = len(args)
        if arg_length == 1:
            os.environ[args[0]] = ""
        if arg_length >= 2:
            os.environ[args[0]] = self.list_to_str(
                args[1:],
                self.input_split_char
            )
        if arg_length == 0:
            var_name = self.ask_question.ask_question(
                "Please enter the name of the variable: ",
                "str"
            )
            var_value = input("Please enter the value of the variable: ")
            os.environ[var_name] = var_value
        self.print_on_tty(self.default_colour, "Variable set\n")
        self.current_tty_status = self.success
        return self.success

    def unset_single_variable(self, argument: str) -> int:
        """ Unset a single variable """
        if argument in os.environ:
            del os.environ[argument]
            return self.success
        return self.error

    def ask_for_env_to_unset(self) -> int:
        """ Ask for the variable that needs to be removed from the environement """
        var_name = self.ask_question.ask_question(
            "Please enter the name of the variable: ",
            "ascii"
        )
        if var_name in os.environ:
            if self.unset_single_variable(var_name) != self.success:
                self.print_on_tty(
                    self.error_colour,
                    f"Variable '{var_name}' does not exist\n"
                )
                self.current_tty_status = self.err
                return self.err
            self.print_on_tty(
                self.success_colour,
                "Variable unset\n"
            )
            self.current_tty_status = self.success
            return self.success
        self.print_on_tty(
            self.error_colour,
            f"Variable '{var_name}' does not exist\n"
        )
        self.current_tty_status = self.err
        return self.err

    def unsetenv(self, args: list) -> int:
        """ Function in charge of unsetting a variable in the environement of the shell """
        func_name = "unsetenv"
        if self.help_function_child_name == func_name:
            help_description = f"""
Unset an environement variable.
If no arguments are passed, the name of the variable will be asked
If one or more argument are passed, the variable with that name is unset
If '*' is passed, the environement will be flushed
Usage Example:
Input:
    {func_name}
Output:
    Please enter the name of the variable: a
    Variable unset
Input (a does not exist):
    {func_name} a
Output:
    Variable 'a' does not exist
Input:
    {func_name} a b
Output:
    Variables ['a','b'] unset
Input (a does not exist):
    {func_name} a b
Output:
    Variable 'a' does not exist
    Variables ['b'] unset
Input:
    {func_name} *
Output:
    Environement flushed
"""
            self.function_help(func_name, help_description)
            self.current_tty_status = self.success
            return self.success
        self.print_on_tty(self.reset_colour, "Welcome to Unsetenv\n")
        arg_length = len(args)
        if arg_length == 0:
            return self.ask_for_env_to_unset()
        if arg_length == 1:
            if args[0] == "*":
                os.environ.clear()
                self.print_on_tty(
                    self.default_colour,
                    "Environement flushed\n"
                )
                self.current_tty_status = self.success
                return self.success
            status = self.unset_single_variable(args[0])
            self.current_tty_status = status
            if status == self.success:
                self.print_on_tty(
                    self.default_colour,
                    "Variable unset\n"
                )
                return status
            self.print_on_tty(
                self.error_colour,
                f"Variable '{args[0]}' does not exist\n"
            )
            return status
        if arg_length > 1:
            unset_variables = []
            global_status = self.success
            for arg in args:
                status = self.unset_single_variable(arg)
                if status != self.success:
                    global_status = status
                    self.print_on_tty(
                        self.error_colour,
                        f"Variable '{arg}' does not exist\n"
                    )
                else:
                    unset_variables.append(arg)
            self.print_on_tty(
                self.success_colour,
                f"Variables {unset_variables} unset\n"
            )
            self.current_tty_status = global_status
            return global_status
        self.current_tty_status = self.success
        return self.success

    def display_status_code(self, args: list) -> None:
        """ Display the status code of the last function """
        func_name = "?"
        if self.help_function_child_name == func_name:
            help_description = f"""
Display the return code of the last function that was called.
Usage Example:
Input:
    {func_name}
Output (if return code is successefull):
    The status is: 0
    This status corresponds to a success
Output (if the return code is a failure):
    The status is: 84
    This status corresponds to and error
Output (if the return code is unknown [here: 1]):
    The status is: 1
    This status is not referenced by this terminal
"""
            self.function_help(func_name, help_description)
            self.current_tty_status = self.success
            return self.success
        self.print_on_tty(
            self.default_colour,
            f"The status is: {self.current_tty_status}\n"
        )
        if self.current_tty_status in (self.err, self.error):
            self.print_on_tty(
                self.default_colour,
                "This status corresponds to and error.\n"
            )
        elif self.current_tty_status == self.success:
            self.print_on_tty(
                self.default_colour,
                "This status corresponds to a success.\n"
            )
        else:
            self.print_on_tty(
                self.default_colour,
                "This status is not referenced by this terminal.\n"
            )
            if self.current_tty_status == 1:
                self.print_on_tty(
                    self.default_colour,
                    "This status generally means that an error has occurred during the execution of a program\n"
                )
        self.current_tty_status = self.success
        return self.success

    def function_help(self, function_name: str, description: str) -> None:
        """ The function in charge of displaying the help for a specific function """
        self.print_on_tty(self.help_title_colour, "Displaying help about: '")
        self.print_on_tty(self.help_command_colour, function_name)
        self.print_on_tty(self.help_title_colour, "'\n")
        self.print_on_tty(self.help_description_colour, description)

    def help_help(self) -> None:
        """ Display the help on the help function """
        func_name = "help"
        help_description = f"""
Display the help section.
If no arguments are passed, the available commands are displayed
If a command is passed in 'help' the help about that command is displayed
If 'help' is passed in 'help' this section is displayed
Usage Example:
Input:
    {func_name} hello_world
Output:
    The {func_name} section of the hello_world function

Input:
    {func_name} prompt
Output:
    The help section of the prompt function (the line asking for your command)
"""
        self.function_help(func_name, help_description)
        self.current_tty_status = self.success

    def help_prompt(self) -> None:
        """ Display the help on the prompt function """
        prompt_description = """
Displays the return code of the previous command.
Here are the different status colours:
"""
        self.function_help("prompt", prompt_description)
        self.print_on_tty(self.help_description_colour, "Success: ")
        self.current_tty_status = self.success
        self.display_status_in_prompt()
        self.print_on_tty(self.help_description_colour, "\nError: ")
        self.current_tty_status = self.error
        self.display_status_in_prompt()
        self.print_on_tty(
            self.help_description_colour,
            "\nUnreferenced status: "
        )
        self.current_tty_status = self.success + 1
        self.display_status_in_prompt()
        self.print_on_tty(
            self.help_description_colour,
            "\nYou can display the status code by entering: '?'\n"
        )
        self.current_tty_status = self.success

    def process_help_call(self, args: list) -> int:
        """ Process the inputs for the help calls """
        usr_input = args[0].lower()
        if usr_input in ("help", "man", ".help", ".h", "/?", "-h", "--h", "-help", "--help"):
            self.help_help()
            self.current_tty_status = self.success
            return self.success
        if usr_input == "prompt":
            self.help_prompt()
            self.current_tty_status = self.success
            return self.current_tty_status
        for item in self.options:
            if usr_input in item:
                self.help_function_child_name = usr_input
                item[usr_input](args)
                self.current_tty_status = self.success
                return self.current_tty_status
        self.print_on_tty(
            self.error_colour,
            f"Invalid option: {str(args[0])}\n"
        )
        self.current_tty_status = self.error
        return self.current_tty_status

    def help(self, args: list) -> int:
        """ The help function in charge of displaying the available options to the user """
        if len(args) > 0 and args[0] != '':
            return self.process_help_call(args)
        self.print_on_tty(self.reset_colour, "Available commands:\n")
        if self.options is None:
            self.print_on_tty(self.reset_colour, "No commands available")
            self.current_tty_status = self.success
            return self.current_tty_status
        for items in self.options:
            for option in items:
                self.print_on_tty(self.env_term_colour, option)
                self.print_on_tty(self.env_shell_colour, ": ")
                self.print_on_tty(
                    self.env_definition_colour,
                    items["desc"]
                )
                self.print_on_tty(self.env_definition_colour, "\n")
                break
        self.print_on_tty(self.default_colour, "\n")
        self.current_tty_status = self.success
        return self.current_tty_status

    def pwd(self, args: list) -> int:
        """ The function in charge of displaying the current working directory """
        func_name = "pwd"
        if self.help_function_child_name == func_name:
            help_description = f"""
Display the current working directory.
Usage Example:
Input:
    {func_name}
Output:
    The current working directory
"""
            self.function_help(func_name, help_description)
            self.current_tty_status = self.success
            return self.success
        self.print_on_tty(self.default_colour, f"{os.getcwd()}\n")
        self.current_tty_status = self.success
        return self.success

    def sanitize_directory_path(self, dir_name: str) -> str:
        """ Replace characters that could break the creation by """
        dir_name = dir_name.replace("\\", "/")
        illegal_character = [
            "\t", "\n", "\r", "\v", "\f", "\b", "\a", "\0", "\'", "\"",
            "?", "*", "<", ">", "|", ":", ";", "!", "@", "#", "$", "%", "^",
            "&", "(", ")", "[", "]", "{", "}", "`", "~", "=", "+"
        ]
        for i in illegal_character:
            if i in dir_name:
                dir_name = dir_name.replace(i, " ")
        return dir_name

    def create_directories(self, path: str, show_if_created: bool = True) -> int:
        """ Create the required directories """
        path = self.sanitize_directory_path(path)
        if os.path.isfile(path):
            self.print_on_tty(
                self.error_colour,
                f"Directory '{path}' is a file\n"
            )
            self.current_tty_status = self.error
            return self.error
        if os.path.isdir(path):
            self.print_on_tty(
                self.error_colour,
                f"Directory '{path}' already exists\n"
            )
            self.current_tty_status = self.error
            return self.error
        try:
            os.makedirs(path, exist_ok=True)
        except OSError as err:
            self.print_on_tty(
                self.error_colour,
                f"Directory '{path}' could not be created\n{err}"
            )
            self.current_tty_status = self.error
            return self.error
        if show_if_created:
            self.print_on_tty(
                self.success_colour,
                f"Directory '{path}' created\n"
            )
        self.current_tty_status = self.success
        return self.success

    def make_directory(self, args: list) -> int:
        """ Create a directory """
        func_name = "mkdir"
        if self.help_function_child_name == func_name:
            help_description = f"""
Create a directory.
If no arguments are passed, the name of the directory will be asked
If one or more argument are passed, the directory with that name is created
Usage Example:
Input:
    {func_name}
Output:
    Please enter the name of the directory: a
    Directory created
Input:
    {func_name} a
Output:
    Directory created
Input:
    {func_name} a b
Output:
    Directories ['a','b'] created
Input:
    {func_name} a/b
Output:
    Directory created
Input:
    {func_name} a/b c/d
Output:
    Directories ['a/b','c/d'] created
Input (a already exists):
    {func_name} a
Output:
    Directory 'a' already exists
Input:
    {func_name} a/b c/d
Output:
    Directory 'a/b' already exists
"""
            self.function_help(func_name, help_description)
            self.current_tty_status = self.success
            return self.success
        self.print_on_tty(self.reset_colour, "Welcome to 'mkdir'\n")
        arg_length = len(args)
        if arg_length == 0:
            dir_name = self.ask_question.ask_question(
                "Please enter the name of the directory: ",
                "ascii"
            )
            self.create_directories(dir_name, True)
        if arg_length >= 1:
            global_status = self.success
            created_directories = []
            for arg in args:
                status = self.create_directories(arg, False)
                if status != self.success:
                    global_status = status
                else:
                    created_directories.append(arg)
            self.print_on_tty(
                self.success_colour,
                f"Directories {created_directories} created\n"
            )
            self.current_tty_status = global_status
            return global_status
        self.current_tty_status = self.success
        return self.success

    def check_file_path(self, file_path: str) -> int:
        """ Check the path leading to the file to make sure the path exists """
        if os.path.exists(file_path):
            return self.success
        return self.error

    def create_a_file(self, filename: str) -> int:
        """ Create a file based on the name """
        filename = filename.replace("\"", " ")
        filename = filename.replace("\\", "/")
        filename_display = filename.split("/")
        file_path = filename_display[:-1]
        file_path = self.list_to_str(file_path, "/")
        filename_display = filename_display[-1]
        if "/" in filename and self.check_file_path(file_path) != self.success:
            self.print_on_tty(
                self.error_colour,
                f"Path '{file_path}' does not exist, file '{filename_display}' creation failed."
            )
            self.current_tty_status = self.error
            return self.current_tty_status
        if os.path.isdir(filename):
            self.print_on_tty(
                self.error_colour,
                f"File '{filename}' is a directory\n"
            )
            self.current_tty_status = self.error
            return self.error
        if os.path.isfile(filename):
            self.print_on_tty(
                self.error_colour,
                f"File '{filename}' already exists\n"
            )
            self.current_tty_status = self.error
            return self.error
        try:
            with open(filename, "w", encoding="utf-8", newline="\n") as file:
                file.write("")
                file.close()
        except IOError as err:
            self.print_on_tty(
                self.error_colour,
                f"File '{filename}' could not be created\n{err}"
            )
            self.current_tty_status = self.error
            return self.error
        self.current_tty_status = self.success
        return self.success

    def touch(self, arg: list) -> int:
        """ Create a file in the present path """
        func_name = "touch"
        if self.help_function_child_name == func_name:
            help_description = f"""
Create a file.
If no arguments are passed, the name of the file will be asked
If one or more argument are passed, the file with that name is created
Usage Example:
Input:
    {func_name}
Output:
    Please enter the name of the file: a
    File created
Input:
    {func_name} a
Output:
    File created
Input:
    {func_name} a b
Output:
    Files ['a','b'] created
Input:
    {func_name} a/b
Output:
    File created
Input:
    {func_name} a/b c/d
Output:
    Files ['a/b','c/d'] created
Input (a already exists):
    {func_name} a
Output:
    File 'a' already exists
Input (b already exists):
    {func_name} a/b c/d
Output:
    File 'a/b' already exists
Input (the path to b does not exist):
    {func_name} not/a/path/b c/d
Output:
    Path 'not/a/path/' does not exist, file 'b' creation failed.
    Files ['c/d'] created
"""
            self.function_help(func_name, help_description)
            self.current_tty_status = self.success
            return self.success
        self.print_on_tty(self.default_colour, "Welcome to Touch\n")
        arg_length = len(arg)
        if arg_length == 0:
            file_name = self.ask_question.ask_question(
                "Please enter the name of the file: ",
                "ascii"
            )
            return self.create_a_file(file_name)
        if arg_length >= 1:
            global_status = self.success
            created_files = []
            for file in arg:
                status = self.create_a_file(file)
                if status != self.success:
                    global_status = status
                else:
                    created_files.append(file)
            self.print_on_tty(
                self.success_colour,
                f"Files {created_files} created\n"
            )
            self.current_tty_status = global_status
            return global_status
        self.current_tty_status = self.success
        return self.success

    def remove_a_directory(self, directory_path: str) -> int:
        """ Remove a directory (child function)"""
        directory_path = directory_path.replace("\\", "/")
        if os.path.isdir(directory_path):
            shutil.rmtree(directory_path)
            return self.success
        return self.error

    def remove_directory(self, args: list) -> int:
        """ Remove a directory """
        func_name = "rmdir"
        if self.help_function_child_name == func_name:
            help_description = f"""
Remove a directory.
If no arguments are passed, the name of the directory will be asked
If one or more argument are passed, the directory with that name is removed
Usage Example:
Input:
    {func_name}
Output:
    Please enter the name of the directory: a
    Directory removed
Input:
    {func_name} a
Output:
    Directory removed
Input:
    {func_name} a b
Output:
    Directories ['a','b'] removed
Input:
    {func_name} a/b
Output:
    Directory removed
Input:
    {func_name} a/b c/d
Output:
    Directories ['a/b','c/d'] removed
Input (a does not exist):
    {func_name} a
Output:
    Directory 'a' does not exist
Input (b does not exist):
    {func_name} a/b c/d
Output:
    Directory 'a/b' does not exist
    Directories ['c/d'] removed
"""
            self.function_help(func_name, help_description)
            self.current_tty_status = self.success
            return self.success
        self.print_on_tty(self.default_colour, "Welcome to 'rmdir'\n")
        arg_length = len(args)
        if arg_length == 0:
            dir_name = self.ask_question.ask_question(
                "Please enter the name of the directory: ",
                "ascii"
            )
            return self.remove_directory([dir_name])
        if arg_length >= 1:
            global_status = self.success
            removed_directories = []
            for directory in args:
                status = self.remove_a_directory(directory)
                if status != self.success:
                    global_status = status
                else:
                    removed_directories.append(directory)
            self.print_on_tty(
                self.success_colour,
                f"Directories {removed_directories} removed\n"
            )
            self.current_tty_status = global_status
            return global_status
        self.current_tty_status = self.success
        return self.success

    def remove_an_item(self, path: str) -> int:
        """ Remove an item """
        try:
            if os.path.isfile(path):
                os.remove(path)
            else:
                response = self.ask_question.ask_question(
                    f"Are you sure you wish to remove folder {path} and all it's content? [(Y)es/(N)o]",
                    "bool"
                )
                if response:
                    shutil.rmtree(path)
                else:
                    self.print_on_tty(self.error_colour, "Folder skipped\n")
                    self.current_tty_status = self.success
                    return self.current_tty_status
            return self.success
        except IOError as err:
            self.print_on_tty(
                self.error_colour,
                f"File or directory '{path}' does not exist\n{err}\n"
            )
            self.current_tty_status = self.err
            return self.error

    def remove_file(self, args: list) -> int:
        """ Remove a file or a directory """
        func_name = "rm"
        if self.help_function_child_name == func_name:
            help_description = f"""
Remove a file or a directory.
If no arguments are passed, the name of the file or directory will be asked
If one or more argument are passed, the file or directory with that name is removed
Usage Example:
Input:
    {func_name}
Output:
    Please enter the name of the file or directory: a
    File or directory removed
Input:
    {func_name} a
Output:
    File or directory removed
Input:
    {func_name} a b
Output:
    Files or directories ['a','b'] removed
Input:
    {func_name} a/b
Output:
    File or directory removed
Input:
    {func_name} a/b c/d
Output:
    Files or directories ['a/b','c/d'] removed
Input (a does not exist):
    {func_name} a
Output:
    File or directory 'a' does not exist
Input (b does not exist):
    {func_name} a/b c/d
Output:
    File or directory 'a/b' does not exist
    Files or directories ['c/d'] removed
"""
            self.function_help(func_name, help_description)
            self.current_tty_status = self.success
            return self.success
        self.print_on_tty(self.default_colour, "Welcome to 'rm'\n")
        arg_length = len(args)
        if arg_length == 0:
            file_name = self.ask_question.ask_question(
                "Please enter the name of the file or directory: ",
                "ascii"
            )
            return self.remove_an_item([file_name])
        if arg_length >= 1:
            global_status = self.success
            removed_files = []
            for file in args:
                status = self.remove_an_item(file)
                if status != self.success:
                    global_status = status
                else:
                    removed_files.append(file)
            self.print_on_tty(
                self.success_colour,
                f"Files or directories {removed_files} removed\n"
            )
            self.current_tty_status = global_status
            return global_status
        self.current_tty_status = self.success
        return self.current_tty_status

    def cd_access_directory(self, path: str) -> int:
        """ Access a directory based on the provided path """
        try:
            self.old_pwd = os.getcwd()
            os.chdir(path)
            self.current_tty_status = self.success
            return self.success
        except IOError:
            self.print_on_tty(self.error_colour, f"Invalid path: {str(path)}")
            self.current_tty_status = self.error
            return self.error

    def cd_go_further_than_home(self, path: str) -> int:
        """ The function in charge of changing the current working directory to a directory further than the home directory """
        tmp = os.getcwd()
        if path[0] == "~":
            self.cd_access_directory(self.home)
            path = path[1:]
        if path != "" and path[0] in ("/", "\\"):
            path = path[1:]
            self.cd_access_directory(path)
        self.old_pwd = tmp
        self.current_tty_status = self.success
        return self.success

    def cd_rollback(self, path: str) -> int:
        """ The function in charge of rolling back the current working directory to the previous one """
        tmp = os.getcwd()
        os.chdir(self.old_pwd)
        self.print_on_tty(self.success_colour, f"{self.old_pwd}\n")
        self.old_pwd = tmp
        if len(path) > 2:
            self.change_directory(path[2:])
        self.current_tty_status = self.success
        return self.success

    def change_directory(self, args: list) -> int:
        """ The function in charge of changing the current working directory """
        func_name = "cd"
        if self.help_function_child_name == func_name:
            help_description = f"""
Change the current working directory.
If no arguments are passed, the current working directory is changed to the home directory
If one argument is passed, the current working directory is changed to the passed in argument
Usage Example:
Input:
    {func_name}
Output:
    # The current working directory is changed to the home directory
Input:
    {func_name} /home
Output:
    # The current working directory is changed to /home
Error handling:
Input:
    {func_name} /home/does_not_exist
Output:
    Invalid path
Input:
    {func_name} /a/path /another/path
Output:
    Invalid number of arguments
"""
            self.function_help(func_name, help_description)
            self.current_tty_status = self.success
            return self.success
        if len(args) == 0:
            return self.cd_access_directory(self.home)
        if len(args) == 1:
            if args[0][0] == "-":
                return self.cd_rollback(args[0])
            if args[0][0] == "~":
                return self.cd_go_further_than_home(args[0])
            self.cd_access_directory(args[0])
            self.current_tty_status = self.success
            return self.success
        self.print_on_tty(self.error_colour, "Invalid number of arguments")
        self.current_tty_status = self.error
        return self.error

    def exit(self, args: list) -> int:
        """ The function in charge of exiting the layer in which the user is located """
        func_name = "exit"
        if self.help_function_child_name == func_name:
            help_description = f"""
Close this menu and return to the parent session
Usage Example:
Input:
    {func_name}
Output:
    The prompt from the parent
"""
            self.function_help(func_name, help_description)
            self.current_tty_status = self.success
            return self.success
        if self.session_name != self.master_session:
            self.print_on_tty(self.default_colour, "Leaving child session\n")
        else:
            self.print_on_tty(self.default_colour, "Leaving program\n")
        self.continue_tty_loop = False
        return self.current_tty_status

    def kill(self, args: list) -> int:
        """ The function in charge of abruptly stopping the program (not recommended) """
        func_name = "abort"
        if self.help_function_child_name == func_name:
            help_description = f"""
Exit the program instantly and abruptly.
This will close all child processes and will not free the allocated ressources.
Usage Example:
Input:
    {func_name}
Output:
    Whatever was used to launch this program.
"""
            self.function_help(func_name, help_description)
            self.current_tty_status = self.success
            return self.success
        self.print_on_tty(self.default_colour, "")
        sys.exit(self.current_tty_status)

    def display_status_in_prompt(self) -> None:
        """ Display the return code of the previous function """
        if self.current_tty_status == self.success:
            self.print_on_tty(self.success_colour, "~")
        elif self.current_tty_status == self.error or self.current_tty_status == self.err:
            self.print_on_tty(self.error_colour, "~")
        else:
            self.print_on_tty(self.error_colour, "~")
        self.print_on_tty(self.default_colour, " ")

    def create_key_prompt_bindings(self) -> None:
        """ Set up the functions in charge of changing the prompt with the content of the history command """
        bindings = KeyBindings()

        @bindings.add('up')
        def _(event):
            if self.history_index > 0:
                self.history_index -= 1
                self.user_session.default_buffer.text = self.history[self.history_index]

        @bindings.add('down')
        def _(event):
            if self.history_index < len(self.history):
                self.history_index += 1
                if self.history_index == len(self.history):
                    self.user_session.default_buffer.reset()
                else:
                    self.user_session.default_buffer.text = self.history[self.history_index]

        self.user_session = prompt_toolkit.PromptSession(
            complete_while_typing=True,
            validate_while_typing=True,
            enable_history_search=True,
            key_bindings=bindings,
            history=self.history
        )

    def process_key_inputs(self) -> str:
        """ act depending on the special keys pressed or if entered is pressed """
        try:
            self.user_input = self.user_session.prompt()
        except KeyboardInterrupt:
            self.user_input = ""
        return self.user_input

    def display_prompt(self) -> None:
        """ The function in charge of displaying a basic prompt to ask the user to enter an option """
        self.display_status_in_prompt()
        self.print_on_tty(self.prompt_colour, "(")
        self.print_on_tty(self.session_name_colour, f"{self.session_name}")
        self.print_on_tty(self.prompt_colour, f") {os.getcwd()}>")
        self.user_input = self.process_key_inputs()

    def get_current_folder(self) -> str:
        """ Return the current folder """
        path = os.getcwd()
        path = path.replace("\\", "/")

    def bind_ls(self, args: list) -> int:
        """ Bind the ls function to the ls command """
        func_name = "ls"
        if self.help_function_child_name in (func_name, "dir"):
            help_description = f"""
Display the content of the current working directory.
Usage Example:
Input:
    {self.help_function_child_name}
Output:
    The content of the current working directory
"""
            self.function_help(self.help_function_child_name, help_description)
            self.current_tty_status = self.success
            return self.success
        if len(args) >= 1:
            status = self.ls.ls(args[0])
            self.current_tty_status = status
            return status
        status = self.ls.ls(".")
        self.current_tty_status = status
        return status

    def hello_world(self, args: list) -> int:
        """ This is a function in charge of displaying a Hello World and the passed arguments """
        func_name = "hello_world"
        if self.help_function_child_name == func_name:
            help_description = f"""
Display a 'Hello World !'.
If no arguments are passed, a 'Hello World !' is displayed
If a command is passed, 'Hello World !' is displayed as well as the passed in arguments
Usage Example:
Input:
    {func_name} hi
Output:
    Hello World !
    0: 'hi'
"""
            self.function_help(func_name, help_description)
            self.current_tty_status = self.success
            return self.success
        self.print_on_tty(self.default_colour, "Hello World !\n")
        for index, arg in enumerate(args):
            self.print_on_tty(self.default_colour, f"{index}: '{arg}'\n")
        self.current_tty_status = self.success
        return self.success

    def run_command(self, args: list) -> int:
        """ Run a command in the host's shell environement """
        help_command = "run"
        if self.help_function_child_name == help_command:
            help_description = f"""
This is a command that allows you to run a command on the parent shell.
Input:
    {help_command} <your command>
Output:
    The result of the command you ran.
Example:
Input:
    {help_command} echo "Hello World!"
Output:
    Hello World!
"""
            self.function_help(help_command, help_description)
            self.current_tty_status = self.success
            return self.success
        if len(args) < 1:
            self.print_on_tty(
                self.error_colour,
                "You need to specify a command to run\n"
            )
            self.current_tty_status = self.error
            return self.error
        command = " ".join(args)
        self.print_on_tty(
            self.default_colour,
            f"Running command: {command}\n"
        )
        status = self.run_external_command(command)
        if status != self.success:
            self.print_on_tty(
                self.error_colour,
                "Error while running command\n"
            )
            self.current_tty_status = status
            return status
        self.current_tty_status = self.success
        return self.success

    def check_if_admin_for_windows(self) -> bool:
        """ Check if the current windows user has admin rights """
        command = """
:: Check if the script is running with administrative privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    exit 2
) else (
    exit 3
)
"""
        status = os.system(command)
        if status == 2:
            return True
        return False

    def is_admin(self) -> bool:
        """ Check if the user has admin rights """
        try:
            # On Windows, check if the user has administrator privileges
            if os.name == 'nt':
                return self.check_if_admin_for_windows()
            # On Unix-like systems, check if the user is the root user
            else:
                return os.geteuid() == 0
        except AttributeError:
            return False

    def run_as_windows_admin(self, file: str) -> int:
        """ Run a powershell script as an administrator """
        return self.run_command(
            [
                "powershell.exe",
                "-ExecutionPolicy Bypass",
                "-Command \"",
                "Start-Process",
                "cmd",
                "-Verb RunAs",
                "-ArgumentList '",
                f"/c {file}'\""
            ]
        )

    def check_admin(self, args: list) -> int:
        """ Check if the program has admin rights """
        func_name = "check_admin"
        if self.help_function_child_name == func_name:
            help_description = f"""
Check if the program has admin rights.
Usage Example:
Input:
    {func_name}
Output:
    {self.is_admin()}
"""
            self.function_help(func_name, help_description)
            self.current_tty_status = self.success
            return self.success
        self.print_on_tty(
            self.default_colour,
            f"{self.is_admin()}\n"
        )
        self.current_tty_status = self.success
        return self.success

    def save_to_file(self, data: str, filepath: str) -> int:
        """ Save data to a file """
        self.print_on_tty(
            self.info_colour,
            f"Saving {data} to file '{filepath}'\n"
        )
        try:
            with open(filepath, "w", encoding="utf-8", newline="\n") as file:
                file.write(data)
                file.close()
            self.print_on_tty(
                self.success_colour,
                f"{data} saved to file '{filepath}'\n"
            )
        except IOError as err:
            self.print_on_tty(
                self.error_colour,
                f"File '{filepath}' could not be created\n{err}"
            )
            self.current_tty_status = self.error
            return self.error
        self.current_tty_status = self.success
        return self.success

    def run_as_admin(self, args: list) -> int:
        """ Run a command as an administrator """
        func_name = "run_as_admin"
        if self.help_function_child_name == func_name:
            help_description = f"""
Run a command as an administrator.
Usage Example:
Input:
    {func_name} <your command>
Output:
    The result of the command you ran.
Example:
Input:
    {func_name} echo "Hello World!"
Output:
    Hello World!
"""
            self.function_help(func_name, help_description)
            self.current_tty_status = self.success
            return self.success
        if len(args) < 1:
            self.print_on_tty(
                self.error_colour,
                "You need to specify a command to run\n"
            )
            self.current_tty_status = self.error
            return self.error
        command = " ".join(args)
        if os.name == "nt":
            commands = f"{os.getcwd()}\\your_code.bat"
            self.save_to_file(command, commands)
            status = self.run_as_windows_admin(command)
            self.remove_an_item(commands)
            if status != self.success:
                self.print_on_tty(
                    self.error_colour,
                    "Error while running command\n"
                )
                self.current_tty_status = status
                return status
            self.current_tty_status = self.success
            return self.success
        args.insert(0, "sudo")
        return self.run_command(args)

    def process_input(self) -> None:
        """ The function in charge of processing the user input """
        if self.user_input == "":
            self.current_tty_status = self.success
            return
        self.history.append(self.user_input)
        cleaned_command = self.user_input.split(self.comment_token)[0]
        command = cleaned_command.split(self.input_split_char)
        args = command[1:]
        command = command[0].lower()
        was_found = False
        for item in self.options:
            if command in item:
                item[command](args)
                was_found = True
        if was_found is False:
            self.print_on_tty(
                self.error_colour,
                f"Invalid option: {str(command)}\n"
            )
            self.current_tty_status = self.err

    def assing_colours(self) -> None:
        """ assing the colours to the variables in charge of managing the displays"""
        colours = {
            "default": "0A",
            "prompt": "0B",
            "error": "0C",
            "success": "01",
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
        for i in self.tty_colours:
            if i not in colours:
                self.tty_colours[i] = colours[i]
        self.reset_colour = self.tty_colours["reset"]
        self.prompt_colour = self.tty_colours["prompt"]
        self.default_colour = self.tty_colours["default"]
        self.error_colour = self.tty_colours["error"]
        self.success_colour = self.tty_colours["success"]
        self.info_colour = self.tty_colours["info"]
        self.help_title_colour = self.tty_colours["help_title_colour"]
        self.help_command_colour = self.tty_colours["help_command_colour"]
        self.help_description_colour = self.tty_colours["help_description_colour"]
        self.env_term_colour = self.tty_colours["env_term_colour"]
        self.env_shell_colour = self.tty_colours["env_shell_colour"]
        self.env_definition_colour = self.tty_colours["env_definition_colour"]
        self.session_name_colour = self.tty_colours["session_name_colour"]

    def command_seperator(self, args: list) -> int:
        """ Display/Change the token in charge of indicating the beginning of a new command when many are put together """
        func_name = "command_seperator"
        if self.help_function_child_name == func_name:
            help_description = f"""
Display the token in charge of indicating the beginning of a new command when many are put together.
Usage Example:
Input:
    {func_name}
Output:
    {self.command_seperator_token}

Input:
    {func_name} -
Output:
    The command seperator has be changed from '{self.command_seperator_token}' to '-'.
Input:
    {func_name} - c
Output:
    The command seperator has be changed from '{self.command_seperator_token}' to '-c'.

"""
            self.function_help(func_name, help_description)
            self.current_tty_status = self.success
            return self.success
        if len(args) == 0:
            self.print_on_tty(
                self.default_colour,
                "The command seperator is: "
            )
            self.print_on_tty(
                self.success_colour,
                f"{self.command_seperator_token}\n"
            )
            self.current_tty_status = self.success
            return self.success
        prev_seperator = self.command_seperator_token
        self.command_seperator_token = "".join(args)
        if self.command_seperator_token == self.comment_token:
            self.print_on_tty(
                self.error_colour,
                "Error: The seperator cannot be the same as the comment token"
            )
            self.command_seperator_token = prev_seperator
            self.current_tty_status = self.error
            return self.error
        if len(self.command_seperator_token) == 0 or self.command_seperator_token.isspace() is True:
            self.print_on_tty(
                self.error_colour,
                "Error: The seperator cannot be empty or contain only blanks/tabs"
            )
            self.command_seperator_token = prev_seperator
            self.current_tty_status = self.error
            return self.error
        self.print_on_tty(
            self.success_colour,
            f"The command seperator has be changed from '{prev_seperator}' to '{self.command_seperator_token}'.\n"
        )
        self.current_tty_status = self.success
        return self.success

    def update_comment_token(self, args: list) -> int:
        """ Display/Change the token in charge of indicating the beginning of a new comment """
        func_name = "comment_token"
        if self.help_function_child_name == func_name:
            help_description = f"""
Display the token in charge of indicating the beginning of a comment.
Usage Example:
Input:
    {func_name}
Output:
    {self.comment_token}

Input:
    {func_name} -
Output:
    The comment token has be changed from '{self.comment_token}' to '-'.
Input:
    {func_name} - c
Output:
    The comment token has be changed from '{self.comment_token}' to '-c'.

"""
            self.function_help(func_name, help_description)
            self.current_tty_status = self.success
            return self.success
        if len(args) == 0:
            self.print_on_tty(
                self.default_colour,
                "The comment token is: "
            )
            self.print_on_tty(
                self.success_colour,
                f"{self.comment_token}\n"
            )
            self.current_tty_status = self.success
            return self.success
        prev_token = self.comment_token
        self.comment_token = "".join(args)
        if len(self.comment_token) == 0 or self.comment_token.isspace() is True:
            self.print_on_tty(
                self.error_colour,
                "Error: The seperator cannot be empty or contain only blanks/tabs"
            )
            self.command_seperator_token = prev_token
            self.current_tty_status = self.error
            return self.error
        self.print_on_tty(
            self.success_colour,
            f"The comment token has be changed from '{prev_token}' to '{self.comment_token}'.\n"
        )
        self.current_tty_status = self.success
        return self.success

    def title(self) -> None:
        """ The boot tile """
        if self.continue_tty_loop is False:
            return
        self.print_on_tty(
            self.default_colour,
            "Welcome to the DevOps deployer\n"
        )
        self.version([])
        self.session_admin()
        self.command_seperator([])
        self.update_comment_token([])
        self.process_session_name([])
        self.client([])
        self.author([])
        self.print_on_tty(self.default_colour, "\n")
        self.current_tty_status = self.success

    def get_the_home_path(self) -> None:
        """ Get the path of the HOME variable based on the system """
        if "HOME" in os.environ:
            self.home = os.environ["HOME"]
        elif "HOMEDRIVE" in os.environ and "HOMEPATH" in os.environ:
            self.home = f"{os.environ['HOMEDRIVE']}{os.environ['HOMEPATH']}"
        elif "HOMEPATH" in os.environ:
            self.home = os.environ["HOMEPATH"]
        elif "HOMEDRIVE" in os.environ:
            self.home = os.environ["HOMEDRIVE"]
        else:
            self.home = os.getcwd()

    def commands_to_auto_complete(self) -> None:
        """ Convert the available commands to a list so that it can be used for command auto-completion """
        for i in self.options:
            for b in i:
                self.auto_complete_list.append(b)

    def load_basics(self) -> None:
        """ set the values for the variables that can be configured by the user """
        self.old_pwd = os.getcwd()
        self.get_the_home_path()
        self.assing_colours()
        self.colour_lib.init_pallet()
        self.options = [
            {"help": self.help, "desc": "Display this help section"},
            {"man": self.help, "desc": "Display this help section"},
            {".help": self.help, "desc": "Display this help section"},
            {".h": self.help, "desc": "Display this help section"},
            {"/?": self.help, "desc": "Display this help section"},
            {"-h": self.help, "desc": "Display this help section"},
            {"--h": self.help, "desc": "Display this help section"},
            {"-help": self.help, "desc": "Display this help section"},
            {"--help": self.help, "desc": "Display this help section"},
            {"setenv": self.setenv, "desc": "Set a variable in the environement"},
            {
                "unsetenv": self.unsetenv,
                "desc": "Remove a variable from the environement"
            },
            {"exit": self.exit, "desc": "Close the current menu"},
            {
                "abort": self.kill,
                "desc": "Exit the program (This will kill the program and any child processes)"
            },
            {"hello_world": self.hello_world, "desc": "Display a Hello World"},
            {"env": self.env, "desc": "Display the environement variables"},
            {
                "env++": self.env_plus_plus,
                "desc": "Display the environement variables using different colours"
            },
            {
                "?": self.display_status_code,
                "desc": "Display the status code of the last function called"
            },
            {"cd": self.change_directory,
                "desc": "Change the current working directory"},
            {"pwd": self.pwd, "desc": "Display the path to the directory in wich we are located"},
            {
                "version": self.version,
                "desc": "Display the current version of the program"
            },
            {"author": self.author, "desc": "Display the author of the program"},
            {
                "session_name": self.process_session_name,
                "desc": "Change the name of the current session"
            },
            {"client": self.client, "desc": "Display the client of the program"},
            {
                "history": self.show_history,
                "desc": "Display the previous commands that were run"
            },
            {"ls": self.bind_ls, "desc": "List all files in the current folder"},
            {"dir": self.bind_ls, "desc": "List all files in the current folder"},
            {
                "mkdir": self.make_directory,
                "desc": "Create a directory in the present path"
            },
            {"touch": self.touch, "desc": "Create a file in the present path"},
            {
                "rm": self.remove_file,
                "desc": "Remove a file or directory if present in the path"
            },
            {
                "rmdir": self.remove_directory,
                "desc": "Remove a directory if present in the path"
            },
            {"run": self.run_command, "desc": "Run a command in the system terminal"},
            {
                "is_admin": self.check_admin,
                "desc": "Return True if the system has elevated privileges."
            },
            {
                "super_run": self.run_as_admin,
                "desc": "Run a command using elevated privileges"
            },
            {
                "command_seperator": self.command_seperator,
                "desc": "Display/Change the token in charge of indicating the begining of a new command when many are put together"
            },
            {
                "comment_token": self.update_comment_token,
                "desc": "Display/Change the token in charge of indicating the begining of a new command when many are put together"
            }
        ]
        self.commands_to_auto_complete()

    def unload_basics(self) -> int:
        """ Free the ressources that were previously allocated """
        self.old_pwd = ""
        self.home = ""
        self.reset_colour = None
        self.prompt_colour = None
        self.default_colour = None
        self.error_colour = None
        self.success_colour = None
        self.info_colour = None
        self.help_title_colour = None
        self.help_command_colour = None
        self.help_description_colour = None
        self.env_term_colour = None
        self.env_shell_colour = None
        self.env_definition_colour = None
        self.session_name_colour = None
        self.tty_colours = None
        self.options = []
        self.auto_complete_list = []
        return self.colour_lib.unload_ressources()

    def import_functions_into_shell(self, functions: list[dict[str, any]]) -> int:
        """ Import functions into the shell """
        for function in functions:
            if function is None or isinstance(function, dict) != True:
                continue
            if "desc" not in function:
                function["desc"] = "No description provided\n"
            self.options.append(function)
            item = list(function)[0]
            self.auto_complete_list.append(item)
            self.print_on_tty(
                self.success_colour,
                f"Added function {item}\n"
            )
        self.current_tty_status = self.success
        return self.success

    def remove_function_from_options(self, function: dict[str, any]) -> int:
        """ Remove a function from the options """
        for function_item in self.options:
            for index, item in enumerate(function_item):
                if item == function:
                    self.options.pop(index)
                    self.auto_complete_list.pop(index)
                    self.print_on_tty(self.success, f"Removed function {item}")
                    self.current_tty_status = self.success
                    return self.current_tty_status
        self.print_on_tty(
            self.error_colour,
            f"Failed to remove function {item}"
        )
        self.current_tty_status = self.error
        return self.current_tty_status

    def remove_functions_from_shell(self, functions: list[dict[str, any]]) -> int:
        """ Remove functions from the shell """
        global_status = self.success
        for function in functions:
            for item in function:
                status = self.remove_function_from_options(item)
                if status != self.success:
                    global_status = status
        self.current_tty_status = global_status
        return self.current_tty_status

    def goodbye_message(self) -> None:
        """ Display a goodbye message on the exit of the main terminal """
        goodbye_message = "Goodbye, see you next time !\n"
        if self.current_tty_status == self.success:
            self.print_on_tty(self.success_colour, goodbye_message)
        elif self.current_tty_status in (self.err, self.error):
            self.print_on_tty(self.error_colour, goodbye_message)
        else:
            self.print_on_tty(self.error_colour, goodbye_message)

    def run_complex_input(self, complex_input: list[str]) -> None:
        """ Run a complex input """
        for item in complex_input:
            self.user_input = item
            self.process_input()

    def process_complex_input(self, usr_input: list) -> None:
        """ process multiple command input if provided """
        command_list = []
        buffer = ""
        prev = ""
        for item in usr_input:
            if self.command_seperator_token == item:
                command_list.append(buffer)
                prev = item
                buffer = ""
                continue
            if prev in (self.command_seperator_token, ""):
                buffer += f"{item}"
                prev = item
                continue
            if buffer != " ":
                buffer += f" {item}"
                prev = item
        if buffer != "":
            command_list.append(buffer)
        self.run_complex_input(command_list)

    def process_if_arg_input(self) -> None:
        """ Check if the argv contains arguments input """
        if len(sys.argv) > 1:
            if self.command_seperator_token in sys.argv:
                self.process_complex_input(sys.argv[1:])
            else:
                self.user_input = " ".join(sys.argv[1:])
                self.process_input()
            if self.continue_tty_loop is True:
                self.print_on_tty(
                    self.default_colour,
                    "\n\n\n\n"
                )

    def clean_string(self, input_string: str) -> str:
        """ remove enclosing string from the run string """
        if len(input_string) > 0:
            if input_string[0] == '"':
                input_string = input_string[1:]
            if input_string[-1] == '"':
                input_string = input_string[:-1]
            if input_string[-2] == '"':
                input_string = input_string[:-2]+input_string[-1:]
            if input_string[-3] == '"':
                input_string = input_string[:-3]+input_string[-2:]
        return input_string

    def process_if_pipe_input(self) -> None:
        """ Check if the user input is a pipe input """
        if not sys.stdin.isatty():
            user_input = sys.stdin.read()
            user_input = self.clean_string(user_input)
            user_args = user_input.split(self.input_split_char)
            self.process_complex_input(user_args)
            if self.continue_tty_loop is True:
                self.exit([])

    def mainloop(self, session_name="main") -> int:
        """ The mainloop allowing the terminal to run like any other terminals """
        self.session_name = session_name
        self.process_if_arg_input()
        self.process_if_pipe_input()
        self.title()
        while self.continue_tty_loop is True:
            self.help_function_child_name = "help"
            self.display_prompt()
            seperated_commands = self.user_input.split(self.input_split_char)
            self.process_complex_input(seperated_commands)
        if self.session_name == "main":
            self.goodbye_message()
        self.print_on_tty(self.reset_colour, "")
        return self.current_tty_status


if __name__ == "__main__":
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
    TTYI.mainloop("Test session")
    TTYI.unload_basics()
