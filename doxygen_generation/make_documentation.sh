#!/bin/bash
##
## EPITECH PROJECT, 2024
## tty_ov
## File description:
## make_documentation.sh
##

# Go to the root of the repository
cd ../../

# Basic constants
YES="YES"
NO="NO"

# Global info about the project

PROJECT_NAME="tty_ov"
PROJECT_VERSION="1.0"

# Files to include in scan
FILES_TO_INCLUDE_IN_SCAN="*.cpp *.h *.hpp *.h++ *.py *.js"

# Folders to exclude
FOLDERS_TO_EXCLUDE="app/back/server/server_env app/back/db/cache app/back/s3/cache app/front/mobile/node_modules app/front/web/node_modules"

# headerfiles include
INCLUDE_PATH="./include"

# Enable/disable recursive parsing of include files
INCLUDE_FILE_PATTERNS="*.h *.h *.hpp *.h++"

# Graph generation
GENERATE_CLASS_DIAGRAMS=$YES
GENERATE_COLLABORATION_GRAPHS=$YES
SORT_MEMBER_DOCS=$YES
SORT_BRIEF_DOCS=$YES

# Output generations
GENERATE_HTML=$YES
GENERATE_LATEX=$YES
GENERATE_RTF=$YES
GENERATE_XML=$YES
GENERATE_MAN=$YES
GENERATE_DOCBOOK=$YES
GENERATE_MD=$YES

## HTML dependencies
HTML_DIR="html"
HTML_EXTENSION=".html"
HTML_HEADER="header.html"
HTML_FOOTER="footer.html"
HTML_HEADER_CONTENT='
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Project Documentation</title>
    <!-- Include any additional CSS or meta tags here -->
</head>
<body>
    <header>
        <h1>Welcome to My Project Documentation</h1>
        <!-- You can include any header content here -->
    </header>
    <nav>
        <!-- Navigation links can be placed here -->
    </nav>
    <main>'
HTML_FOOTER_CONTENT="
</main>
    <footer>
        <p>&copy; $(date +'%Y') $PROJECT_NAME. All rights reserved.</p>
        <!-- You can include any footer content here -->
    </footer>
    <!-- Include any additional JavaScript or scripts here -->
</body>
</html>"

## LaTeX dependencies
LATEX_DIR="latex"
LATEX_EXTENSION=".tex"
LATEX_HEADER="header.tex"
LATEX_FOOTER="footer.tex"
LATEX_HEADER_CONTENT="
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{hyperref}
\title{My Project Documentation}
\author{My Name}
\date{2024}
\begin{document}
\maketitle
\tableofcontents
\newpage"
LATEX_FOOTER_CONTENT="
\end{document}"

## RTF dependencies
RTF_DIR="rtf"
COMPACT_RTF=$YES

## XML dependencies
XML_DIR="xml"

## MAN dependencies
MAN_DIR="man"
MAN_EXTENSION=".1"

## DOCBOOK dependencies
DOCBOOK_DIR="docbook"

## Markdown dependencies
MARKDOWN_DIR="markdown"

# Additional features
EXTRACT_ALL=$YES
HIDE_UNDOC_MEMBERS=$NO
HIDE_UNDOC_CLASSES=$NO

# Global status
ERROR=1
SUCCESS=0
STATUS=$SUCCESS

# Global booleans
TRUE=1
FALSE=0

# Global admin stuff
SUDO=/bin/sudo

# Docker container stuff
CONTAINER_NAME="doxygen"
CONTAINER_TAG="v$(date +"%Y-%m-%d")"
CONTAINER_PATH_NAME="hanralatalliard/${CONTAINER_NAME}"
CONTAINER_FINAL_NAME="${CONTAINER_PATH_NAME}:${CONTAINER_TAG}"
DOCKERFILE_PATH="bonus/doxygen_generation/"

# Docker volume management
## The destination for the generated documentation
DOCUMENTATION_FOLDER="$(pwd)/doc"
CONTAINER_DOCUMENTATION_FOLDER="/app/doc"
## The source of the project
REPOSITORY_PATH="$(pwd)"
REPOSITORY_DESTINATION="/app/repository"
## The temporary folder for the generated documentation
TEMPORARY_FOLDER="/app/tmp"

DOXYGEN_CONFIGURATION="
# Doxyfile

# Set project name and version
PROJECT_NAME           = \"$PROJECT_NAME\"
PROJECT_NUMBER         = $PROJECT_VERSION

# Set input and output directories
INPUT                  = $REPOSITORY_DESTINATION
OUTPUT_DIRECTORY       = $TEMPORARY_FOLDER

# Set source file extensions
FILE_PATTERNS          = $FILES_TO_INCLUDE_IN_SCAN

# Include subdirectories
RECURSIVE              = YES

# Exclude specific directories or files
EXCLUDE                = $FOLDERS_TO_EXCLUDE

# Specify additional directories to include in the search path
INCLUDE_PATH           = $INCLUDE_PATH

# Enable/disable recursive parsing of include files
INCLUDE_FILE_PATTERNS  = $INCLUDE_FILE_PATTERNS

# Enable/disable generation of inheritance diagrams
HAVE_DOT               = YES
CLASS_DIAGRAMS         = $GENERATE_CLASS_DIAGRAMS

# Enable/disable generation of collaboration diagrams
COLLABORATION_GRAPH   = $GENERATE_COLLABORATION_GRAPHS

# Set the order of the members in the documentation
SORT_MEMBER_DOCS       = $SORT_MEMBER_DOCS

# Set the order of the files in the documentation
SORT_BRIEF_DOCS        = $SORT_BRIEF_DOCS

