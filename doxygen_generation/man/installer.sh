#!/bin/bash
##
## EPITECH PROJECT, 2024
## my_area
## File description:
## installer.sh
##

# Boolean data
TRUE=1
FALSE=0
DEBUG=$FALSE

# This is a simple python program that take the standard input and an output file and then write the input to the file under the correct format
PYTHON_ENCODER="/tmp/file_charset_changer.py"

# Man pages meta-data
EMAIL='<henrysoftwarehouse@protonmail\&.com>'

# SPECIAL_CHARACTERS
SC_BACKSLASH='\'
SC_QUOTE='"'
SC_TAB="${SC_BACKSLASH}t"
SC_SPACE="${SC_BACKSLASH} "
SC_DASH="${SC_BACKSLASH}-"

# Man pages known commands
M_COMMENT=".${SC_BACKSLASH}${SC_QUOTE}"

# Man Styles Inline
MSI_BULLET="${SC_BACKSLASH}[bu]"
MSI_BOLD="${SC_BACKSLASH}${SC_BACKSLASH}fB"
MSI_RESET="${SC_BACKSLASH}${SC_BACKSLASH}fR"
MSI_ITALIC="${SC_BACKSLASH}${SC_BACKSLASH}fI"
MSI_COMMA="${SC_BACKSLASH},"

# Man file manager
MF_NEWLINE='\n'

function decho {
    if [ $DEBUG -eq $TRUE ]; then
        echo "$1"
    fi
}

