meteor.py
=======

awesome tool to manage an meteor environment

Clone this repo to <code>$path/scripts</code> (or some other subfolder of $path) and execute:

```
./meteor.py -i
```

the script will make the <code>$path/app</code>, <code>$path/develop</code>, <code>$path/backup</code> and <code>$path/config</code> folders. Then ask for the environment variables like mongo connection and ports. By default the connection options for develop environment are the defaults of meteor. If you want to use other settings you can modify the <code>$path/config/meteor.conf</code> by yourself.

After initialisation you can run your Meteor App in develop or production environment. 
PM2 support is in testing and git support will be added soon.

```
./meteor.py -r # run default environment (develop)  
./meteor.py -r -e production # run production environment  
./meteor.py -b # build the app (files in develop are convertet to normal node.js code and saved in app folder  
./meteor.py -r -b -e production # run production environment but build it before
./meteor.py --backup bak1 -e p # backup production mongo db to bak1 (folder in backup folder with the dump)
./meteor.py --restore bak1 -e p # comming very soon
```

## install ##

```
$ apt-get install python-pip  
$ pip install termcolor  
$ pip install configparser  
$ pip install demjson 
$ git clone https://github.com/Rackmonkey/scripts
$ git cd scripts
$ ./meteor.py -i
```

## -h output ##

```
usage: meteor.py [-h] [-b] [-r] [-i] [-e ENV] [--backup BACKUP]
[--restore RESTORE] [--list LIST]
 
meteor application helper
 
optional arguments:
-h, --help show this help message and exit
-b, --build build meteor app (pre running)
-r, --run run app
-i, --init init the environment
-e ENV, --env ENV develop OR production OR pm2
--backup BACKUP backup Mongo DB to file (pre running)
--restore RESTORE restore Mongo DB from file (pre running)
--list LIST list Mongo DB backups
```