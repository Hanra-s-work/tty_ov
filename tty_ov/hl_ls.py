"""
File containing the ls class
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
