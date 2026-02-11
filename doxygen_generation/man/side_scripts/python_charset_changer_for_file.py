#!/bin/env python3
import sys  # Import the sys package in order to get the standard input

error = 1  # The status when the program fails
success = 0  # The status when the program succeeds

argc = len(sys.argv)
# Check if the argument count is not equal to 2 or (if the argument count is equal to 2 check that the content corresponds to a help call)
if argc != 2 or (argc == 2 and sys.argv[1].lower() in ("-h", "--help", "/?")):
    # The print function displays text
    print(f"USAGE:\n\t<stdin_data> | {sys.argv[0]} <file_name>")
    # The print function displays text
    print("DESCRIPTION:\n\tThis script is used in order make sure that the files written to the disk are in the correct format.")
    # If the argument count is not 2, exit with an error
    if argc != 2:
        sys.exit(error)
    # If we did not exit before, we exit with a success code
    sys.exit(success)

# If we passed the check sequence, we open a file with the name passed as an argument (with a few encoding parameters)
with open(f"{sys.argv[1]}", "w", encoding="utf-8", newline="\n") as file:
    # We get the content piped in by the user
    data = sys.stdin.read()
    # We write it to a file
    file.write(data)
# Once the with loop is exited, the file is automatically closed
# We display the "data is written to the file" message on the user's screen
print("The data is written to the file")
