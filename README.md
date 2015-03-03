scripts
=======

## readme explanations ##

**dependency:** Scripts you must start before you can use it. 

## setup_debian_basics ##
Installs some basic tools and add the sid repo to sources.list for the newest Apache and PHP  
**dependency:** -

## setup_apache_phpfpm_fcgi ##
Installs a full Apache 2.4, PHP-fpm 5.6 and fcgi Setup.  
**dependency:** setup_debian_basics  


## setup_domain ##

Setups a vHost for an Domain.  
**dependency:** setup_apache_phpfpm_fcgi **&&** setup_debian_basics

## meteor.py ##
awesome tool to manage an meteor environment

Clone this repo to <code>$path/scripts</code> (or some other subfolder of $path) and execute:

<code>./meteor.py -i</code>

the script will make the <code>$path/app</code> and <code>$path/develop</code> folders. Then ask for the environment variables like mongo connection and ports.

After initialisation you can run your Meteor App in develop or production environment. PM2 and git support will be added soon.

<code>./meteor.py -r # run default environment (develop)</code>

<code>./meteor.py -r -e production # run production environment</code>

<code>./meteor.py -b # build the app (files in develop are convertet to normal node.js code and saved in app folder</code>

<code>./meteor.py -r -b -e production # run production environment but build it before</code>

**dependency:** -
