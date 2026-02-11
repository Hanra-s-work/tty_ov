#!/bin/bash
##
## EPITECH PROJECT, 2024
## my_zappy
## File description:
## launch_server.sh
##

TRUE=1
FALSE=0
DEBUG=$FALSE

IMAGE_NAME="httpd:2.4.59" # This is a docker containing a web server (not the content being served)
CONTAINER_NAME="doxeb"
MOUNT_SRC_PATH="$(pwd)"
MOUNT_PATH_DEST="/usr/local/apache2/htdocs/"
MIN_EXPOSED_PORT=80
MAX_EXPOSED_PORT=8999
EXPOSED_PORT=$MIN_EXPOSED_PORT

function decho {
    if [ $DEBUG -eq $TRUE ]; then
        echo "$1"
    fi
}

function run_docker_command {
    decho "Executing the command : '$1'"
    docker exec -it $CONTAINER_NAME /bin/bash -c "$1"
    decho "Command: '$1' has been run, status code: $?"
    return $?
}

function stop_container {
    decho "Stopping previous container instance"
    docker stop $CONTAINER_NAME
    decho "Removing previous container instance"
    docker rm $CONTAINER_NAME
}

function spin_up_the_docker {
    stop_container
    decho "Spinning up a new version"
    docker run -it -d -v "$MOUNT_SRC_PATH":"$MOUNT_PATH_DEST" -p $EXPOSED_PORT:80 --name $CONTAINER_NAME $IMAGE_NAME
    STATUS=$?
    if [ $STATUS -ne 0 ]; then
        echo "Failed to start the server"
        echo "This error could be due to many factors, but here are a few to consider:"
        echo "* Low or abscent diskspace"
        echo "* Port already taken (despite the scan the program did)"
        echo "* No more ram"
        echo "* The Docker program is not running"
        echo "If you do not know the source of the issue, internet is your best friend"
        echo "The exit code was: $STATUS"
        exit $STATUS
    fi
}

function find_correct_port {

    for ((i = MIN_EXPOSED_PORT; i <= MAX_EXPOSED_PORT; i++)); do
        netstat -tuln | grep ":${i} " >/dev/null 2>&1
        if [ $? -ne 0 ]; then
            decho "Port: '$i' is not available"
        else
            decho "Port: '$i' is available"
            EXPOSED_PORT=$i
            return 0
        fi
    done

    echo "No ports available in the range, please expand your port range" >&2
    exit 1
}

function check_docker_is_installed {
    docker --version >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Docker is a component that is required for this program, please install it in order to view a web page"
        exit 1
    fi
    decho "Docker is installed"
    return 0
}

function my_pause {
    echo "Pause: press enter to continue ..."
    read
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

check_docker_is_installed
find_correct_port
spin_up_the_docker
echo "The webpage is available at: http://127.0.0.1:$EXPOSED_PORT"
echo "(C) Created by Henry Letellier"
echo "This program is provided as if and without any warranty"
echo "Press enter to kill the website or CTL+C to stop this script"
my_pause
stop_container