# Specify the output format
GENERATE_HTML          = $GENERATE_HTML
GENERATE_LATEX         = $GENERATE_LATEX
GENERATE_RTF           = $GENERATE_RTF
GENERATE_XML           = $GENERATE_XML
GENERATE_MAN           = $GENERATE_MAN
GENERATE_DOCBOOK       = $GENERATE_DOCBOOK
GENERATE_MD            = $GENERATE_MD


# Set HTML output options
HTML_OUTPUT            = $HTML_DIR
HTML_FILE_EXTENSION    = $HTML_EXTENSION
HTML_HEADER            = $HTML_HEADER
HTML_FOOTER            = $HTML_FOOTER


# Set LaTeX output options
LATEX_OUTPUT           = $LATEX_DIR
LATEX_FILE_EXTENSION   = $LATEX_EXTENSION
LATEX_EXTRA_PACKAGES   = 


# Set RTF output options
RTF_OUTPUT             = $RTF_DIR
COMPACT_RTF            = $COMPACT_RTF


# Set XML output options
XML_OUTPUT             = $XML_DIR


# Set MAN output options
MAN_OUTPUT             = $MAN_DIR
MAN_EXTENSION          = $MAN_EXTENSION


# Set DOCBOOK output options
DOCBOOK_OUTPUT         = $DOCBOOK_DIR


# Set Markdown output options
MARKDOWN_OUTPUT        = $MARKDOWN_DIR

# Enable/disable additional options
EXTRACT_ALL            = $EXTRACT_ALL
HIDE_UNDOC_MEMBERS     = $HIDE_UNDOC_MEMBERS
HIDE_UNDOC_CLASSES     = $HIDE_UNDOC_CLASSES
"

# Debug mode (for development purposes)
DEBUG=$FALSE

# Publish container (for updating purposes)
PUBLISH=$FALSE

function run_command_in_container() {
    time $SUDO docker exec -it $CONTAINER_NAME /bin/bash -c "$1"
    STATUS=$?
    if [ $STATUS -ne $SUCCESS ]; then
        echo "Error while running '$1' in '$CONTAINER_PATH_NAME', ERROR CODE: $STATUS"
        exit $ERROR
    fi
}

# Remove python environement if present
LOCAL_CWD=$(pwd)
cd ./app/back/server/
if [ -d "server_env" ]; then
    $SUDO rm -rvf server_env
fi
if [ -d ".pytest_cache" ]; then
    $SUDO rm -rvf .pytest_cache
fi
if [ -f "Makefile" ]; then
    make ffclean
fi
cd $LOCAL_CWD

if [ -d "$DOCUMENTATION_FOLDER" ]; then
    rm -rf $DOCUMENTATION_FOLDER
fi
mkdir -p $DOCUMENTATION_FOLDER
$SUDO docker container stop $CONTAINER_NAME
$SUDO docker container rm -f $CONTAINER_NAME
$SUDO docker volume prune -f
if [ $DEBUG -eq $TRUE ]; then
    $SUDO docker image prune -f
    $SUDO docker system prune -f
fi
time $SUDO docker build -t $CONTAINER_PATH_NAME $DOCKERFILE_PATH
STATUS=$?
if [ $STATUS -ne $SUCCESS ]; then
    echo "Error while building the image, ERROR CODE: $STATUS"
    exit $ERROR
fi
if [ $PUBLISH -eq $TRUE ]; then
    time $SUDO docker build -t $CONTAINER_FINAL_NAME $DOCKERFILE_PATH
    time $SUDO docker push "${CONTAINER_FINAL_NAME}"
    time $SUDO docker push "$CONTAINER_PATH_NAME:latest"
    STATUS=$?
    if [ $STATUS -ne $SUCCESS ]; then
        echo "Error while publishing the container image '$CONTAINER_FINAL_NAME' '$CONTAINER_PATH_NAME', ERROR CODE: $STATUS"
    fi
fi
time $SUDO docker run -d -it -v "$DOCUMENTATION_FOLDER":"$CONTAINER_DOCUMENTATION_FOLDER" -v "$REPOSITORY_PATH":"$REPOSITORY_DESTINATION" --name $CONTAINER_NAME "${CONTAINER_PATH_NAME}:latest"
STATUS=$?
if [ $STATUS -ne $SUCCESS ]; then
    echo "Error while spinning up the container, ERROR CODE: $STATUS"
    exit $ERROR
fi

run_command_in_container "cd /app && echo \"$DOXYGEN_CONFIGURATION\" > Doxyfile"
if [ $DEBUG -eq $FALSE ]; then

    if [ $GENERATE_HTML == $YES ]; then
        run_command_in_container "cd /app && echo \"$HTML_HEADER_CONTENT\" > $HTML_HEADER"
        run_command_in_container "cd /app && echo \"$HTML_FOOTER_CONTENT\" > $HTML_FOOTER"
    fi
    if [ $GENERATE_LATEX == $YES ]; then
        run_command_in_container "cd /app && echo \"$LATEX_HEADER_CONTENT\" > $LATEX_HEADER"
        run_command_in_container "cd /app && echo \"$LATEX_FOOTER_CONTENT\" > $LATEX_FOOTER"
    fi
    run_command_in_container "cd /app && doxygen Doxyfile ; exit $?"
    run_command_in_container "cd /app && cp -rvf $TEMPORARY_FOLDER/* $CONTAINER_DOCUMENTATION_FOLDER ; exit $?"
    run_command_in_container "echo Data generated"
else
    echo "Debug mode enabled"
    run_command_in_container "dnf install -y nano emacs vim"
    time $SUDO docker exec -it $CONTAINER_NAME /bin/bash
fi

LOCAL_CWD=$(pwd)
cd ./app/back/server/
if [ -f "Makefile" ]; then
    make create_environement install_dependencies
fi
cd $LOCAL_CWD
$SUDO chmod a+rw -R $DOCUMENTATION_FOLDER
