# ItemCatalogAppProject README

## What is it???

This project is designed to hold a catalog of teams for professional soccer leagues throughout the world.  People can add, edit and delete categories(leagues) and teams  within the catalog system.

## Software Needed:

This program is being ran through a Virtual Machine environment using Vagrant. You will have to download all programs (if not have downloaded previously), depending on your operating system (windows, Linux, Apple)

    GIT: http://git-scm.com/downloads
    Virtual-Machine: https://www.virtualbox.org/wiki/Download_Old_Builds_5_1
    Vagrant: https://www.vagrantup.com/downloads.html


## Steps for Running the Application Successfully:

* Launch GIT Bash on your device.
* Run *git clone* https://github.com/ad988x/fullstack-nanodegree-vm.
* Once the user has cloned the directory, use the terminal to change the directory, *cd catalog* then type *vagrant up*.  Depending on your internet speed and computer, might take up to 20 minutes.
* The Virtual Machine should be up and working.  Once it is, type *vagrant ssh* (if vagrant ssh does not work properly, you can use winpty vagrant ssh), this will log in to the Virtual Machine and get a Linux shell prompt.
* Change the directory, *cd /vagrant*, this will take the user into the vagrant folder between the Virtual Machine and the users device.
Before running the catalog application, there are a good amount of python modules that will need to be installed through the Virtual Machine.  The user will have to use either *PIP INSTALL or SUDO PIP INSTALL* while running these modules

        flask
        sqlalchemy
        oauth2client
        httplib2
        json
        requests
        
* After the python modules have been installed, type *ls* to ensure that you are in the directory that states, database_setup.py, project.py, folders named templates and static.
* Type *python database_setup.py* to initialize the database.
* Type *python project.py*.
* Go into the browser using http://localhost:8000 to view the soccer league app.  

Once the user is logged into the application, they can then login through Facebook or Google+ Sign In. The user will also be able to view, add, edit and delete Categories and teams.
