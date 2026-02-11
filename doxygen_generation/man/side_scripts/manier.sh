#!/bin/bash
export PS1="NOT_IN_DOCKER> "
echo "beginning of script"
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
rm -vf ./Doxyfile ./test_doxygen.sh ./documentation/man/installer.sh
cp -vf /home/hhh/Documents/my_repositories/Hanra-s-work/my_zappy/bonus/doxygen_docker/Doxyfile /home/hhh/Documents/my_repositories/Hanra-s-work/my_zappy/bonus/test_doxygen.sh /home/hhh/Documents/my_repositories/Hanra-s-work/my_zappy/bonus/doxygen_docker/man/installer.sh .
mv ./installer.sh ./documentation/man/installer.sh
sudo docker stop fedo
sudo docker system prune -f
sudo docker run -it -v "$(pwd)":"/home" --name fedo fedora:34 /bin/bash -c "dnf install -y sed man-db && cd /home/documentation/man && ./installer.sh -d  && export PS1='IN_A_DOCKER> ' && bash || export PS1='IN_AN_ERROR_DOCKER> ' && bash" #> data.txt 2>&1
echo "End of script"
