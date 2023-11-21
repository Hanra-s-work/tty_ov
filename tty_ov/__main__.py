from .tty_ov import TTY, ColouriseOutput, AskQuestion

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