function count_files_in_man_folder {
    decho "Counting files in man folder" >&2
    DIRECTORY="$1"/*.3
    FILE_COUNT=$(ls -1 $DIRECTORY 2>/dev/null | wc -l)
    decho "File count: $FILE_COUNT" >&2
    echo "$FILE_COUNT"
}

function dump_python_charset_changer_for_file {
    decho "Creating file charset changer"
    echo '#!/bin/env python3' >"$PYTHON_ENCODER"
    echo '# Import the sys package in order to get the standard input' >>"$PYTHON_ENCODER"
    echo 'import sys' >>"$PYTHON_ENCODER"
    echo 'error = 1  # The status when the program fails' >>"$PYTHON_ENCODER"
    echo 'success = 0  # The status when the program succeeds' >>"$PYTHON_ENCODER"
    echo 'argc = len(sys.argv)' >>"$PYTHON_ENCODER"
    echo '# Check if the argument count is not equal to 2 or (if the argument count is equal to 2 check that the content corresponds to a help call)' >>"$PYTHON_ENCODER"
    echo 'if argc != 2 or (argc == 2 and sys.argv[1].lower() in ("-h", "--help", "/?")):' >>"$PYTHON_ENCODER"
    echo '    # The print function displays text' >>"$PYTHON_ENCODER"
    echo '    print(f"USAGE:\n\t<stdin_data> | {sys.argv[0]} <file_name>")' >>"$PYTHON_ENCODER"
    echo '    # The print function displays text' >>"$PYTHON_ENCODER"
    echo '    print("DESCRIPTION:\n\tThis script is used in order make sure that the files written to the disk are in the correct format.")' >>"$PYTHON_ENCODER"
    echo '    # If the argument count is not 2, exit with an error' >>"$PYTHON_ENCODER"
    echo '    if argc != 2:' >>"$PYTHON_ENCODER"
    echo '        sys.exit(error)' >>"$PYTHON_ENCODER"
    echo '    # If we did not exit before, we exit with a success code' >>"$PYTHON_ENCODER"
    echo '    sys.exit(success)' >>"$PYTHON_ENCODER"
    echo '# If we passed the check sequence, we open a file with the name passed as an argument (with a few encoding parameters)' >>"$PYTHON_ENCODER"
    echo 'with open(f"{sys.argv[1]}", "w", encoding="utf-8", newline="\n") as file:' >>"$PYTHON_ENCODER"
    echo '    # We get the content piped in by the user' >>"$PYTHON_ENCODER"
    echo '    data = sys.stdin.read()' >>"$PYTHON_ENCODER"
    echo '    # We write it to a file' >>"$PYTHON_ENCODER"
    echo '    file.write(data)' >>"$PYTHON_ENCODER"
    echo '# Once the with loop is exited, the file is automatically closed' >>"$PYTHON_ENCODER"
    echo '# We display the "data is written to the file" message on the user"s screen' >>"$PYTHON_ENCODER"
    echo 'print("The data is written to the file")' >>"$PYTHON_ENCODER"
    echo "Granting execution wrights to: '$PYTHON_ENCODER'"
    chmod a+x $PYTHON_ENCODER
    chmod u+x $PYTHON_ENCODER
    chmod g+x $PYTHON_ENCODER
}

function get_files_in_man_folder {
    decho "In get file in man folder" >&2
    decho "PWD = $(pwd)" >&2
    DIRECTORY="$1"/*.3
    decho "Directory = $DIRECTORY, \$1 = $1" >&2
    if [ -z "$(ls -A $DIRECTORY 2>/dev/null)" ]; then
        echo "No .3 files found in $1"
        return
    fi
    MAN_CONTENT=""
    decho "Files found:" >&2
    # Iterate over the files in the directory and append their names to the man page
    for file in $DIRECTORY; do
        # Extract the file name and remove the ".3" extension
        filename=$(basename "$file")
        filename_without_extension="${filename%.3}"
        decho "file: '$filename_without_extension'" >&2
        # Append the file name to the man page content
        MAN_CONTENT+="\n.B ${MAN_PROG_DIR}/${filename_without_extension}\n"
        MAN_CONTENT+="\n.so ${MAN_PROG_DIR}/${filename}\n"
    done
    decho "Out of get file in man folder" >&2
    echo -e "$MAN_CONTENT"
}

function create_homepage_man {
    decho "In create homepage man" >&2
    decho "MAN_FOLDER='$4'" >&2
    local FILE_COUNT=$(count_files_in_man_folder "$4")
    local MAN_FILES=$(get_files_in_man_folder "$4")
    local HOMEPAGE="${M_COMMENT} Manpage for Area project
${M_COMMENT} Contact: Henry Letellier ${EMAIL}.
.TH AREA ${SC_QUOTE}EPITECH${SC_QUOTE} 6 ${SC_QUOTE}September 2024${SC_QUOTE} ${SC_QUOTE}Version 1.0${SC_QUOTE} ${SC_QUOTE}Area Manual${SC_QUOTE}
.PP
.SH NAME
AREA ${SC_BACKSLASH}-${SC_SPACE}Welcome${SC_SPACE}to${SC_SPACE}Area!
.PP
.SH SYNOPSIS
.nf
.BI Area${SC_SPACE}${SC_TAB}${SC_TAB}${SC_SPACE}${SC_SPACE}${SC_SPACE}${SC_SPACE}-${SC_SPACE}${MSI_RESET} https://pingpal\&.news/
.BI Area${SC_SPACE}documentation${SC_SPACE}-${SC_SPACE}${MSI_RESET} https://ifttt-area\&.pingpal\&.news/
.fi
.SH DESCRIPTION
.nf
.BI ${MSI_RESET}The${SC_SPACE}Area${SC_SPACE}project${SC_SPACE}is${SC_SPACE}directly${SC_SPACE}inspired${SC_SPACE}by${SC_SPACE}the${SC_SPACE}ifttt${SC_SPACE}(https://ifttt\&.com)${SC_SPACE}project.
.BI ${SC_SPACE}${MSI_RESET}This${SC_SPACE}project${SC_SPACE}aims${SC_SPACE}to${SC_SPACE}automate${SC_SPACE}everyday${SC_SPACE}actions${SC_SPACE}through${SC_SPACE}various${SC_SPACE}APIs${SC_SPACE}and${SC_SPACE}sequences${SC_SPACE}of${SC_SPACE}events${SC_SPACE}that${SC_SPACE}are${SC_SPACE}defined${SC_SPACE}by${SC_SPACE}the${SC_SPACE}user.
.BI ${MSI_RESET}
.BI ${MSI_RESET}The${SC_SPACE}project${SC_SPACE}consists${SC_SPACE}of${SC_SPACE}five${SC_SPACE}major${SC_SPACE}services:
.IP ${MSI_BULLET}
Website (https://pingpal\&.news/):
.BI ${MSI_RESET}${SC_TAB}This${SC_SPACE}service${SC_SPACE}is${SC_SPACE}the${SC_SPACE}one${SC_SPACE}in${SC_SPACE}charge${SC_SPACE}of${SC_SPACE}providing${SC_SPACE}the${SC_SPACE}user${SC_SPACE}with${SC_SPACE}an${SC_SPACE}intuitive${SC_SPACE}interface${SC_SPACE}regardless${SC_SPACE}of${SC_SPACE}the${SC_SPACE}device${SC_SPACE}it${SC_SPACE}is${SC_SPACE}being${SC_SPACE}accessed${SC_SPACE}on.
.BI ${MSI_RESET}${SC_TAB}This${SC_SPACE}service${SC_SPACE}is${SC_SPACE}also${SC_SPACE}the${SC_SPACE}one${SC_SPACE}that${SC_SPACE}will${SC_SPACE}allow${SC_SPACE}the${SC_SPACE}user${SC_SPACE}to${SC_SPACE}download${SC_SPACE}it's${SC_SPACE}mobile${SC_SPACE}equivalent.
.IP ${MSI_BULLET}
Mobile application (Available at https://pingpal\&.news/):
.BI ${MSI_RESET}${SC_TAB}The${SC_SPACE}mobile${SC_SPACE}application${SC_SPACE}aims${SC_SPACE}to${SC_SPACE}provide${SC_SPACE}a${SC_SPACE}way${SC_SPACE}to${SC_SPACE}remain${SC_SPACE}intergrated${SC_SPACE}in${SC_SPACE}the${SC_SPACE}user's${SC_SPACE}life${SC_SPACE}in${SC_SPACE}a${SC_SPACE}more${SC_SPACE}stable${SC_SPACE}way${SC_SPACE}so${SC_SPACE}that${SC_SPACE}the${SC_SPACE}user${SC_SPACE}doesn't${SC_SPACE}have${SC_SPACE}to${SC_SPACE}fear${SC_SPACE}about${SC_SPACE}missing${SC_SPACE}out${SC_SPACE}on${SC_SPACE}their${SC_SPACE}flows.
.IP ${MSI_BULLET}
Server (https://ifttt-back\&.pingpal\&.news/):
.BI ${MSI_RESET}${SC_TAB}This${SC_SPACE}service${SC_SPACE}is${SC_SPACE}the${SC_SPACE}backbone${SC_SPACE}of${SC_SPACE}the${SC_SPACE}project.
.BI ${MSI_RESET}${SC_TAB}It${SC_SPACE}is${SC_SPACE}the${SC_SPACE}one${SC_SPACE}that${SC_SPACE}will${SC_SPACE}handle${SC_SPACE}all${SC_SPACE}the${SC_SPACE}traffic,${SC_SPACE}the${SC_SPACE}accounts${SC_SPACE}and${SC_SPACE}the${SC_SPACE}flows.
.IP ${MSI_BULLET}
Database (Mariadb [this is internal to the Server]):
.BI ${MSI_RESET}${SC_TAB}The${SC_SPACE}database${SC_SPACE}is${SC_SPACE}a${SC_SPACE}core${SC_SPACE}part${SC_SPACE}of${SC_SPACE}the${SC_SPACE}server.
.BI ${MSI_RESET}${SC_TAB}It${SC_SPACE}is${SC_SPACE}the${SC_SPACE}one${SC_SPACE}that${SC_SPACE}will${SC_SPACE}store${SC_SPACE}all${SC_SPACE}the${SC_SPACE}informations${SC_SPACE}that${SC_SPACE}the${SC_SPACE}users${SC_SPACE}provide${SC_SPACE}as${SC_SPACE}well${SC_SPACE}as${SC_SPACE}accounts,${SC_SPACE}api's${SC_SPACE}and${SC_SPACE}flows.
.IP ${MSI_BULLET}
S3 bucket (Minion [this is internal to the Server]):
.BI ${MSI_RESET}${SC_TAB}The${SC_SPACE}S3${SC_SPACE}bucket${SC_SPACE}is${SC_SPACE}a${SC_SPACE}locally${SC_SPACE}deployed${SC_SPACE}service${SC_SPACE}that${SC_SPACE}aims${SC_SPACE}to${SC_SPACE}store${SC_SPACE}the${SC_SPACE}data${SC_SPACE}that${SC_SPACE}the${SC_SPACE}database${SC_SPACE}could${SC_SPACE}not.
.BI ${MSI_RESET}${SC_TAB}The${SC_SPACE}S3${SC_SPACE}bucket${SC_SPACE}will${SC_SPACE}store${SC_SPACE}files${SC_SPACE}that${SC_SPACE}are${SC_SPACE}required${SC_SPACE}to${SC_SPACE}be${SC_SPACE}accessed${SC_SPACE}by${SC_SPACE}the${SC_SPACE}website${SC_SPACE}and${SC_SPACE}app.
.PP
.BI ${MSI_RESET}The${SC_SPACE}Area${SC_SPACE}project${SC_SPACE}offers${SC_SPACE}an${SC_SPACE}interesting${SC_SPACE}yet${SC_SPACE}challenging${SC_SPACE}project${SC_SPACE}that${SC_SPACE}can${SC_SPACE}be${SC_SPACE}used${SC_SPACE}in${SC_SPACE}our${SC_SPACE}everyday${SC_SPACE}life.
.fi
.SH AUTHOR
Written by (c) Henry Letellier.
.PP
.SH DEVELOPERS
.nf
.B (c)${SC_SPACE}Harleen${SC_SPACE}Singh-Kaur
.B (c)${SC_SPACE}Eric${SC_SPACE}Xu
.B (c)${SC_SPACE}Flavien${SC_SPACE}Maillard
.B (c)${SC_SPACE}Thomas${SC_SPACE}Lebouc
.B (c)${SC_SPACE}Henry${SC_SPACE}Letellier
.fi
.PP
.SH COPYRIGHT
.nf
.BI ${MSI_RESET}This${SC_SPACE}is${SC_SPACE}a${SC_SPACE}project${SC_SPACE}that${SC_SPACE}was${SC_SPACE}created${SC_SPACE}during${SC_SPACE}our${SC_SPACE}third${SC_SPACE}year${SC_SPACE}at${SC_SPACE}Epitech.
.BI ${MSI_RESET}Thus,${SC_SPACE}feel${SC_SPACE}free${SC_SPACE}to${SC_SPACE}use${SC_SPACE}this${SC_SPACE}project,${SC_SPACE}but${SC_SPACE}you${SC_SPACE}cannot${SC_SPACE}edit,${SC_SPACE}sel${SC_SPACE}or${SC_SPACE}re-sel${SC_SPACE}it.
.fi
.PP
.SH BUGS
.nf
.BI ${MSI_RESET}Please${SC_SPACE}report${SC_SPACE}any${SC_SPACE}bugs${SC_SPACE}to${SC_SPACE}${EMAIL}.
.BI ${MSI_RESET}Although,${SC_SPACE}there${SC_SPACE}is${SC_SPACE}absolutely${SC_SPACE}no${SC_SPACE}guaranty${SC_SPACE}that${SC_SPACE}it${SC_SPACE}will${SC_SPACE}be${SC_SPACE}fixed.
.BI ${MSI_RESET}Another${SC_SPACE}way${SC_SPACE}would${SC_SPACE}be${SC_SPACE}to${SC_SPACE}open${SC_SPACE}an${SC_SPACE}issue${SC_SPACE}on${SC_SPACE}the${SC_SPACE}github${SC_SPACE}project,${SC_SPACE}see${SC_SPACE}${SC_QUOTE}PROJECT${SC_SPACE}RESSOURCES${SC_QUOTE}${SC_SPACE}for${SC_SPACE}more${SC_SPACE}details.
.fi
.PP
.SH NOTES
.nf
.BI ${MSI_ITALIC}This${SC_SPACE}man${SC_SPACE}page${SC_SPACE}is${SC_SPACE}for${SC_SPACE}informational${SC_SPACE}purposes${SC_SPACE}only.
.BI ${MSI_RESET}You${SC_SPACE}can${SC_SPACE}also${SC_SPACE}find${SC_SPACE}links${SC_SPACE}concerning${SC_SPACE}the${SC_SPACE}project${SC_SPACE}in${SC_SPACE}${SC_QUOTE}PROJECT${SC_SPACE}RESSOURCES${SC_QUOTE}
.fi
.PP
.SH PROJECT RESSOURCES
.nf
.BI ${MSI_RESET}Website:${SC_SPACE}https://pingpal\\&.news/
.BI ${MSI_RESET}Source${SC_SPACE}code${SC_SPACE}(Github):${SC_SPACE}https://github\\&.com/bazar-de-komi/terarea
.BI ${MSI_RESET}Documentation:${SC_SPACE}https://iftt-area\\&.pingpal\\&.news/
.fi
.PP
.SH DISCLAIMER
.PP
This software is provided ${SC_QUOTE}as is${SC_QUOTE} without warranty of any kind. Use at your own risk.
.PP
.SH VERSION
1.0
.PP
.SH DATE
September 2024
.PP
.SH SUB-PAGE DOXY DUMP [${FILE_COUNT} file(s)]
$MAN_FILES
"
    decho "Homepage generated" >&2
    mkdir -p "$1"
    if [ $DEBUG -eq $TRUE ]; then
        echo -e "$HOMEPAGE"
    fi
    echo -e "$HOMEPAGE" | $PYTHON_ENCODER "$1/$2.$3"
}

function update_man_paths {
    MAN_DEST="$1"
    # Update the shell man paths to include the area folder
    echo "Updating the shell man paths to include the area folder"
    export MANPATH="/usr/local/man:/usr/local/share/man:/usr/share/man:$MAN_DEST:$MANPATH"
    SHELL_PATHS=("/etc/bash.bashrc" "/etc/bashrc" "/etc/profile" "/etc/zsh/zshenv" "/etc/zshrc" "/etc/fish/config.fish")

    SHELL_LINE="export MANPATH=\"/usr/local/man:/usr/local/share/man:/usr/share/man:$MAN_DEST:\$MANPATH\""
    for i in "${SHELL_PATHS[@]}"; do
        # Check if the line is already present in the file
        if ! grep -qF "$SHELL_LINE" "$i"; then
            echo "$SHELL_LINE" >>"$i"
            decho "Added MANPATH to '$i'"
        else
            decho "MANPATH is already present in '$i' not adding"
        fi
    done
    echo "Updated the shell man paths to include the area folder"
}

function add_required_mans {
    MAN_DEST="$2"
    MAN_DIR="$1"
    shift 2
    MANS=("$@")
    # Create a symbolic link for the main man page
    for i in "${MANS[@]}"; do
        MAN_FILE="$i" #"${i%.*}"
        if [ ! -L "$MAN_DEST/$i" ]; then
            echo "Creating symbolic link of '$MAN_DEST/$i' to '$MAN_DIR/$MAN_FILE'"
            ln -sf "$MAN_DEST/$i" "$MAN_DIR/$MAN_FILE"
            STATUS=$?
            if [ $STATUS -ne 0 ]; then
                echo "This operation failed, please re-run this program with -d or do the operation manually"
                exit $STATUS
            fi
            echo "Symbolic link created of '$MAN_DEST/$i' to '$MAN_DIR/$MAN_FILE'"
        else
            echo "A symbolic link of '$MAN_DEST/$i' to '$MAN_DIR/$MAN_FILE' already exists"
        fi
    done
}

function update_man_db {
    MY_MAN_PATH="$1"
    DESTINATION="$2"
    PROJECT_DIRECTORY="$3"
    if [ "$MY_MAN_PATH" = "" ]; then
        echo "Argument 1 cannot be empty (update man db)"
        return
    fi
    if grep -qF "$MY_MAN_PATH" "$DESTINATION"; then
        echo "The man paths for area are correct"
        return
    fi
    echo "#" >>"$DESTINATION"
    echo "#---------------------------------------------------------" >>"$DESTINATION"
    echo "# These are injections so that the '$PROJECT_DIRECTORY' man works properly" >>"$DESTINATION"
    echo "# Adding '$PROJECT_DIRECTORY' to the search path of the man so that you can do man '$PROJECT_DIRECTORY/child_element'" >>"$DESTINATION"
    decho "# Adding '$PROJECT_DIRECTORY' to the search path of the man so that you can do man '$PROJECT_DIRECTORY/child_element'"
    echo "MANDATORY_MANPATH			$MY_MAN_PATH" >>"$DESTINATION"
    decho "# Adding '$PROJECT_DIRECTORY' to the user specifiable targets"
    sed -i "s/^SECTION.*/& $PROJECT_DIRECTORY/" "$DESTINATION"
    echo "The man db file has been updated"
}

