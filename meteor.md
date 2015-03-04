meteor.py
=======

awesome tool to manage an meteor environment

Clone this repo to <code>$path/scripts</code> (or some other subfolder of $path) and execute:

<code>./meteor.py -i</code>

the script will make the <code>$path/app</code> and <code>$path/develop</code> folders. Then ask for the environment variables like mongo connection and ports.

After initialisation you can run your Meteor App in develop or production environment. PM2 and git support will be added soon.

<code>
	./meteor.py -r # run default environment (develop)  
	./meteor.py -r -e production # run production environment  
	./meteor.py -b # build the app (files in develop are convertet to normal node.js code and saved in app folder  
	./meteor.py -r -b -e production # run production environment but build it before
</code>

## install ##

<code>
$ apt-get install python-pip  
$ pip install termcolor  
$ pip install configparser  
$ git clone https://github.com/Rackmonkey/scripts
</code>