function update_database {
    # Update the man database
    echo "Updating database"
    mandb
    STATUS=$?
    if [ $STATUS -ne 0 ]; then
        echo "This operation failed, please re-run this program with -d or do the operation manually"
        exit $STATUS
    fi
    echo "Database updated"
}

function display_help() {
    echo "USAGE:"
    echo "       $0   [-h|--help|-d]"
    echo "PARAMETERS:"
    echo "       -h or --help is to display this help section"
    echo "       -d or --debug is to enable a debug display of the program"
}

# Check if administrator
if [ $# -ge 2 ]; then
    display_help
    exit 1
fi

if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    display_help
    exit 0
fi

if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root."
    sudo $0 $@
    exit $?
fi

if [ "$1" == "-d" ] || [ "$1" == "--debug" ]; then
    DEBUG=$TRUE
else
    DEBUG=$FALSE
fi

# Define the installation directory for man pages
UPDATE_DB_FILE=$TRUE
MAN_DIR="/usr/share/man/"
MAN_PROG_DIR="area"
MAN_DEST="${MAN_DIR}${MAN_PROG_DIR}"
MAN_LEVEL=6
MAN_SHORTCUT_HOME="${MAN_DIR}man${MAN_LEVEL}"
MAN_SHORTCUT_BINS="${MAN_DIR}man1"
MAN_SOURCE="./man6"
MAN_DB="/etc/man_db.conf"

# Create a python file that will be used to change the file encoding of the man pages we are going to create
# See function content for line by line comments
dump_python_charset_changer_for_file

# Removing existing man pages if they exist
echo "Removing previous manual entries of this program if they existed"
decho "Removing '$MAN_DEST' entry if it exists"
if [ $DEBUG -eq $TRUE ]; then
    rm -rvf "$MAN_DEST"
else
    rm -rf "$MAN_DEST"
fi
STATUS=$?
if [ $STATUS -ne 0 ]; then
    echo "This operation failed, please re-run this program with -d or do the operation manually"
    exit $STATUS
fi
decho "Removing '${MAN_SHORTCUT_HOME}/${MAN_PROG_DIR}.${MAN_LEVEL}' if it exists"
if [ $DEBUG -eq $TRUE ]; then
    rm -vf "${MAN_SHORTCUT_HOME}/${MAN_PROG_DIR}.${MAN_LEVEL}"
else
    rm -f "${MAN_SHORTCUT_HOME}/${MAN_PROG_DIR}.${MAN_LEVEL}"
fi
STATUS=$?
if [ $STATUS -ne 0 ]; then
    echo "This operation failed, please re-run this program with -d or do the operation manually"
    exit $STATUS
fi
decho "Removed '$MAN_DEST' and '$MAN_DIR/area.3' if they existed"
echo "Previous entries, if present, have been removed"

# Create the directory structure for your project's man pages
decho "Creating folder '$MAN_DEST'"
mkdir -p "$MAN_DEST"
STATUS=$?
if [ $STATUS -ne 0 ]; then
    echo "This operation failed, please re-run this program with -d or do the operation manually"
    exit $STATUS
fi
decho "Created folder '$MAN_DEST'"

# Copy or move your man pages into the appropriate directory
echo "Copying contents from the data folder to the man folder"
cd $MAN_SOURCE
STATUS=$?
if [ $STATUS -ne 0 ]; then
    echo "This operation failed, please re-run this program with -d or do the operation manually"
    exit $STATUS
fi
if [ $DEBUG -eq $TRUE ]; then
    cp -rvf * "$MAN_DEST"
else
    cp -rf * "$MAN_DEST"
fi
STATUS=$?
if [ $STATUS -ne 0 ]; then
    echo "This operation failed, please re-run this program with -d or do the operation manually"
    exit $STATUS
fi
cd ..
echo "Content of '$MAN_SOURCE' has been copied to '$MAN_DEST'"

# Creating the homepage
echo "Generating homepage"
create_homepage_man "$MAN_DEST" "$MAN_PROG_DIR" "$MAN_LEVEL" "$MAN_SOURCE"
STATUS=$?
if [ $STATUS -ne 0 ]; then
    echo "This operation failed, please re-run this program with -d or do the operation manually"
    exit $STATUS
fi
echo "Homepage has been generated"

echo "Adding required man links"
add_required_mans "$MAN_SHORTCUT_HOME" "$MAN_DEST" "area.6"
echo "Added required man links"

if [ "$UPDATE_DB_FILE" = "$TRUE" ]; then
    decho "You chose to update the db file"
    update_man_db "$MAN_DEST" "$MAN_DB" "$MAN_PROG_DIR"
else
    decho "You chose to use the MANPATH environment variable"
    update_man_paths "$MAN_DEST"
fi

update_database

echo "Installation complete. You can now use 'man area' to access the manual page."
echo "Please relaunch any terminal instances you have for the full effect of the new man pages to be applied"

echo "(C) Created by Henry Letellier"
echo "This program is provided as if and without any warranty"
